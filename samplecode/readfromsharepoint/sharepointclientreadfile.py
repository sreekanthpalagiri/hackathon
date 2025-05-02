from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential

site_url = "https://yourtenant.sharepoint.com/sites/yoursite"
file_url = "/sites/yoursite/Shared Documents/yourfile.pdf"
username = "your.email@domain.com"
password = "your_password"

ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))
response = ctx.web.get_file_by_server_relative_url(file_url).download()
ctx.execute_query()

# Save to local file
with open("downloaded_file.pdf", "wb") as f:
    f.write(response.content)
print("PDF downloaded successfully!")
