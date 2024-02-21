from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal, Optional
from enum import Enum


"""
https://hl7.org/fhir/R4/observation-definitions.html#Observation.referenceRange
Observation.referenceRange
Element Id	Observation.referenceRange
Definition	
Guidance on how to interpret the value by comparison to a normal or recommended range.
Multiple reference ranges are interpreted as an "OR". In other words, to represent two distinct target populations,
two referenceRange elements would be used.
"""


"""
Observation.referenceRange.low
Element Id	Observation.referenceRange.low
Definition	
The value of the low bound of the reference range.
The low bound of the reference range endpoint is inclusive of the value (e.g. reference range is >=5 - <=9).
If the low bound is omitted, it is assumed to be meaningless (e.g. reference range is <=2.3).
"""

"""
Observation.referenceRange.high
Element Id	Observation.referenceRange.high
Definition	
The value of the high bound of the reference range.
The high bound of the reference range endpoint is inclusive of the value (e.g. reference range is >=5 - <=9).
If the high bound is omitted, it is assumed to be meaningless (e.g. reference range is >= 2.3).
"""


"""
Observation.referenceRange.type
Element Id	Observation.referenceRange.type
Definition	
Codes to indicate the what part of the targeted reference population it applies to.
For example, the normal or therapeutic range.
https://hl7.org/fhir/R4/valueset-referencerange-meaning.html
"""


"""
Observation.referenceRange.appliesTo
Element Id	Observation.referenceRange.appliesTo
Definition	
Codes to indicate the target population this reference range applies to.
For example, a reference range may be based on the normal population or a particular sex or race.
Multiple appliesTo are interpreted as an "AND" of the target populations.
For example, to represent a target population of African American females,
both a code of female and a code for African American would be used.
https://hl7.org/fhir/R4/valueset-referencerange-appliesto.html
"""


"""
Observation.referenceRange.age
Element Id	Observation.referenceRange.age
Definition	
The age at which this reference range is applicable.
This is a neonatal age (e.g. number of weeks at term) if the meaning says so.
"""

"""
Observation.referenceRange.text
Element Id	Observation.referenceRange.text
Definition	
Text based reference range in an observation which may be used
when a quantitative range is not appropriate for an observation.
An example would be a reference value of "Negative" or a list or table of "normals".
"""


class CodingItem(BaseModel):
    code: str
    display: str
    system: str


class Code(BaseModel):
    coding: list[CodingItem]
    text: str


class ReferenceRangeLow(BaseModel):
    value: float    # Numerical value (with implicit precision)
    comparator: Optional[Literal['<', '<=', '>=', '>']] = None # < | <= | >= | > - how to understand the value
    unit: Literal['mmHg', 'mmol/l', 'mmol/L', 'mg/dL', 'g/dl', 'μKat/L', 'U/L', 'g/L']   # Unit representation
    system: Literal['http://unitsofmeasure.org']    # System that defines coded unit form
    code: Literal['mm[Hg]', 'mmol/L', 'mg/dL', 'g/dL', 'μKat/L', 'U/L', 'g/L']  # Coded form of the unit


class ReferenceRangeHigh(BaseModel):
    value: float    # Numerical value (with implicit precision)
    comparator: Optional[Literal['<', '<=', '>=', '>']] = None # < | <= | >= | > - how to understand the value
    unit: Literal['mmHg', 'mmol/l', 'mmol/L', 'mg/dL', 'g/dl', 'μKat/L', 'U/L', 'g/L']   # Unit representation
    system: Literal['http://unitsofmeasure.org']    # System that defines coded unit form
    code: Literal['mm[Hg]', 'mmol/L', 'mg/dL', 'g/dL', 'μKat/L', 'U/L', 'g/L']  # Coded form of the unit


class ReferenceRange(BaseModel):
    low: Optional[ReferenceRangeLow] = None
    high: Optional[ReferenceRangeHigh] = None
    normalValue: Optional[list[str]] = None
    #type: Optional[list[str]] = Literal[None, 'normal', 'recommended', 'treatment', 'therapeutic', 'pre', 'post']
    appliesTo: Optional[list[list[str]]] = None
    age: Optional[list[int]] = Field(None, json_schema_extra={
        "ge": 0,
        "le": 150,
        "min_length": 2,
        "max_length": 2,
        "description": "age",
        "example": [50, 70]})
    text: Optional[list[str]] = None


class Reference(BaseModel):
    resourceType: Literal['Observation']
    status: str
    code: Code
    referenceRange: list[ReferenceRange]


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
    resourceType: str = "Observation"
    id: str
    meta: dict
    status: str = "final"
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
