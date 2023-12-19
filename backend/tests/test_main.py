# test_main.py
from fastapi import status
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.api.resources.resource_loader import Resource
from backend.src.api.models.schemas.references import Bundle, Code, Reference, ReferenceRangeItem
from typing import Final, List
import json

resource = Resource().load()
client = TestClient(app)

def test_references_post():
    data = {
        "resourceType": "Observation",
        "effectiveDateTime": "2023-12-17T09:30:10+01:00",
        "id": "123456789",
        "identifier": [
            {
            "system": "https:/helthq.dev/identifiers/observations",
            "use": "official",
            "value": "1234"
            }
        ],
        "issued": "2023-12-17T15:30:10+01:00",
        "performer": [
            {
            "reference": "Practitioner/example"
            }
        ],
        "status": "final",
        "subject": {
            "reference": "Patient/example"
        },
        "valueQuantity": {
            "code": "mmol/L",
            "system": "http://unitsofmeasure.org",
            "unit": "mmol/l",
            "value": 6.3
        }
    }

    post_response = client.post(
        "/Observation/_references/glucose",
        content = json.dumps(data),
        headers = {"Content-Type": "application/json"},
    )

    assert(post_response.status_code == status.HTTP_201_CREATED)

    reference_response = client.get("/Observation/_references/glucose")

    post_response_json = json.loads(post_response.content)
    reference_response_json = json.loads(reference_response.content)
    assert(is_subset(reference_response_json, post_response_json))
    assert(is_subset(data, json.loads(post_response.content)))
    assert(isinstance(post_response_json["text"], dict))
    assert(post_response_json["text"]["status"] == "generated")
    assert(isinstance(post_response_json["text"]["div"], str))
    assert isinstance(post_response_json["interpretation"], List)
    assert isinstance(post_response_json["interpretation"][0]["coding"], List)
    assert(list(post_response_json["interpretation"][0]["coding"][0].keys()) == ['system', 'code', 'display'])

def test_references():
    response = client.get("/Observation/_references")
    response_content_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK

    for key, value in resource.references.items():
        assert key in resource.reference_keys
        assert isinstance(Reference(**value), Reference)
        
    for key, value in response_content_json.items():
        assert key in resource.reference_keys
        assert isinstance(Reference(**value), Reference)

def test_reference_keys():
    response = client.get("/Observation/_references/_keys")
    response_content_json =json.loads(response.content)

    assert isinstance(resource.reference_keys, List)
    assert isinstance(response_content_json, List)
    assert(resource.reference_keys == response_content_json)

def test_acronyms():
    response = client.get("/Observation/_references/_acronyms")
    response_content_json =json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(resource.acronyms, dict)
    assert isinstance(response_content_json, dict)
    assert(resource.acronyms == response_content_json)

def test_acronym_by_key():
    acronym_response = client.get("/Observation/_references/_acronyms/HDL")
    acronym_response_content_json = json.loads(acronym_response.content)
    assert acronym_response.status_code == status.HTTP_200_OK

    reference_response = client.get(f"/Observation/_references/{resource.acronyms['HDL']}")
    reference_response_content_json = json.loads(reference_response.content)
    assert reference_response.status_code == status.HTTP_200_OK

    assert isinstance(resource.acronyms['HDL'], str)
    assert isinstance(Reference(**acronym_response_content_json), Reference)
    assert isinstance(Reference(**reference_response_content_json), Reference)
    assert(acronym_response_content_json == reference_response_content_json)

def test_reference():
    response = client.get("/Observation/_references/glucose")
    response_content_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(Reference(**resource.references['glucose']), Reference)
    assert isinstance(Reference(**response_content_json), Reference)
    assert(is_subset(resource.references['glucose'], response_content_json))

def test_reference_range():
    response = client.get("/Observation/_references/glucose/_referenceRange")
    response_content_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(ReferenceRangeItem(**resource.references['glucose']['referenceRange'][0]), ReferenceRangeItem)
    assert isinstance(ReferenceRangeItem(**response_content_json[0]), ReferenceRangeItem)
    assert(is_subset(resource.references['glucose']['referenceRange'], response_content_json))

def test_reference_code():
    response = client.get("/Observation/_references/glucose/_code")
    response_content_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(Code(**resource.references['glucose']['code']), Code)
    assert isinstance(Code(**response_content_json), Code)

    assert(is_subset(resource.references['glucose']['code'], response_content_json))

def test_bundles():
    response = client.get("/Bundles/_references")
    response_content_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK

    for key, value in resource.bundles.items():
        assert key in resource.bundle_keys
        assert isinstance(Bundle(**value), Bundle)
        
    for key, value in response_content_json.items():
        assert key in resource.bundle_keys
        assert isinstance(Bundle(**value), Bundle)

def test_bundle_keys():
    response = client.get("/Bundles/_keys")
    response_content_json =json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(resource.bundle_keys, List)
    assert isinstance(response_content_json, List)
    assert(resource.bundle_keys == response_content_json)

def is_subset(subset, superset):
    match subset:
        case dict(_): return all(key in superset and is_subset(val, superset[key]) for key, val in subset.items())
        case list(_) | set(_): return all(any(is_subset(subitem, superitem) for superitem in superset) for subitem in subset)
        # assume that subset is a plain value if none of the above match
        case _: return subset == superset
