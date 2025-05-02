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


from azure.identity import ManagedIdentityCredential
from azure.mgmt.authorization import AuthorizationManagementClient

# Inputs
client_id = "<YOUR-MANAGED-IDENTITY-CLIENT-ID>"
subscription_id = "<YOUR-SUBSCRIPTION-ID>"
resource_group = "<YOUR-RESOURCE-GROUP>"
webapp_name = "<YOUR-WEBAPP-NAME>"

# Authenticate with Managed Identity (User-Assigned)
credential = ManagedIdentityCredential(client_id=client_id)

# Initialize the Authorization client
auth_client = AuthorizationManagementClient(credential, subscription_id)

# Scope to check: the Web App resource
scope = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Web/sites/{webapp_name}"

print(f"Checking role assignments for scope: {scope}")

# List all role assignments for this scope
assignments = auth_client.role_assignments.list_for_scope(scope)

# Print results
has_roles = False
for assignment in assignments:
    if assignment.principal_id:  # optional: filter by principal_id or client_id if needed
        has_roles = True
        print(f"✓ Role Assigned: {assignment.role_definition_id}")
        print(f"  Principal ID: {assignment.principal_id}")
        print(f"  Scope: {assignment.scope}")
        print("-" * 40)

if not has_roles:
    print("⚠️ No roles found for the Managed Identity on this Web App.")


