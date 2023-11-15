# test_reference_loader.py
import pytest
from app.src.utilities import reference_loader
from app.src.api.models.schemas.references import Reference
from typing import Final, List

def test_reference_loader():
    REFERENCES: Final[dict] = reference_loader.load_references("default")

    for key, value in REFERENCES["Observations"].items():
        reference_model = Reference
        validated_reference = reference_loader.validate_data(value, reference_model)
        assert isinstance(validated_reference, Reference)
