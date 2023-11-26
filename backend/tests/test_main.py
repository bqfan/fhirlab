# test_main.py
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.utilities import resource_loader
from backend.src.api.models.schemas.references import Code, Reference, ReferenceRangeItem
from typing import Final, List
import json

REFERENCES: Final[dict] = resource_loader.load_resources("default")
client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "LabTest API"}

def test_references():
    response = client.get("/v1/References")
    response_content_json = json.loads(response.content)
    reference_model = Reference

    assert response.status_code == 200

    for key, value in REFERENCES["Observations"].items():
        validated_reference = resource_loader.validate_data(value, reference_model)
        assert isinstance(validated_reference, Reference)
        assert(is_subset(value, response_content_json[key]))
        
    for key, value in response_content_json.items():
        validated_reference = resource_loader.validate_data(value, reference_model)
        assert isinstance(validated_reference, Reference)

def test_reference_keys():
    response = client.get("/v1/References/keys")
    response_content_json =json.loads(response.content)

    assert isinstance(REFERENCES['ObservationKeys'], List)
    assert isinstance(response_content_json, List)
    assert(REFERENCES['ObservationKeys'] == response_content_json)

def test_reference():
    response = client.get("/v1/References/glucose")
    response_content_json = json.loads(response.content)
    reference_model = Reference

    assert response.status_code == 200

    validated_reference = resource_loader.validate_data(REFERENCES["Observations"]["glucose"], reference_model)
    assert isinstance(validated_reference, reference_model)

    validated_response_content_json = resource_loader.validate_data(response_content_json, reference_model)
    assert isinstance(validated_response_content_json, reference_model)

    assert(is_subset(REFERENCES["Observations"]["glucose"], response_content_json))

def test_reference_range():
    response = client.get("/v1/References/glucose/referenceRange")
    response_content_json = json.loads(response.content)
    reference_range_model = ReferenceRangeItem
    #print(type(response_content_json))
    assert response.status_code == 200

    validated_reference = resource_loader.validate_data(REFERENCES["Observations"]["glucose"]["referenceRange"][0], reference_range_model)
    assert isinstance(validated_reference, reference_range_model)

    validated_response_content_json = resource_loader.validate_data(response_content_json[0], reference_range_model)
    assert isinstance(validated_response_content_json, reference_range_model)

    assert(is_subset(REFERENCES["Observations"]["glucose"]["referenceRange"], response_content_json))

def test_reference_code():
    response = client.get("/v1/References/glucose/code")
    response_content_json = json.loads(response.content)
    reference_code_model = Code
    #print(type(response_content_json))
    assert response.status_code == 200

    validated_reference = resource_loader.validate_data(REFERENCES["Observations"]["glucose"]["code"], reference_code_model)
    assert isinstance(validated_reference, reference_code_model)

    validated_response_content_json = resource_loader.validate_data(response_content_json, reference_code_model)
    assert isinstance(validated_response_content_json, reference_code_model)

    assert(is_subset(REFERENCES["Observations"]["glucose"]["code"], response_content_json))

def is_subset(subset, superset):
    match subset:
        case dict(_): return all(key in superset and is_subset(val, superset[key]) for key, val in subset.items())
        case list(_) | set(_): return all(any(is_subset(subitem, superitem) for superitem in superset) for subitem in subset)
        # assume that subset is a plain value if none of the above match
        case _: return subset == superset




