import requests
from azure.identity import ManagedIdentityCredential

# Set variables
webapp_name = ""
zip_path = "/full/path/to/app.zip"

# Get token via Managed Identity
credential = ManagedIdentityCredential()
token = credential.get_token("https://management.azure.com/.default").token

# Prepare deploy URL (zipdeploy endpoint)
deploy_url = f"https://{webapp_name}.scm.azurewebsites.net/api/zipdeploy"
headers = {"Authorization": f"Bearer {token}"}

# Upload ZIP file
with open(zip_path, "rb") as zip_file:
    print("Uploading ZIP...")
    response = requests.post(deploy_url, headers=headers, data=zip_file)

print("Status:", response.status_code)
print("Response:", response.text)
