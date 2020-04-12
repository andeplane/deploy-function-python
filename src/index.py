from cognite.experimental import CogniteClient
import os
from actions import handle_pull_request, handle_push

CDF_PROJECT = os.getenv("INPUT_CDF_PROJECT")
CDF_CREDENTIALS = os.getenv("INPUT_CDF_CREDENTIALS")
CDF_BASE_URL = os.getenv("INPUT_CDF_BASE_URL", "https://api.cognitedata.com")
FUNCTIONS = os.getenv("INPUT_FUNCTIONS")
GITHUB_EVENT_NAME = os.environ["GITHUB_EVENT_NAME"]
GITHUB_REF = os.environ["GITHUB_REF"]
print("FUNCTION_PATH: ", FUNCTIONS)

if not (CDF_PROJECT and CDF_CREDENTIALS and FUNCTIONS):
  print("Missing one of inputs cdf_project, cdf_credentials, functions", flush=True)
  exit()

print(f"Handling event {GITHUB_EVENT_NAME} on {GITHUB_REF}", flush=True)

client = CogniteClient(api_key=CDF_CREDENTIALS, project=CDF_PROJECT, base_url=CDF_BASE_URL)

user = client.login.status()
print(f"Logged in as user {user}", flush=True)
if GITHUB_EVENT_NAME == "push":
  handle_push(client.functions)
elif GITHUB_EVENT_NAME == "pull_request":
  handle_pull_request(client.functions)

# print(len(client.assets.list()))
