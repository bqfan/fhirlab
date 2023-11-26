# test_resouce_loader.py
from backend.src.utilities import resource_loader
from backend.src.api.models.schemas.references import Reference
from typing import Final

def test_resouce_loader():
    REFERENCES: Final[dict] = resource_loader.load_resources("default")

    for key, value in REFERENCES["Observations"].items():
        reference_model = Reference
        validated_reference = resource_loader.validate_data(value, reference_model)
        assert isinstance(validated_reference, Reference)
