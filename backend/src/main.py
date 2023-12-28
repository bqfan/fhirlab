from heapq import merge
import json
from fastapi import Body, FastAPI, status, HTTPException, Depends
from typing import Annotated, Final, List
from fastapi.responses import RedirectResponse
from backend.src.api.resources.resource_loader import Resource
# from pydantic import BaseModel, create_model
from fastapi.middleware.cors import CORSMiddleware
from backend.src.api.models.schemas.references import CodingItem, Code, High, Low, Reference, ReferenceRangeItem, ObservationPayload, Bundle, Acronyms, TempEnum
from fhir.resources.observation import Observation
# from . import models
# from .database import engine
# from .routers import post, user, auth, vote
# from .config import settings


# models.Base.metadata.create_all(bind=engine)

description = """
labtest-api uses customized FHIR resource paths to fetch lab test references and evaluate labvalues and return FHIR compatible resources. 🚀

## References

You can **get observation references, acronyms, reference code and ranges**.
You can **evaluate lab values (observations) against reference ranges**.

## Bundlers

You can **get bundles references, acronyms**.
You can **evaluate bundles of observations against reference ranges** (_not implemented_).
"""
tags_metadata = [
    {"name": "References",
     "description": "Reference values (intervals) for blood, urine, cerebrospinal fluid (CSF), stool, and other fluids (eg, gastric acid). In FHIR, observation resources can be used to describe observations which may need to be evaluated in order to determine whether a specific medicine can be administered or held (e.g., weight, lab value result) and provide guidance on the dose to be administered (e.g., sliding scale insulin dose)." },
    {"name": "Bundles",
     "description": "In FHIR bundles is referred to as \"bundling\" the resources together."
     }
]

app = FastAPI(
    title="labtest-api",
    description=description,
    summary="Healthq Opensource.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "bqfan",
        "url": "https://healthq.dev",
        "email": "bqfan@healthq.dev",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },    
    openapi_tags=tags_metadata
)

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

@app.get("/Observation/_references", status_code=status.HTTP_200_OK, tags=["References"])
def get_references() -> dict:
    return resource.references

@app.get("/Observation/_references/_keys", status_code=status.HTTP_200_OK, tags=["References"])
def get_reference_keys() -> list:
    return resource.reference_keys

@app.get("/Observation/_references/_acronyms", status_code=status.HTTP_200_OK, tags=["References"])
def get_acronyms() -> dict:
    return resource.acronyms

@app.get("/Observation/_references/_acronyms/{key}", status_code=status.HTTP_200_OK, tags=["References"])
def get_reference_by_acronym(key: AcronymKeys):
    try:
        acronym_value = resource.acronyms[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"acronym key {key} not found")

    return get_reference_by_key(acronym_value)

