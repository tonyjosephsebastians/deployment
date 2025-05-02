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


from azure.identity import ManagedIdentityCredential
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.web.models import SiteConfigResource

# Variables
subscription_id = "your-subscription-id"
resource_group = ""
webapp_name = ""
zip_path = ""

# Authenticate
credential = ManagedIdentityCredential()
client = WebSiteManagementClient(credential, subscription_id)

# Step 1: Update startup command (only for Linux Web Apps)
# Make sure you have gunicorn installed in your requirements.txt and entrypoint is main:app
site_config = SiteConfigResource(app_command_line="gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app")
client.web_apps.update_configuration(resource_group, webapp_name, site_config)

print("Updated startup command to use gunicorn.")

# Step 2: Deploy ZIP file
with open(zip_path, "rb") as f:
    zip_content = f.read()

deployment = client.web_apps.begin_create_zip_deployment(
    resource_group_name=resource_group,
    name=webapp_name,
    zip_file=zip_content
)

print("Deployment started...")
deployment.wait()
print("Deployment completed.")


