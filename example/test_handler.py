import pytest
import os
from cognite.experimental import CogniteClient

GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
FUNCTION_PATH     = os.getenv("INPUT_FUNCTION_PATH")
GITHUB_HEAD_REF   = os.environ["GITHUB_HEAD_REF"]

@pytest.fixture
def client():
    client = CogniteClient(api_key=os.environ["INPUT_CDF_CREDENTIALS"], project=os.environ["INPUT_CDF_PROJECT"], client_name="deploy-function-action")
    return client

@pytest.fixture
def data():
    return {
      "value": 2.0
    }

def test_handler(client, data):
  external_id = f"{GITHUB_REPOSITORY}/{FUNCTION_PATH}/{GITHUB_HEAD_REF}"
  function = client.functions.retrieve(external_id=external_id)
  response = function.call(data=data)
  print(response)
