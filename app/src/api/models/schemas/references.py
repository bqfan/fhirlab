from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class CodingItem(BaseModel):
    code: str
    display: str
    system: str

class Code(BaseModel):
    coding: List[CodingItem]
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
    normalValue: List[str] = None
    type: List[str] = None
    appliesTo: List[List[str]] = None
    age: Optional[list[int]] = Field(None, json_schema_extra={ "ge":0, "le":150, "min_length":2, "max_length":2, "description":"age", "example":[50, 70] })

class Reference(BaseModel):
    resourceType: str
    code: Code
    referenceRange: List[ReferenceRangeItem]

class Acronyms(str, Enum):
    true = True
    false = False

class TempEnum(str, Enum):
    pass
