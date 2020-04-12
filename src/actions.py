import os
from tempfile import TemporaryDirectory
# from typing import Any, Dict, List, Optional, Union
from zipfile import ZipFile

CDF_CREDENTIALS = os.getenv("INPUT_CDF_CREDENTIALS")
FUNCTION_PATH = os.getenv("INPUT_FUNCTION_PATH")
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
GITHUB_SHA = os.environ["GITHUB_SHA"][:7]

def zip_and_upload_folder(functions_api, folder, name) -> int:
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

          file = functions_api._cognite_client.files.upload(zip_path, name=f"{name}.zip")

      return file.id

  finally:
      os.chdir(current_dir)

def handle_push(client):
  function_name = f"{GITHUB_REPOSITORY}:{GITHUB_SHA}"
  external_id = function_name
  file_name = function_name.replace("/", "_")
  # Upload file
  file_id = zip_and_upload_folder(client.functions, FUNCTION_PATH, file_name+".zip")
  
  function = client.functions.create(name=function_name, external_id=external_id, file_id=file_id, api_key=CDF_CREDENTIALS)
  print(f"Successfully created function {external_id} with id {function.id}")
  
def handle_pull_request(client):
  functions = client.functions
  pass