@app.get("/Observation/_references/{key}", status_code=status.HTTP_200_OK, response_model=Reference, response_model_exclude_unset=True, tags=["References"])
def get_reference_by_key(key: ReferenceKeys):
    try:
        reference = resource.references[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference key {key} not found")

    return reference

@app.get("/Observation/_references/{key}/_referenceRange", status_code=status.HTTP_200_OK, response_model=list[ReferenceRangeItem], response_model_exclude_unset=True, tags=["References"])
def get_reference_range_by_key(key: ReferenceKeys):
    try:
        referenceRange = resource.references[key]["referenceRange"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"referenceRange with key {key} not found")

    return referenceRange

@app.get("/Observation/_references/{key}/_code", status_code=status.HTTP_200_OK, tags=["References"])
def get_reference_code_by_key(key: ReferenceKeys) -> Code:
    try:
        referenceCode = resource.references[key]["code"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference code with key {key} not found")

    return referenceCode

@app.post("/Observation/_references/{key}", status_code=status.HTTP_201_CREATED, tags=["References"])
async def evaluate_reference(key: ReferenceKeys, observation:
                             Annotated[dict,
                                       Body(
                                            examples=[
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
                                       )]):

    reference = get_reference_by_key(key)
    
    global status
    try:
        Observation.validate(observation)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Request payload is invalid: {e}.")

    if not __check_semantic_interoperable(observation, reference):
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Request code is not semantic interoperable.")

    if not __check_unit(observation, reference):
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Request unit is not semantic interoperable.")
    
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

    value_quantity = observation['valueQuantity']
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

    id = observation["id"]
    #identifier = dict(observation_payload)["identifier"]
    status = observation["status"]
    subject = observation["subject"]["reference"]
    effectivePeriodStart = observation["effectivePeriod"]["start"]
    effectivePeriodend = observation["effectivePeriod"]["end"]
    #issued = dict(observation_payload)["issued"]
    #practitioner = dict(observation_payload)["performer"][0]["reference"]

    # text = {
    #     "status" : "generated",
    #     "div" : f"<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative: {resource_type}</b><a name=\"{id}\"> </a></p><div style=\"display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"><p style=\"margin-bottom: 0px\">Resource {resource_type} &quot;{id}&quot; </p></div><p><b>{identifier}</b>: id:\u00a06323\u00a0(use:\u00a0OFFICIAL)</p><p><b>status</b>: {status}</p><p><b>code</b>: {display} <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"https://loinc.org/\">LOINC</a>#15074-8)</span></p><p><b>subject</b>: <a href=\"patient-example-f001-pieter.html\">{subject}</a></p><p><b>effective</b>: {effectiveDateTime}</p><p><b>issued</b>: {issued}</p><p><b>performer</b>: <a href=\"practitioner-example-f005-al.html\">{practitioner}</a></p><p><b>value</b>: {value} {value_unit}<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code {value_code} = '{value_code} ')</span></p><p><b>interpretation</b>: High <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"http://terminology.hl7.org/5.4.0/CodeSystem-v3-ObservationInterpretation.html\">ObservationInterpretation</a>#H)</span></p><h3>ReferenceRanges</h3><table class=\"grid\"><tr><td style=\"display: none\">-</td><td><b>Low</b></td><td><b>High</b></td></tr><tr><td style=\"display: none\">*</td><td>{low} {low_unit}<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code {low_code} = '{low_code}')</span></td><td>{high} {high_unit}<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code {high_code} = '{high_code}')</span></td></tr></table></div>"
    # }
    text = {
        "status" : "generated",
        "div" : f"<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative: {resource_type}</b><a name=\"{id}\"> </a></p><div style=\"display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"><p style=\"margin-bottom: 0px\">Resource {resource_type} &quot;{id}&quot; </p></div><p>: id:\u00a06323\u00a0(use:\u00a0OFFICIAL)</p><p><b>status</b>: {status}</p><p><b>code</b>: {display} <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"https://loinc.org/\">LOINC</a>#15074-8)</span></p><p><b>subject</b>: <a href=\"patient-example-f001-pieter.html\">{subject}</a></p><p><b>value</b>: {value} {value_unit}<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code {value_code} = '{value_code} ')</span></p><p><b>interpretation</b>: High <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"http://terminology.hl7.org/5.4.0/CodeSystem-v3-ObservationInterpretation.html\">ObservationInterpretation</a>#H)</span></p><h3>ReferenceRanges</h3><table class=\"grid\"><tr><td style=\"display: none\">-</td><td><b>Low</b></td><td><b>High</b></td></tr><tr><td style=\"display: none\">*</td><td>{low} {low_unit}<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code {low_code} = '{low_code}')</span></td><td>{high} {high_unit}<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code {high_code} = '{high_code}')</span></td></tr></table></div>"
    }

    interpretation = [{
        "coding" : [{
        "system" : "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
        "code" : code,
        "display" : display
        }]
    }]

    response = observation | reference
    response["text"] = text
    response["interpretation"] = interpretation
    return response

@app.get("/Bundles/_references", status_code=status.HTTP_200_OK, tags=["Bundles"])
def get_bundles() -> dict:
    __bundle_formatter()

    return resource.bundles

@app.get("/Bundles/_keys", tags=["Bundles"])
def get_bundle_keys() -> list:
    return resource.bundle_keys

@app.get("/Bundles/{key}/_references", status_code=status.HTTP_200_OK, response_model=Bundle, response_model_exclude_unset=True, tags=["Bundles"])
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

def get_json(obj):
  return json.loads(
    json.dumps(obj, default=lambda o: getattr(o, '__dict__', str(o)))
  )

def __check_semantic_interoperable(observation, reference):
    reference_code = reference["code"]
    observation_code = observation["code"]

    for observation_code_coding in observation_code["coding"]:
        for reference_code_coding in reference_code["coding"]:
            if observation_code_coding["system"] == reference_code_coding["system"] and \
                observation_code_coding["code"] == reference_code_coding["code"]:

                return True
    
    return False

def __check_unit(observation, reference):
    reference_ranges = reference["referenceRange"]
    observation_value_quantity = observation["valueQuantity"]

    for reference_range in reference_ranges:
        if "high" in reference_range and "low" in reference_range and \
                observation_value_quantity["system"] == reference_range["high"]["system"] and \
                    observation_value_quantity["unit"] == reference_range["high"]["unit"] and \
                        observation_value_quantity["system"] == reference_range["low"]["system"] and \
                            observation_value_quantity["unit"] == reference_range["low"]["unit"]:
                                return True
        elif "high" in reference_range and "low" not in reference_range and \
                observation_value_quantity["system"] == reference_range["high"]["system"] and \
                    observation_value_quantity["unit"] == reference_range["high"]["unit"]:
                        return True
        elif "high" not in reference_range and "low" in reference_range and \
                observation_value_quantity["system"] == reference_range["low"]["system"] and \
                    observation_value_quantity["unit"] == reference_range["low"]["unit"]:
                        return True

        else:
            return False
