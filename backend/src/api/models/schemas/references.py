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
    id: str
    identifier: list
    status: str="final"
    subject: dict
    effectiveDateTime: str
    issued: str
    performer: list
    valueQuantity: ValueQuantity
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123456789",
                    "identifier" : [{
                        "use" : "official",
                        "system" : "https:/helthq.dev/identifiers/observations",
                        "value" : "1234"
                    }],
                    "subject" : {
                        "reference" : "Patient/example"
                    },
                    "effectiveDateTime" : "2023-12-17T09:30:10+01:00",
                    "issued" : "2023-12-17T15:30:10+01:00",
                    "performer" : [{
                        "reference" : "Practitioner/example",
                    }],
                    "status": "final",
                    "valueQuantity":
                    {
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
