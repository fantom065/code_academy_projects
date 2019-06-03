#!/usr/bin/env python
# coding: utf-8

# # Capstone Project 1: MuscleHub AB Test

# ## Step 1: Get started with SQL

# Like most businesses, Janet keeps her data in a SQL database.  Normally, you'd download the data from her database to a csv file, and then load it into a Jupyter Notebook using Pandas.
# 
# For this project, you'll have to access SQL in a slightly different way.  You'll be using a special Codecademy library that lets you type SQL queries directly into this Jupyter notebook.  You'll have pass each SQL query as an argument to a function called `sql_query`.  Each query will return a Pandas DataFrame.  Here's an example:

# In[1]:


# This import only needs to happen once, at the beginning of the notebook
from codecademySQL import sql_query


# In[2]:


# Here's an example of a query that just displays some data
sql_query('''
SELECT *
FROM visits
LIMIT 5
''')


# In[3]:


# Here's an example where we save the data to a DataFrame
df = sql_query('''
SELECT applications.first_name, applications.last_name, applications.email, purchases.purchase_date
FROM applications
LEFT JOIN purchases
ON applications.first_name = purchases.first_name
AND applications.last_name = purchases.last_name
AND applications.email = purchases.email

LIMIT 10;
''')


# In[4]:


print df.head(10)


# ## Step 2: Get your dataset

# Let's get started!
# 
# Janet of MuscleHub has a SQLite database, which contains several tables that will be helpful to you in this investigation:
# - `visits` contains information about potential gym customers who have visited MuscleHub
# - `fitness_tests` contains information about potential customers in "Group A", who were given a fitness test
# - `applications` contains information about any potential customers (both "Group A" and "Group B") who filled out an application.  Not everyone in `visits` will have filled out an application.
# - `purchases` contains information about customers who purchased a membership to MuscleHub.
# 
# Use the space below to examine each table.

# In[5]:


# Examine visits here
sql_query('''
SELECT *
FROM visits
WHERE visit_date >= '7-1-17'
LIMIT 5;
''')


# In[6]:


# Examine fitness_tests here
sql_query('''
SELECT *
FROM fitness_tests
LIMIT 5;
''')


# In[7]:


# Examine applications here
sql_query('''
SELECT *
FROM applications
LIMIT 10;
''')


# In[8]:


sql_query('''
SELECT COUNT(first_name)
FROM applications;
''')


# In[9]:


# Examine purchases here
sql_query('''
SELECT *
FROM purchases
LIMIT 5;
''')


# We'd like to download a giant DataFrame containing all of this data.  You'll need to write a query that does the following things:
# 
# 1. Not all visits in  `visits` occurred during the A/B test.  You'll only want to pull data where `visit_date` is on or after `7-1-17`.
# 
# 2. You'll want to perform a series of `LEFT JOIN` commands to combine the four tables that we care about.  You'll need to perform the joins on `first_name`, `last_name`, and `email`.  Pull the following columns:
# 
# 
# - `visits.first_name`
# - `visits.last_name`
# - `visits.gender`
# - `visits.email`
# - `visits.visit_date`
# - `fitness_tests.fitness_test_date`
# - `applications.application_date`
# - `purchases.purchase_date`
# 
# Save the result of this query to a variable called `df`.
# 
# Hint: your result should have 5004 rows.  Does it?

# In[ ]:





# In[10]:


df = sql_query('''
SELECT visits.first_name, visits.last_name, visits.gender, visits.email, visits.visit_date, fitness_tests.fitness_test_date,
applications.application_date, purchases.purchase_date
FROM visits

LEFT JOIN applications
ON visits.first_name = applications.first_name
AND visits.last_name = applications.last_name
AND visits.email = applications.email

LEFT JOIN fitness_tests
ON visits.first_name = fitness_tests.first_name
AND visits.last_name = fitness_tests.last_name
AND visits.email = fitness_tests.email

LEFT JOIN purchases
ON visits.first_name = purchases.first_name
AND visits.last_name = purchases.last_name
AND visits.email = purchases.email
WHERE visit_date >= '7-1-17';
''')


# In[11]:


print df.info()


# In[12]:


df.head(10)


# The DataFrame does have 5004 rows. 

