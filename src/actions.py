import os

CDF_CREDENTIALS = os.getenv("INPUT_CDF_CREDENTIALS")
FUNCTION_PATH = os.getenv("INPUT_FUNCTION_PATH")
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
GITHUB_SHA = os.environ["GITHUB_SHA"]

def handle_push(client):
  function_name = f"{GITHUB_REPOSITORY}:{GITHUB_SHA}"
  external_id = function_name;
  function = client.functions.create(name=function_name, external_id=external_id, folder=FUNCTION_PATH, api_key=CDF_CREDENTIALS)
  print(f"Successfully created function {external_id} with id {function.id}")
  
def handle_pull_request(client):
  functions = client.functions
  pass