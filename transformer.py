import time
import os
import sys
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.csv'):
            filename = os.path.basename(event.src_path)
            if not filename.startswith('transformed_'):
                print(f"New CSV detected: {event.src_path}")
                self.process_csv(event.src_path)

    def process_csv(self, filepath):
        filename = os.path.basename(filepath)
        print(f"Processing {filename}...")

        # Load the CSV
        apollo_df = pd.read_csv(filepath)

        # The columns need delete
        columns_to_delete = [
            'Company Name for Emails', 'Company Linkedin Url', 'Email Status', 'Email Confidence',
            'Catch-all Status','Email Last Verified At', 'Seniority', 'Departments', 'Work Direct Phone',
            'Home Phone', 'Mobile Phone', 'Corporate Phone', 'Other Phone', 'Stage', 'Lists', 'Last Contacted',
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
            'SEO Description': 'Description',
            'Person Linkedin Url': 'Linkedin',
            'Country': 'CNTY'
        }, errors='ignore')

        # Clean phone number format
        if 'Phone' in apollo_df.columns:
            apollo_df['Phone'] = apollo_df['Phone'].str.replace("'", "", regex=False)

        # Update content in "Lead Owner" column
        apollo_df['Lead Owner'] = 'beth.kuang@pengxinlogistics.com'

        # Combine "Facebook Url" and "Twitter Url" into a new column "Social Media Account "
        social_media_columns = ['Facebook Url', 'Twitter Url']
        existing_social_columns = [col for col in social_media_columns if col in apollo_df.columns]

        if existing_social_columns:
            apollo_df['Social Media Account '] = apollo_df[existing_social_columns].apply(
                lambda row: next((val for val in row if pd.notna(val)), ''), axis=1)
            apollo_df = apollo_df.drop(columns=existing_social_columns)
        else:
            apollo_df['Social Media Account '] = ''

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
            'First Name', 'Last Name', 'Title', 'Company', 'Email', 'Lead Owner', 'Phone', 'No. of Employees ',
            'Industry', 'Description', 'Linkedin', 'Website', 'Social Media Account ', 'City', 'CNTY', 'Rating',
            'Lead Status', 'Lead Source', 'Email Opt Out', 'Key Follow-up', 'Annual Revenue'
        ]
        # Ensure all columns exist before reordering, and keep any additional columns
        final_columns_order = [col for col in final_columns_order if col in apollo_df.columns]
        apollo_df = apollo_df[final_columns_order + [col for col in apollo_df.columns if col not in final_columns_order]]

        # Save the transformed data
        output_filename = f"transformed_{os.path.splitext(filename)[0][:200]}.csv"
        output_path = os.path.join(os.path.dirname(filepath), output_filename)
        apollo_df.to_csv(output_path, index=False)
        print(f"Transformed CSV saved as {output_filename}")


if __name__ == "__main__":
    # Determine the correct folder to watch
    if getattr(sys, 'frozen', False):
        # The application is frozen (PyInstaller)
        folder_to_watch = os.path.dirname(sys.executable)
    else:
        # Running in a normal Python environment
        folder_to_watch = os.path.dirname(os.path.abspath(__file__))

    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()
    print(f"Watching for CSV files in {folder_to_watch}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()