# ## Step 3: Investigate the A and B groups

# We have some data to work with! Import the following modules so that we can start doing analysis:
# - `import pandas as pd`
# - `from matplotlib import pyplot as plt`

# In[200]:


import pandas as pd
from matplotlib import pyplot as plt


# We're going to add some columns to `df` to help us with our analysis.
# 
# Start by adding a column called `ab_test_group`.  It should be `A` if `fitness_test_date` is not `None`, and `B` if `fitness_test_date` is `None`.

# In[14]:


df['ab_test_group'] = df.fitness_test_date.apply (lambda x: 'A' if pd.notnull(x) else 'B')


# In[15]:


df.head(10)


# Let's do a quick sanity check that Janet split her visitors such that about half are in A and half are in B.
# 
# Start by using `groupby` to count how many users are in each `ab_test_group`.  Save the results to `ab_counts`.

# In[16]:


ab_counts = df.groupby('ab_test_group').first_name.count().reset_index()


# In[17]:


print ab_counts


# There seems to be an equal(ish) amount of participants in each test group.

# We'll want to include this information in our presentation.  Let's create a pie cart using `plt.pie`.  Make sure to include:
# - Use `plt.axis('equal')` so that your pie chart looks nice
# - Add a legend labeling `A` and `B`
# - Use `autopct` to label the percentage of each group
# - Save your figure as `ab_test_pie_chart.png`

# In[218]:


test_groups = ["Test Group A - (fitness test)", "Test Group B - (no fitness test)"]
group_numbers = [2504, 2500]
plt.figure(figsize=(7,5))
plt.pie(group_numbers, labels=test_groups, autopct = '%0.1f%%') # labels each part & adds a percentage to one decimal place.
plt.title('A/B Test Groups')
plt.axis('equal')
plt.legend(test_groups, loc = 7)
plt.savefig('ab_test_pie_chart.png')
plt.show()


# ## Step 4: Who picks up an application?

# Recall that the sign-up process for MuscleHub has several steps:
# 1. Take a fitness test with a personal trainer (only Group A)
# 2. Fill out an application for the gym
# 3. Send in their payment for their first month's membership
# 
# Let's examine how many people make it to Step 2, filling out an application.
# 
# Start by creating a new column in `df` called `is_application` which is `Application` if `application_date` is not `None` and `No Application`, otherwise.

# In[19]:


df['is_application'] = df.application_date.apply(lambda x: "Application" if pd.notnull(x) else "No Application")


# In[20]:


df.head()


# Now, using `groupby`, count how many people from Group A and Group B either do or don't pick up an application.  You'll want to group by `ab_test_group` and `is_application`.  Save this new DataFrame as `app_counts`

# In[21]:


app_counts = df.groupby(['is_application', 'ab_test_group']).first_name.count().reset_index()


# In[22]:


print app_counts


# We're going to want to calculate the percent of people in each group who complete an application.  It's going to be much easier to do this if we pivot `app_counts` such that:
# - The `index` is `ab_test_group`
# - The `columns` are `is_application`
# Perform this pivot and save it to the variable `app_pivot`.  Remember to call `reset_index()` at the end of the pivot!

# In[23]:


app_pivot = app_counts.pivot(
    columns='is_application',
    index='ab_test_group',
    values='first_name').reset_index()


# In[24]:


print app_pivot


# Define a new column called `Total`, which is the sum of `Application` and `No Application`.

# In[25]:


app_pivot['Total'] = app_pivot.apply(lambda row: row.Application + row['No Application'], axis = 1)


# In[26]:


print app_pivot


# Calculate another column called `Percent with Application`, which is equal to `Application` divided by `Total`.

# In[27]:


app_pivot['percent_with_application'] = app_pivot.apply(lambda row: 1.*row.Application / row.Total, axis=1)


# In[28]:


app_pivot.head()


# Graphically demonstrate what percentage of people completed an application.

# In[220]:


test_groups = ["Test Group A", "Test Group B"]
group_numbers = [250, 325]
plt.figure(figsize=(7,5))
plt.pie(group_numbers, labels=test_groups, autopct = '%0.1f%%') # labels each part & adds a percentage to one decimal place.
plt.title('Who Completed Applications')
plt.axis('equal')
plt.legend(test_groups, loc = 6)
plt.savefig('ab_app_pie_chart.png')
plt.show()


