from dotenv import load_dotenv
import os
from sharepoint_online import SharePoint

# Load environment variables (recommended for credentials and IDs)
load_dotenv()

AUTH_URL = os.environ.get("AUTH_URL")
CLIENT_ID = os.environ.get("CLIENT_ID")
TOKEN_URL = os.environ.get("TOKEN_URL")
SITE_ID = os.environ.get("SITE_ID")
LIST_ID = os.environ.get("LIST_ID")

# Initialize SharePoint connection
sp = SharePoint(CLIENT_ID, AUTH_URL, TOKEN_URL, SITE_ID)

# Read SharePoint List into a pandas DataFrame
df = sp.get_list_df(LIST_ID, expand="fields")

# Example: Update the 'Title' column
df["Title"] = "New Title"

# Write changes back to SharePoint
sp.update_rows(LIST_ID, df)

# Print the updated DataFrame
print(sp.get_list_df(LIST_ID, expand="fields"))
