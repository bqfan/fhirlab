# test_resouce_loader.py
from backend.src.api.resources.resource_loader import Resource
from backend.src.api.models.schemas.references import Reference
from typing import Final

def test_resouce_loader():
    resource = Resource().load()
    reference_model = Reference

    for key, value in resource.references.items():
        assert key in resource.reference_keys
        assert isinstance(reference_model(**value), reference_model)