# It looks like more people from Group B turned in an application.  Why might that be?
# 
# We need to know if this difference is statistically significant.
# 
# Choose a hypothesis tests, import it from `scipy` and perform it.  Be sure to note the p-value.
# Is this result significant?

# Since our data is categorized between those who applied and those who didn't, and there is no mean nor standard deviation, and I have two or more samples, I will use a chi-squared test to test between results. 
# My null hypothesis is that there is NO significant difference and my expected p-val would be greater than or equal to 0.05 - else, there is significant difference.

# In[62]:


from scipy.stats import chi2_contingency


# In[64]:


contingency = [[250, 2254],[325, 2500]]
_,pvalue,_,_ = chi2_contingency(contingency)
print pvalue


# In[66]:


#from scipy.stats import binom_test
#pval = binom_test(325, n=2500, p=.13)
#print pval


# In[69]:


if pvalue <= 0.05:
    print "Janet's guess is correct. Those who did not do a fitness test did complete more applications than those who did the fitness test"
else:
    print " Group A and B are the same"


# Since my p-val > 0.05, my null is not rejected and there is no significant difference in Janet's expectations that Group B's application rate would be higher that Group A's rate or maybe there's just not enough data.

# ## Step 4: Who purchases a membership?

# Of those who picked up an application, how many purchased a membership?
# 
# Let's begin by adding a column to `df` called `is_member` which is `Member` if `purchase_date` is not `None`, and `Not Member` otherwise.

# In[34]:


df['is_member'] = df.purchase_date.apply(lambda x: "Member" if pd.notnull(x) else "Not_member")


# In[35]:


df.head()


# Now, let's create a DataFrame called `just_apps` the contains only people who picked up an application.

# In[42]:


just_apps = df[df.is_application == 'Application']


# In[221]:


just_apps.head()


# Great! Now, let's do a `groupby` to find out how many people in `just_apps` are and aren't members from each group.  Follow the same process that we did in Step 4, including pivoting the data.  You should end up with a DataFrame that looks like this:
# 
# |is_member|ab_test_group|Member|Not Member|Total|Percent Purchase|
# |-|-|-|-|-|-|
# |0|A|?|?|?|?|
# |1|B|?|?|?|?|
# 
# Save your final DataFrame as `member_pivot`.

# In[44]:


member_counts = just_apps.groupby(['is_member', 'ab_test_group']).is_application.count().reset_index()


# In[45]:


member_pivot = member_counts.pivot(
    columns='is_member',
    index='ab_test_group',
    values='is_application').reset_index()


# In[48]:


member_pivot['Total'] = member_pivot.apply(lambda row: row.Member + row.Not_member, axis = 1)


# In[180]:


member_pivot['Percent_Purchase'] = member_pivot.apply(lambda row: 1.*row.Member/row.Total, axis = 1)


# In[181]:


member_pivot.head()


# In[ ]:





# It looks like people who took the fitness test were more likely to purchase a membership **if** they picked up an application.  Why might that be?
# 
# Just like before, we need to know if this difference is statistically significant.  Choose a hypothesis tests, import it from `scipy` and perform it.  Be sure to note the p-value.
# Is this result significant?

# My null is that there is no difference in those groups A & B (if filled out an application) who are more likely to purchase a membership.

# In[67]:


contingency = [[200, 250],[250, 325]]
_,pvalue,_,_ = chi2_contingency(contingency)
print pvalue


# In[68]:


#pval = binom_test(50, n=250, p=.8)
#print pval


# Since my p-val is > 0.05, my null is NOT rejected and there is no significant difference.

# Previously, we looked at what percent of people **who picked up applications** purchased memberships.  What we really care about is what percentage of **all visitors** purchased memberships.  Return to `df` and do a `groupby` to find out how many people in `df` are and aren't members from each group.  Follow the same process that we did in Step 4, including pivoting the data.  You should end up with a DataFrame that looks like this:
# 
# |is_member|ab_test_group|Member|Not Member|Total|Percent Purchase|
# |-|-|-|-|-|-|
# |0|A|?|?|?|?|
# |1|B|?|?|?|?|
# 
# Save your final DataFrame as `final_member_pivot`.

