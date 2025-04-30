from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
import io
import pandas as pd

# SharePoint site and file details
site_url = "https://yourtenant.sharepoint.com/sites/yoursite"
file_url = "/sites/yoursite/Shared Documents/yourfile.xlsx"  # Relative path to file

# Credentials
username = "your.email@domain.com"
password = "your_password"

# Authenticate and connect
ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))

# Download file content into memory
response = ctx.web.get_file_by_server_relative_url(file_url).download()
ctx.execute_query()

# Read the file content into a pandas DataFrame (for Excel)
bytes_file_obj = io.BytesIO(response.content)
df = pd.read_excel(bytes_file_obj)

print(df.head())