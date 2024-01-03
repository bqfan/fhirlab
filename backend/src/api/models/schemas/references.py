from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class CodingItem(BaseModel):
    code: str
    display: str
    system: str

class Code(BaseModel):
    coding: list[CodingItem]
    text: str

class High(BaseModel):
    code: str
    system: str
    unit: str
    value: float

class Low(BaseModel):
    code: str
    system: str
    unit: str
    value: float

class ReferenceRangeItem(BaseModel):
    low: Optional[Low] = None
    high: Optional[High] = None
    normalValue: Optional[list[str]] = None
    type: Optional[list[str]] = None
    appliesTo: Optional[list[list[str]]] = None
    age: Optional[list[int]] = Field(None, json_schema_extra={ "ge":0, "le":150, "min_length":2, "max_length":2, "description":"age", "example":[50, 70] })

class Reference(BaseModel):
    resourceType: str
    status: str
    code: Code
    referenceRange: list[ReferenceRangeItem]

class ValueQuantity(BaseModel):
    value: float
    unit: str
    system: str
    code: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "value": 6.3,
                    "unit": "mmol/l",
                    "system": "http://unitsofmeasure.org",
                    "code": "mmol/L",
                }
            ]
        }
    }

class ObservationPayload(BaseModel):
    resourceType: str="Observation"
    id: str
    meta: dict
    status: str="final"
    code: Code
    subject: dict
    effectivePeriod: dict
    valueQuantity: ValueQuantity
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "resourceType": "Observation",
                    "id": "8892395",
                    "meta": {
                        "versionId": "1",
                        "lastUpdated": "2023-03-28T11:47:32.696+00:00",
                        "source": "#kfVW4VF0cQM8qBJe"
                    },
                    "status": "final",
                    "code": {
                        "coding": [
                        {
                            "code": "15074-8",
                            "display": "Glucose [Moles/volume] in Blood",
                            "system": "http://loinc.org"
                        }
                        ],
                        "text": "Glucose"
                    },
                    "subject": {
                        "reference": "Patient/7304958"
                    },
                    "effectivePeriod": {
                        "start": "2023-12-22T20:11:00.000+00:00",
                        "end": "2023-12-22T20:11:00.000+00:00"
                    },
                    "valueQuantity": {
                        "value": 6.3,
                        "unit": "mmol/l",
                        "system": "http://unitsofmeasure.org",
                        "code": "mmol/L"
                    }
                }
            ]
        }
    }

class Bundle(BaseModel):
    resourceType: str
    entry: list

class Acronyms(str, Enum):
    true = True
    false = False

class TempEnum(str, Enum):
    pass
