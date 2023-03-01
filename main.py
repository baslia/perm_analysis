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
# Get statistics about the decision time
print(df['DECISION_TIME'].describe(percentiles=[0.25, 0.5, 0.75, 0.80, 0.85, 0.9, 0.95, 0.99]))

#%%
# Keep only the first 7 character of SOC codes
df['PW_SOC_CODE'] = df['PW_SOC_CODE'].str[:7]

# Get the mean decision time for a given SOC codes
soc_codes = ['15-2031']
df_soc = df[df['PW_SOC_CODE'].isin(soc_codes)]
print('Statistics for SOC code: ', soc_codes)
print(df_soc.groupby('CASE_STATUS')['DECISION_TIME'].mean())
print(df_soc['DECISION_TIME'].describe(percentiles=[0.25, 0.5, 0.75, 0.80, 0.85, 0.9, 0.95, 0.99]))

#%%
# Get the mean decision time for a given law firm
law_firms = 'fragomen'

df_law = df[~df['AGENT_ATTORNEY_FIRM_NAME'].isna()]
df_law['AGENT_ATTORNEY_FIRM_NAME'] = df_law['AGENT_ATTORNEY_FIRM_NAME'].astype(str)
df_law['AGENT_ATTORNEY_FIRM_NAME'] = df_law['AGENT_ATTORNEY_FIRM_NAME'].str.lower()
df_law = df_law[df_law['AGENT_ATTORNEY_FIRM_NAME'].str.contains(law_firms)]
print(f'Statistics for law firm: {law_firms}')
print(df_law['CASE_STATUS'].value_counts(normalize=True))
print(df_law['DECISION_TIME'].mean())
print(df_law['DECISION_TIME'].describe(percentiles=[0.25, 0.5, 0.75, 0.80, 0.85, 0.9, 0.95, 0.99]))
#%%
# Get the approval rate by waiting time
priority_date = pd.to_datetime('2022-05-19')
# get the number of days since the priority date and now
days_pending = (pd.to_datetime('today') - priority_date).days
df_pending = df[(df['DECISION_TIME'] >= days_pending - 5) & (df['DECISION_TIME'] <= days_pending + 5)]
print(df_pending['CASE_STATUS'].value_counts(normalize=True))
# Get decile of the decision time
print('Decile of the decision time in total: ')
print(df['DECISION_TIME'].lt(days_pending).sum()/df.shape[0])
print(f'Decile of the decision time for soc {soc_codes[0]}: ')
print(df_soc['DECISION_TIME'].lt(days_pending).sum()/df_soc.shape[0])
print(f'Decile of the decision time for lawyer firm {law_firms}: ')
print(df_law['DECISION_TIME'].lt(days_pending).sum()/df_law.shape[0])

#%%
# Denial analysis
df_denial = df[df['CASE_STATUS'] == 'Denied']
df_denial['PW_SOC_TITLE'] = df_denial['PW_SOC_TITLE'].str.lower()
df_denial['EMPLOYER_NAME'] = df_denial['EMPLOYER_NAME'].str.lower()
print('Number of denied cases: ')
print(df_denial.shape[0])
# Top SOC TITLE for denied cases
print(df_denial['PW_SOC_TITLE'].value_counts().head(20))
print(df_denial['PW_SOC_TITLE'].value_counts().tail(20))
# Top Employer count for denied cases
print(df_denial['EMPLOYER_NAME'].value_counts().head(10))
# Top education level for denied cases
print(df_denial['MINIMUM_EDUCATION'].value_counts().head(10))
# Top field of studies for denied cases
print(df_denial['MAJOR_FIELD_OF_STUDY'].value_counts().head(10))
# Top PW skill levels for denied cases
print(df_denial['PW_SKILL_LEVEL'].value_counts(normalize=True))
print(df['PW_SKILL_LEVEL'].value_counts(normalize=True))
# Foreign worker education level
print(df_denial.iloc[:, 130].value_counts(normalize=True))

