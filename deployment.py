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



from azure.mgmt.web import WebSiteManagementClient
from azure.identity import ManagedIdentityCredential

cred = ManagedIdentityCredential()
subscription_id = "<your-subscription-id>" 
resource_group = ""
webapp = ""

web_client = WebSiteManagementClient(cred, subscription_id)
config = web_client.web_apps.get_configuration(resource_group, webapp)

# Set the FastAPI startup command
config.app_command_line = "gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app"
web_client.web_apps.update_configuration(resource_group, webapp, config)

print("Startup command configured.")

