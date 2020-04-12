import pytest
import os
from cognite.experimental import CogniteClient

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

def test_handler(client, data):
  external_id = f"{GITHUB_REPOSITORY}/example/{GITHUB_HEAD_REF}"
  if GITHUB_EVENT_NAME == "push":
    external_id = f"{GITHUB_REPOSITORY}/example:{GITHUB_SHA}"
  function = client.functions.retrieve(external_id=external_id)
  call = function.call(data=data)
  assert call.status == "Completed"
  assert call.response["result"] == 2.0 * data["value"]
