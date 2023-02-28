import pandas as pd

data_url = 'https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/PERM_Disclosure_Data_FY2023_Q1.xlsx'

# Read the data from the URL
df = pd.read_excel(data_url)

# Print general statistics about the approval rate
print(df['CASE_STATUS'].value_counts(normalize=True))
