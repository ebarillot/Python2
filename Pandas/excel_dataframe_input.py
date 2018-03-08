# coding=utf-8

import pandas as pd
import numpy as np


#  pour regler pb de PATH
import os
if os.path.basename(os.getcwd()) != 'Pandas':
    os.chdir('./Pandas')
print(os.getcwd())

# df = pd.read_excel('data/vins.xlsx')
# print(df)
# print(df['flavanoids'])
# print(df['flavanoids'][0])

df = pd.read_excel("data/excel-comp-data.xlsx")
df.head()

# We want to add a total column to show total sales for Jan, Feb and Mar.
# For Excel, I have added the formula sum(G2:I2)
df["total"] = df["Jan"] + df["Feb"] + df["Mar"]
df.head()

# Next, let’s get some totals and other values for each month.
# SUM(G2:G16) in row 17
df["Jan"].sum(), df["Jan"].mean(),df["Jan"].min(),df["Jan"].max()

# sum for the month and total columns
sum_row=df[["Jan","Feb","Mar","total"]].sum()
sum_row

df_sum=pd.DataFrame(data=sum_row).T
df_sum

df_sum=df_sum.reindex(columns=df.columns)
df_sum

df_final=df.append(df_sum,ignore_index=True)
df_final.tail()


# Additional Data Transforms
# For another example, let’s try to add a state abbreviation to the data set.
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
state_to_code = {"VERMONT": "VT", "GEORGIA": "GA", "IOWA": "IA", "Armed Forces Pacific": "AP", "GUAM": "GU",
                 "KANSAS": "KS", "FLORIDA": "FL", "AMERICAN SAMOA": "AS", "NORTH CAROLINA": "NC", "HAWAII": "HI",
                 "NEW YORK": "NY", "CALIFORNIA": "CA", "ALABAMA": "AL", "IDAHO": "ID", "FEDERATED STATES OF MICRONESIA": "FM",
                 "Armed Forces Americas": "AA", "DELAWARE": "DE", "ALASKA": "AK", "ILLINOIS": "IL",
                 "Armed Forces Africa": "AE", "SOUTH DAKOTA": "SD", "CONNECTICUT": "CT", "MONTANA": "MT", "MASSACHUSETTS": "MA",
                 "PUERTO RICO": "PR", "Armed Forces Canada": "AE", "NEW HAMPSHIRE": "NH", "MARYLAND": "MD", "NEW MEXICO": "NM",
                 "MISSISSIPPI": "MS", "TENNESSEE": "TN", "PALAU": "PW", "COLORADO": "CO", "Armed Forces Middle East": "AE",
                 "NEW JERSEY": "NJ", "UTAH": "UT", "MICHIGAN": "MI", "WEST VIRGINIA": "WV", "WASHINGTON": "WA",
                 "MINNESOTA": "MN", "OREGON": "OR", "VIRGINIA": "VA", "VIRGIN ISLANDS": "VI", "MARSHALL ISLANDS": "MH",
                 "WYOMING": "WY", "OHIO": "OH", "SOUTH CAROLINA": "SC", "INDIANA": "IN", "NEVADA": "NV", "LOUISIANA": "LA",
                 "NORTHERN MARIANA ISLANDS": "MP", "NEBRASKA": "NE", "ARIZONA": "AZ", "WISCONSIN": "WI", "NORTH DAKOTA": "ND",
                 "Armed Forces Europe": "AE", "PENNSYLVANIA": "PA", "OKLAHOMA": "OK", "KENTUCKY": "KY", "RHODE ISLAND": "RI",
                 "DISTRICT OF COLUMBIA": "DC", "ARKANSAS": "AR", "MISSOURI": "MO", "TEXAS": "TX", "MAINE": "ME"}


process.extractOne("Minnesotta",choices=state_to_code.keys())
process.extractOne("AlaBAMMazzz",choices=state_to_code.keys(),score_cutoff=80)
process.extractOne("AlaBAMMazzz",choices=state_to_code.keys(),score_cutoff=90)


def convert_state(row):
    # print(row["state"])
    # print(type(row["state"]))
    # print(type(row["state"]) in [unicode,str])
    if type(row["state"]) in [unicode, str]:    # fuzzywuzzy ne supporte pas autre chose, or on a mis des NaN
        # dans la dernière ligne notamment dans la colonne state
        abbrev = process.extractOne(row["state"],choices=state_to_code.keys(),score_cutoff=80)
        if abbrev:
            return state_to_code[abbrev[0]]
    return np.nan


df_final.insert(6, "abbrev", np.nan)
df_final.head()
df_final
# df_final.drop('abbrev', axis=1, inplace=True)
df_final['state']

df_final.apply(convert_state, axis=1)
df_final['abbrev'] = df_final.apply(convert_state, axis=1)
df_final.tail()


df_final['abbrev']


# Subtotals
# Creating a subtotal in pandas, is accomplished using groupby
df_sub=df_final[["abbrev","Jan","Feb","Mar","total"]].groupby('abbrev').sum()
df_sub


# Next, we want to format the data as currency by using applymap to all the values in the data frame
def money(x):
    return "${:,.0f}".format(x)

formatted_df = df_sub.applymap(money)
formatted_df


# The formatting looks good, now we can get the totals like we did earlier.
sum_row=df_sub[["Jan","Feb","Mar","total"]].sum()
sum_row
df_sub_sum=pd.DataFrame(data=sum_row).T
df_sub_sum=df_sub_sum.applymap(money)
df_sub_sum

# Finally, add the total value to the DataFrame
final_table = formatted_df.append(df_sub_sum)
final_table


# You’ll notice that the index is ‘0’ for the total line. We want to change that using rename
final_table = final_table.rename(index={0:"Total"})
final_table
