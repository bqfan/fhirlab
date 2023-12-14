# test_main.py
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.api.resources.resource_loader import Resource
from backend.src.api.models.schemas.references import Bundle, Code, Reference, ReferenceRangeItem
from typing import List
import json

resource = Resource().load()
client = TestClient(app)


def test_references():
    response = client.get("/default/References")
    response_content_json = json.loads(response.content)

    assert response.status_code == 200

    for key, value in resource.references.items():
        assert key in resource.references.keys()
        assert isinstance(Reference(**value), Reference)
        
    for key, value in response_content_json.items():
        assert key in resource.references.keys()
        assert isinstance(Reference(**value), Reference)

def test_reference_keys():
    response = client.get("/default/References/keys")
    response_content_json =json.loads(response.content)

    assert isinstance(resource.references.keys(), type({}.keys()))
    assert isinstance(response_content_json, List)
    assert(list(resource.references.keys()) == response_content_json)

def test_reference():
    response = client.get("/default/References/glucose")
    response_content_json = json.loads(response.content)

    assert response.status_code == 200
    assert isinstance(Reference(**resource.references['glucose']), Reference)
    assert isinstance(Reference(**response_content_json), Reference)
    assert(is_subset(resource.references['glucose'], response_content_json))

def test_reference_range():
    response = client.get("/default/References/glucose/referenceRange")
    response_content_json = json.loads(response.content)

    assert response.status_code == 200
    assert isinstance(ReferenceRangeItem(**resource.references['glucose']['referenceRange'][0]), ReferenceRangeItem)
    assert isinstance(ReferenceRangeItem(**response_content_json[0]), ReferenceRangeItem)
    assert(is_subset(resource.references['glucose']['referenceRange'], response_content_json))

def test_reference_code():
    response = client.get("/default/References/glucose/code")
    response_content_json = json.loads(response.content)

    assert response.status_code == 200
    assert isinstance(Code(**resource.references['glucose']['code']), Code)
    assert isinstance(Code(**response_content_json), Code)

    assert(is_subset(resource.references['glucose']['code'], response_content_json))

def test_bundles():
    response = client.get("/default/Bundles")
    response_content_json = json.loads(response.content)

    assert response.status_code == 200

    for key, value in resource.bundles.items():
        assert key in resource.bundles.keys()
        assert isinstance(Bundle(**value), Bundle)
        
    for key, value in response_content_json.items():
        assert key in resource.bundles.keys()
        assert isinstance(Bundle(**value), Bundle)

def test_bundle_keys():
    response = client.get("/default/Bundles/keys")
    response_content_json =json.loads(response.content)

    assert response.status_code == 200
    assert isinstance(resource.bundles.keys(), type({}.keys()))
    assert isinstance(response_content_json, List)
    assert(list(resource.bundles.keys()) == response_content_json)

def test_acronyms():
    response = client.get("/default/Acronyms")
    response_content_json =json.loads(response.content)

    assert response.status_code == 200
    assert isinstance(resource.acronyms, dict)
    assert isinstance(response_content_json, dict)
    assert(resource.acronyms == response_content_json)

def test_acronym_by_key():
    acronym_response = client.get("/default/Acronyms/HDL")
    acronym_response_content_json = json.loads(acronym_response.content)
    assert acronym_response.status_code == 200

    reference_response = client.get(f"/default/References/{resource.acronyms['HDL']['reference']}")
    reference_response_content_json = json.loads(reference_response.content)
    assert reference_response.status_code == 200

    assert isinstance(resource.acronyms['HDL']['reference'], str)
    assert isinstance(Reference(**acronym_response_content_json), Reference)
    assert isinstance(Reference(**reference_response_content_json), Reference)
    assert(acronym_response_content_json == reference_response_content_json)

def is_subset(subset, superset):
    match subset:
        case dict(_): return all(key in superset and is_subset(val, superset[key]) for key, val in subset.items())
        case list(_) | set(_): return all(any(is_subset(subitem, superitem) for superitem in superset) for subitem in subset)
        # assume that subset is a plain value if none of the above match
        case _: return subset == superset
