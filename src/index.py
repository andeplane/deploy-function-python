# from cognite.client import CogniteClient
from cognite.experimental import CogniteClient
import os

CDF_PROJECT = os.getenv("INPUT_CDF_PROJECT")
CDF_CREDENTIALS = os.getenv("INPUT_CDF_CREDENTIALS")
CDF_BASE_URL = os.getenv("INPUT_CDF_BASE_URL", "https://api.cognitedata.com")

if not CDF_PROJECT:
  print("Missing input cdf_project")
  exit()

if not CDF_CREDENTIALS:
  print("Missing input cdf_credentials")
  exit() 

client = CogniteClient(api_key=CDF_CREDENTIALS, project=CDF_PROJECT, base_url=CDF_BASE_URL)
print(len(client.assets.list())
