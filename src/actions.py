import os
import time
from tempfile import TemporaryDirectory
# from typing import Any, Dict, List, Optional, Union
from zipfile import ZipFile

CDF_FUNCTION_CREDENTIALS = os.getenv("INPUT_CDF_FUNCTION_CREDENTIALS")
FUNCTION_PATH = os.getenv("INPUT_FUNCTION_PATH")
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
GITHUB_SHA = os.environ["GITHUB_SHA"][:7]
GITHUB_HEAD_REF = os.environ["GITHUB_HEAD_REF"]

class FunctionDeployTimeout(Exception):
    pass

def zip_and_upload_folder(functions_api, folder, name) -> int:
  print(f"Uploading source code from {folder} to {name}", flush=True)
  current_dir = os.getcwd()
  os.chdir(folder)

  try:
      with TemporaryDirectory() as tmpdir:
          zip_path = os.path.join(tmpdir, "function.zip")
          zf = ZipFile(zip_path, "w")
          for root, dirs, files in os.walk("."):
              zf.write(root)
              for filename in files:
                  zf.write(os.path.join(root, filename))
          zf.close()

          file = functions_api._cognite_client.files.upload(zip_path, name=name)

      return file.id

  finally:
      os.chdir(current_dir)

def await_function_deployment(functions_api, external_id, wait_time_seconds):
  t_end = time.time() + wait_time_seconds
  while time.time() < t_end:
    function = functions_api.retrieve(external_id=external_id)
    if function.status == "Ready":
      return True
    if function.status == "Failed":
      return False
    time.sleep(5.0)

  return False

def try_delete_function(functions_api, external_id):
  try:
    function = functions_api.retrieve(external_id=external_id)
    print(f"Found existing function {external_id}. Deleting ...", flush=True)
    functions_api.delete(external_id=external_id)
    print(f"Did delete function {external_id}.", flush=True)
  except:
    print(f"Did not delete function {external_id}.", flush=True)

def create_and_wait_for_deployment(functions_api, name, external_id, file_id):
  print(f"Will create function {external_id}", flush=True)
  api_key = CDF_FUNCTION_CREDENTIALS
  function = functions_api.create(name=name, external_id=external_id, file_id=file_id, api_key=api_key)
  print(f"Created function {external_id}. Waiting for deployment ...", flush=True)
  wait_time_seconds = 300 # 5 minutes
  deployed = await_function_deployment(functions_api, function.external_id, wait_time_seconds)
  if not deployed:
    print(f"Function {external_id} did not deploy within {wait_time_seconds} seconds.", flush=True)
    raise FunctionDeployTimeout(f"Function {external_id} did not deploy within {wait_time_seconds} seconds.")
  print(f"Function {external_id} is deployed.", flush=True)
  return function

def handle_push(functions_api):
  function_name = f"{GITHUB_REPOSITORY}/{FUNCTION_PATH}:{GITHUB_SHA}"
  external_id = function_name
  file_name = function_name.replace("/", "_")+".zip" # / not allowed in file names
  
  # Upload file
  file_id = zip_and_upload_folder(functions_api, FUNCTION_PATH, file_name)
  
  try_delete_function(functions_api, external_id) # Delete old one first
  create_and_wait_for_deployment(functions_api, function_name, external_id, file_id) # Upload new
  
  # Delete :latest and recreate immediately. This will hopefully be fast because file_id is cached
  function_name_latest = f"{GITHUB_REPOSITORY}/{FUNCTION_PATH}:latest"
  external_id_latest = function_name_latest
  try_delete_function(functions_api, external_id_latest)
  function = create_and_wait_for_deployment(functions_api, function_name_latest, external_id_latest, file_id)
  try_delete_function(functions_api, external_id)

  print(f"Successfully created and deployed function {external_id} with id {function.id}", flush=True)
  
def handle_pull_request(functions_api):
  function_name = f"{GITHUB_REPOSITORY}/{FUNCTION_PATH}/{GITHUB_HEAD_REF}"
  external_id = function_name
  try_delete_function(functions_api, external_id)
  if os.getenv("DELETE_PR_FUNCTION"):
    return
  
  # Upload file
  file_name = function_name.replace("/", "_")+".zip" # / not allowed in file names
  file_id = zip_and_upload_folder(functions_api, FUNCTION_PATH, file_name)
  function = create_and_wait_for_deployment(functions_api, function_name, external_id, file_id)

  print(f"Successfully created and deployed PR function {external_id} with id {function.id}", flush=True)
  