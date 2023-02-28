import pandas as pd

data_url = 'https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/PERM_Disclosure_Data_FY2023_Q1.xlsx'

# Read the data from the URL
df = pd.read_excel(data_url)

# Add the date decision time column
df['DECISION_TIME'] = df['DECISION_DATE'] - df['RECEIVED_DATE']

# Print general statistics about the approval rate
print(df['CASE_STATUS'].value_counts(normalize=True))

# Remove withdrawn cases
df = df[df['CASE_STATUS'] != 'Withdrawn']

# Concert the decision time to days
df['DECISION_TIME'] = df['DECISION_TIME'].dt.days

# Get mean decision time for each case status
print(df.groupby('CASE_STATUS')['DECISION_TIME'].mean())

# Get the mean decision time for all cases
print(df['DECISION_TIME'].mean())
#%%
# Keep only the first 7 character of SOC codes
df['PW_SOC_CODE'] = df['PW_SOC_CODE'].str[:7]

# Get the mean decision time for a given SOC codes
soc_codes = ['15-2031']
df_soc = df[df['PW_SOC_CODE'].isin(soc_codes)]
print(df_soc.groupby('CASE_STATUS')['DECISION_TIME'].mean())

#%%
# Get the mean decision time for a given law firm
law_firms = 'fragomen'

df_law = df[~df['AGENT_ATTORNEY_FIRM_NAME'].isna()]
df_law['AGENT_ATTORNEY_FIRM_NAME'] = df_law['AGENT_ATTORNEY_FIRM_NAME'].astype(str)
df_law['AGENT_ATTORNEY_FIRM_NAME'] = df_law['AGENT_ATTORNEY_FIRM_NAME'].str.lower()
df_law = df_law[df_law['AGENT_ATTORNEY_FIRM_NAME'].str.contains(law_firms)]
print(df_law['CASE_STATUS'].value_counts(normalize=True))
print(df_law['DECISION_TIME'].mean())

#%%
# Get the approval rate by waiting time
days_pending = 280
df_pending = df[(df['DECISION_TIME'] >= days_pending - 5) & (df['DECISION_TIME'] <= days_pending + 5)]
print(df_pending['CASE_STATUS'].value_counts(normalize=True))