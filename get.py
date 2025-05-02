from azure.identity import ManagedIdentityCredential
from azure.mgmt.resource import SubscriptionClient, ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
import os

# ---- Auth with Managed Identity ----
credential = ManagedIdentityCredential()

# ---- Get Subscription ID ----
subscription_client = SubscriptionClient(credential)
subscription = next(subscription_client.subscriptions.list())
subscription_id = subscription.subscription_id
print("✅ Subscription ID:", subscription_id)

# ---- Discover Resource Groups and Web Apps ----
resource_client = ResourceManagementClient(credential, subscription_id)
web_client = WebSiteManagementClient(credential, subscription_id)

print("\n🔍 Searching Web Apps...")
for rg in resource_client.resource_groups.list():
    apps = web_client.web_apps.list_by_resource_group(rg.name)
    for app in apps:
        print(f"Found Web App: {app.name} in RG: {rg.name}")
 
