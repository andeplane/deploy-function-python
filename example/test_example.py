import pytest
import os
from cognite.experimental import CogniteClient
from handler import handle

print(os.environ)
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
GITHUB_EVENT_NAME = os.environ["GITHUB_EVENT_NAME"]
GITHUB_HEAD_REF   = os.environ["GITHUB_HEAD_REF"]
GITHUB_SHA        = os.environ["GITHUB_SHA"]


@pytest.fixture
def client():
    client = CogniteClient()
    return client

@pytest.fixture
def data():
    return {
      "value": 2.0
    }

@pytest.mark.integration
def test_deployed_function(data, client):
  external_id = f"{GITHUB_REPOSITORY}/example/{GITHUB_HEAD_REF}"
  if GITHUB_EVENT_NAME == "push":
    external_id = f"{GITHUB_REPOSITORY}/example:{GITHUB_SHA}"
  function = client.functions.retrieve(external_id=external_id)
  call = function.call(data=data)
  assert call.status == "Completed"
  assert call.response["result"] == 2.0 * data["value"]

@pytest.mark.unit
def test_handler(data, client):
  result = handle(data, client)
  result == 2.0 * data["value"]