# In[55]:


final_member = df.groupby(['is_member', 'ab_test_group']).first_name.count().reset_index()


# In[56]:


final_member_pivot = final_member.pivot(
    columns='is_member',
    index='ab_test_group',
    values='first_name').reset_index()


# In[58]:


final_member_pivot['Total'] = final_member_pivot.apply(lambda row: row.Member + row.Not_member, axis = 1)


# In[60]:


final_member_pivot['Percent_Purchase'] = final_member_pivot.apply(lambda row: 1.*row.Member/row.Total, axis = 1)


# In[61]:


final_member_pivot.head()


# Previously, when we only considered people who had **already picked up an application**, we saw that there was no significant difference in membership between Group A and Group B.
# 
# Now, when we consider all people who **visit MuscleHub**, we see that there might be a significant different in memberships between Group A and Group B.  Perform a significance test and check.

# Since I have to analyze two samples of categorical data, I will use a chi-squared test.

# In[62]:


from scipy.stats import chi2_contingency


# In[63]:


contingency = [[200, 2304],[250, 2250]]
_,pvalue,_,_ = chi2_contingency(contingency)
print pvalue


# Since pvalue < 0.05, there seems to be significant difference between the two groups.

# ## Step 5: Summarize the acquisition funel with a chart

# We'd like to make a bar chart for Janet that shows the difference between Group A (people who were given the fitness test) and Group B (people who were not given the fitness test) at each state of the process:
# - Percent of visitors who apply
# - Percent of applicants who purchase a membership
# - Percent of visitors who purchase a membership
# 
# Create one plot for **each** of the three sets of percentages that you calculated in `app_pivot`, `member_pivot` and `final_member_pivot`.  Each plot should:
# - Label the two bars as `Fitness Test` and `No Fitness Test`
# - Make sure that the y-axis ticks are expressed as percents (i.e., `5%`)
# - Have a title

# In[222]:


groups = ['Grp-A, Fitness Test', 'Grp-B, No Fitness Test']
#app_percentages = app_pivot.percent_with_application.apply(lambda x: str(round(x*100,1)) + ('%'))
app_percentages = app_pivot.percent_with_application

plt.figure(figsize=(7,5))
plt.bar(range(len(groups)),app_percentages)
ax = plt.subplot()
ax.set_yticks([0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14])
ax.set_yticklabels(['0', '2%', '4%', '6%', '8%', '10%', '12%','14%'])
ax.set_xticks(range(len(groups)))
ax.set_xticklabels(groups)
plt.ylabel('Percentages')
plt.title('Application Percentages')
plt.savefig('app_percentages.png')
plt.show()


# In[223]:


groups = ['Grp-A, Fitness Test', 'Grp-B, No Fitness Test']
plt.figure(figsize=(7,5))
#member_percentages = member_pivot.Percent_Purchase.apply(lambda x: str(round(x*100)) + '%')
member_percentages = member_pivot.Percent_Purchase*100
plt.bar(range(len(groups)),member_percentages)
ax = plt.subplot()
ax.set_xticks(range(len(groups)))
ax.set_xticklabels(groups)
ax.set_yticks([0,20,40,60,80,100])
ax.set_yticklabels(['0', '20%', '40%', '60%', '80%', '100%'])
plt.ylabel('Percentages')
plt.title('Purchase Percentages of Applicants')
plt.savefig('pruchase_percentage_applicants.png')
plt.show()


# In[224]:


groups = ['Grp-A, Fitness Test', 'Grp-B, No Fitness Test']
final_member_percentages = final_member_pivot.Percent_Purchase
plt.figure(figsize=(7,5))
plt.bar(range(len(groups)),final_member_percentages)
ax = plt.subplot()
ax.set_xticks(range(len(groups)))
ax.set_xticklabels(groups)
ax.set_yticks([0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12])
ax.set_yticklabels(['0','2%','4%','6%','8%','10%','12%'])
plt.ylabel('Percentages')
plt.title('Purchase Percentages of All Visitors')
plt.savefig('pruchase_percentage_all.png')
plt.show()


# In[ ]:




