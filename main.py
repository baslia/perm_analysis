import pandas as pd

data_url = 'https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/PERM_Disclosure_Data_FY2023_Q2.xlsx'
data_url = 'https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/PERM_Disclosure_Data_FY2022_Q4.xlsx'

# Read the data from the URL
df = pd.read_excel(data_url)

df['DECISION_DATE_month'] = df['DECISION_DATE'].dt.to_period('M')

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
# Plot the distribution of the decision time
import matplotlib.pyplot as plt
import seaborn as sns
# Plot histpgram of cases status per decision month
# plt.hist(df, x='DECISION_DATE_month', hue='CASE_STATUS', multiple='stack', log=True)
# plt.hist([x1, x2], bins=bins, stacked=True,
#                  color=colors, label=names, density=False)
df['DECISION_DATE_month'] = df['DECISION_DATE_month'].astype(str).replace('20', '', regex=True)
sns.histplot(df, x='DECISION_DATE_month', hue='CASE_STATUS', multiple='stack')
plt.xticks(fontsize=8)
plt.show()

#%%
# Keep only the first 7 character of SOC codes
df['PW_SOC_CODE'] = df['PW_SOC_CODE'].str[:7]
df['PW_SOC_CODE_ROOT'] = df['PW_SOC_CODE'].str[:2]

# Get the mean decision time for a given SOC codes
soc_codes = ['15-2031']
soc_codes_root = ['15']
df_soc = df[df['PW_SOC_CODE'].isin(soc_codes)]
df_soc_root = df[df['PW_SOC_CODE_ROOT'].isin(soc_codes_root)]
print('Statistics for SOC code: ', soc_codes)
print(df_soc['CASE_STATUS'].value_counts(normalize=True))
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
#%%
# Build some visualizations
# Denial rate by decision date

# certified rate by decision date month
df_hist = df[['CASE_STATUS', 'DECISION_DATE_month']].groupby('DECISION_DATE_month', as_index=False).value_counts(normalize=True)
print(df_hist)
df_hist_law = df_law[['CASE_STATUS', 'DECISION_DATE_month']].groupby('DECISION_DATE_month', as_index=False).value_counts(normalize=True)
print(df_hist_law)
df_hist_soc_root = df_soc_root[['CASE_STATUS', 'DECISION_DATE_month', 'PW_SKILL_LEVEL']].groupby(['DECISION_DATE_month', 'PW_SKILL_LEVEL'], as_index=False).value_counts(normalize=True)
print(df_hist_soc_root)


def get_certified_rate(df):
    df = pd.DataFrame(df)
    try:
        result = df.value_counts(normalize=True)[1]
    except:
        result = 0
    return result


df_sorted = df.sort_values('DECISION_TIME')
df_sorted['CERTIFIED_INT'] = df_sorted['CASE_STATUS'].map({'Certified': 1, 'Denied': 0})
window = 10
df_sorted['CERTIFIED_RATE'] = df_sorted.rolling(window=window, on='DECISION_TIME', axis=0)['CERTIFIED_INT'].apply(get_certified_rate)
