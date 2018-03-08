# coding=utf-8

# http://pbpython.com/excel-diff-pandas.html

# As part of my continued exploration of pandas, I am going to walk through a real world example of how to use pandas
# to automate a process that could be very difficult to do in Excel. My business problem is that I have two Excel files
# that are structured similarly but have different data and I would like to easily understand what has changed between
# the two files.
#
# Basically, I want an Excel diff tool.


import pandas as pd
import numpy as np

#  pour regler pb de PATH
import os
if os.path.basename(os.getcwd()) != 'Pandas':
    os.chdir('./Pandas')
print(os.getcwd())


# Define the diff function to show the changes in each field
def report_diff(x):
    return x[0] if x[0] == x[1] else '{} ---> {}'.format(*x)

# Read in the two files but call the data old and new and create columns to track
old = pd.read_excel('data/sample-address-old.xlsx', 'Sheet1', na_values=['NA'])
new = pd.read_excel('data/sample-address-new.xlsx', 'Sheet1', na_values=['NA'])
old['version'] = "old"
new['version'] = "new"
old.head()

#Join all the data together and ignore indexes so it all gets added
full_set = pd.concat([old,new],ignore_index=True)

# Let's see what changes in the main columns we care about
# changes = full_set.drop_duplicates(subset=["account number","name","street","city","state","postal code"],take_last=True)
changes = full_set.drop_duplicates(subset=["account number","name","street","city","state","postal code"])

#We want to know where the duplicate account numbers are, that means there have been changes
dupe_accts = changes.set_index('account number').index.get_duplicates()

#Get all the duplicate rows
dupes = changes[changes["account number"].isin(dupe_accts)]

#Pull out the old and new data into separate dataframes
change_new = dupes[(dupes["version"] == "new")]
change_old = dupes[(dupes["version"] == "old")]

#Drop the temp columns - we don't need them now
change_new = change_new.drop(['version'], axis=1)
change_old = change_old.drop(['version'], axis=1)

#Index on the account numbers
change_new.set_index('account number',inplace=True)
change_old.set_index('account number',inplace=True)

#Now we can diff because we have two data sets of the same size with the same index
diff_panel = pd.Panel(dict(df1=change_old,df2=change_new))
diff_output = diff_panel.apply(report_diff, axis=0)

#Diff'ing is done, we need to get a list of removed items

#Flag all duplicated account numbers
# voir http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
#  pour explication syntaxe
changes.loc[:,'duplicate'] = pd.Series(changes.loc[:,'account number'].isin(dupe_accts))


#Identify non-duplicated items that are in the old version and did not show in the new version
removed_accounts = changes[(changes["duplicate"] == False) & (changes["version"] == "old")]

# We have the old and diff, we need to figure out which ones are new

#Drop duplicates but keep the first item instead of the last
new_account_set = full_set.drop_duplicates(subset=["account number","name","street","city","state","postal code"],take_last=False)

#Identify dupes in this new dataframe
new_account_set['duplicate'] = new_account_set["account number"].isin(dupe_accts)

#Identify added accounts
added_accounts = new_account_set[(new_account_set["duplicate"] == False) & (new_account_set["version"] == "new")]

#Save the changes to excel but only include the columns we care about
writer = pd.ExcelWriter("my-diff-2.xlsx")
diff_output.to_excel(writer,"changed")
removed_accounts.to_excel(writer,"removed",index=False,columns=["account number",
                                         "name","street","city","state","postal code"])
added_accounts.to_excel(writer,"added",index=False,columns=["account number",
                                         "name","street","city","state","postal code"])
writer.save()
