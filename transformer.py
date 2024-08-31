import pandas as pd

# Load the Apollo CSV
apollo_df = pd.read_csv('apollo-contacts-export.csv')

# Delete unnecessary columns
columns_to_delete = [
    'Company Name for Emails', 'Company Linkedin Url', 'Email Status', 'Email Confidence', 'Catch-all Status',
    'Email Last Verified At', 'Seniority', 'Departments', 'Work Direct Phone', 'Home Phone',
    'Mobile Phone', 'Corporate Phone', 'Other Phone', 'Stage', 'Lists', 'Last Contacted',
    'Account Owner', 'Keywords', 'State', 'Company Address', 'Company City', 'Company State',
    'Company Country', 'Company Phone', 'Technologies', 'Total Funding', 'Latest Funding',
    'Latest Funding Amount', 'Last Raised At', 'Email Sent', 'Email Open', 'Email Bounced',
    'Replied', 'Demoed', 'Number of Retail Locations', 'Apollo Contact Id', 'Apollo Account Id',
    'User Managed', 'Primary Intent Topic', 'Primary Intent Score', 'Secondary Intent Topic',
    'Secondary Intent Score'
]
apollo_df = apollo_df.drop(columns=columns_to_delete, errors='ignore')

# Rename columns and update the content as specified
apollo_df = apollo_df.rename(columns={
    'Contact Owner': 'Lead Owner',
    'First Phone': 'Phone',
    '# Employees': 'No. of Employees ',
    'Seo Description': 'Description',
    'Person Linkedin Url': 'Linkedin',
    'Country': 'CNTY'
}, errors='ignore')

# Update content in "Lead Owner" column
apollo_df['Lead Owner'] = 'beth.kuang@pengxinlogistics.com'

# Combine "Facebook Url" and "Twitter Url" into a new column "Social Media Account "
apollo_df['Social Media Account '] = apollo_df['Facebook Url'].combine_first(apollo_df['Twitter Url'])
apollo_df = apollo_df.drop(columns=['Facebook Url', 'Twitter Url'], errors='ignore')

# Add new columns with specified default content
apollo_df['Rating'] = 'To be future identified'
apollo_df['Lead Status'] = 'Contact in Future'
apollo_df['Lead Source'] = 'Apollo'

# Add new columns with blank content
columns_to_add_blank = ['Email Opt Out', 'Key Follow-up']
for col in columns_to_add_blank:
    apollo_df[col] = ''

# Reorder columns to match the final desired order, preserving existing columns
final_columns_order = [
    'First Name', 'Last Name', 'Title', 'Company', 'Email', 'Lead Owner	Phone', 'No. of Employees',
    'Industry',	'Description', 'Linkedin', 'Website', 'Social Media Account', 'City', 'CNTY', 'Rating',
    'Lead Status', 'Lead Source', 'Email Opt Out', 'Key Follow-up', 'Annual Revenue'
]
# Ensure all columns exist before reordering, and keep any additional columns
final_columns_order = [col for col in final_columns_order if col in apollo_df.columns]
apollo_df = apollo_df[final_columns_order + [col for col in apollo_df.columns if col not in final_columns_order]]

# Save the transformed data to a new CSV
apollo_df.to_csv('transformed_apollo.csv', index=False)
