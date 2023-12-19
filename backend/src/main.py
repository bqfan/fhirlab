from heapq import merge
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Final, List
from fastapi.responses import RedirectResponse
from backend.src.api.resources.resource_loader import Resource
# from pydantic import BaseModel, create_model
from fastapi.middleware.cors import CORSMiddleware
from backend.src.api.models.schemas.references import CodingItem, Code, High, Low, Reference, ReferenceRangeItem, ObservationPayload, Bundle, Acronyms, TempEnum
# from . import models
# from .database import engine
# from .routers import post, user, auth, vote
# from .config import settings


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(post.router)
# app.include_router(user.router)
# app.include_router(auth.router)
# app.include_router(vote.router)

resource = Resource().load()

reference_keys = {}
for key in resource.reference_keys:
    reference_keys[key] = key

ReferenceKeys = TempEnum("ReferenceKeys", reference_keys)

bundle_keys = {}
for key in resource.bundle_keys:
    bundle_keys[key] = key

BundleKeys = TempEnum("BundleKeys", bundle_keys)

acronym_keys = {}
for key in resource.acronyms:
    acronym_keys[key] = key

AcronymKeys = TempEnum("BundleKeys", acronym_keys)

@app.post("/Observation/_references/{key}", status_code=status.HTTP_201_CREATED)
async def evaluate_reference(key: ReferenceKeys, observation_payload: ObservationPayload):
    reference = get_reference_by_key(key)
    reference_range = get_reference_range_by_key(key)[0]
    resource_type = reference["resourceType"]
    display = reference["code"]["coding"][0]["display"]
    if "high" in reference_range:
        high = reference_range['high']['value']
        high_code = reference_range['high']['code']
        high_unit = reference_range['high']['unit']
    else:
        high = "N/A"
        high_code = "N/A"
        high_unit = "N/A"
    if "low" in reference_range:
        low = reference_range['low']['value']
        low_code = reference_range['low']['code']
        low_unit = reference_range['low']['unit']
    else:
        low = "N/A"
        low_code = "N/A"
        low_unit = "N/A"

    value_quantity = dict(observation_payload.valueQuantity)
    value = value_quantity['value']
    value_code = value_quantity['code']
    value_unit = value_quantity['unit']

    code = ""
    display = ""

    if high != "N/A" and value > high:
        code = "H"
        display = "High"
    elif low != "N/A" and value < low:
        code = "L"
        display = "Low"
    else:
        code = "N"
        display = "Normal"

    id = dict(observation_payload)["id"]
    identifier = dict(observation_payload)["identifier"]
    status = dict(observation_payload)["status"]
    subject = dict(observation_payload)["subject"]["reference"]
    effectiveDateTime = dict(observation_payload)["effectiveDateTime"]
    issued = dict(observation_payload)["issued"]
    practitioner = dict(observation_payload)["performer"][0]["reference"]

    text = {
        "status" : "generated",
        "div" : f"<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative: {resource_type}</b><a name=\"{id}\"> </a></p><div style=\"display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"><p style=\"margin-bottom: 0px\">Resource {resource_type} &quot;{id}&quot; </p></div><p><b>{identifier}</b>: id:\u00a06323\u00a0(use:\u00a0OFFICIAL)</p><p><b>status</b>: {status}</p><p><b>code</b>: {display} <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"https://loinc.org/\">LOINC</a>#15074-8)</span></p><p><b>subject</b>: <a href=\"patient-example-f001-pieter.html\">{subject}</a></p><p><b>effective</b>: {effectiveDateTime}</p><p><b>issued</b>: {issued}</p><p><b>performer</b>: <a href=\"practitioner-example-f005-al.html\">{practitioner}</a></p><p><b>value</b>: {value} {value_unit}<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code {value_code} = '{value_code} ')</span></p><p><b>interpretation</b>: High <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"http://terminology.hl7.org/5.4.0/CodeSystem-v3-ObservationInterpretation.html\">ObservationInterpretation</a>#H)</span></p><h3>ReferenceRanges</h3><table class=\"grid\"><tr><td style=\"display: none\">-</td><td><b>Low</b></td><td><b>High</b></td></tr><tr><td style=\"display: none\">*</td><td>{low} {low_unit}<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code {low_code} = '{low_code}')</span></td><td>{high} {high_unit}<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code {high_code} = '{high_code}')</span></td></tr></table></div>"
    }

    interpretation = [{
        "coding" : [{
        "system" : "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
        "code" : code,
        "display" : display
        }]
    }]

    response = dict(observation_payload) | reference
    response["text"] = text
    response["interpretation"] = interpretation
    return response

@app.get("/Observation/_references", status_code=status.HTTP_200_OK)
def get_references() -> dict:
    return resource.references

@app.get("/Observation/_references/_keys", status_code=status.HTTP_200_OK)
def get_reference_keys() -> list:
    return resource.reference_keys

@app.get("/Observation/_references/_acronyms", status_code=status.HTTP_200_OK)
def get_acronyms() -> dict:
    return resource.acronyms

@app.get("/Observation/_references/_acronyms/{key}", status_code=status.HTTP_200_OK)
def get_reference_by_acronym(key: AcronymKeys):
    try:
        acronym_value = resource.acronyms[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"acronym key {key} not found")

    return get_reference_by_key(acronym_value)

@app.get("/Observation/_references/{key}", status_code=status.HTTP_200_OK, response_model=Reference, response_model_exclude_unset=True)
def get_reference_by_key(key: ReferenceKeys):
    try:
        reference = resource.references[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference key {key} not found")

    return reference

@app.get("/Observation/_references/{key}/_referenceRange", status_code=status.HTTP_200_OK, response_model=list[ReferenceRangeItem], response_model_exclude_unset=True)
def get_reference_range_by_key(key: ReferenceKeys):
    try:
        referenceRange = resource.references[key]["referenceRange"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"referenceRange with key {key} not found")

    return referenceRange

@app.get("/Observation/_references/{key}/_code", status_code=status.HTTP_200_OK)
def get_reference_code_by_key(key: ReferenceKeys) -> Code:
    try:
        referenceCode = resource.references[key]["code"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference code with key {key} not found")

    return referenceCode

@app.get("/Bundles/_references", status_code=status.HTTP_200_OK)
def get_bundles() -> dict:
    __bundle_formatter()

    return resource.bundles

@app.get("/Bundles/_keys")
def get_bundle_keys() -> list:
    return resource.bundle_keys

@app.get("/Bundles/{key}/_references", status_code=status.HTTP_200_OK, response_model=Bundle, response_model_exclude_unset=True)
def get_bundle_by_key(key: BundleKeys):
    try:
        __bundle_formatter()
        bundle = resource.bundles[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"bundle key {key} not found")

    return bundle

def __bundle_formatter():
    for _, value in resource.bundles.items():
        for entry in value['entry']:
            entry['fullUrl'] = entry['fullUrl'].replace('BaseUrl', resource.base_url)
            if isinstance(entry['resource'], str):
                entry['resource'] = resource.references[entry['resource']]
