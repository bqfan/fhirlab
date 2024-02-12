
from typing import Annotated
from fastapi import Body, status, HTTPException, Depends
from fastapi import APIRouter
from fastapi.security.api_key import APIKey
from fhir.resources.observation import Observation
from backend.src.api.resources.resource_loader import Resource
from backend.src.api.models.schemas.references \
    import Code, Reference, ReferenceRangeItem, TempEnum
from backend.src.api.utils import get_api_key, \
    __check_semantic_interoperable, __check_unit

router = APIRouter(
    prefix="/Observation/_references",
    tags=['References']
)

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


@router.get("/",
            summary="Returns all observation references",
            status_code=status.HTTP_200_OK)
def get_references(api_key: APIKey = Depends(get_api_key)) -> dict:
    return resource.references


@router.get("/_keys",
            summary="Returns all observation reference keys",
            status_code=status.HTTP_200_OK)
def get_reference_keys(api_key: APIKey = Depends(get_api_key)) -> list:
    return resource.reference_keys


@router.get("/_acronyms",
            summary="Returns all observation reference acronyms",
            status_code=status.HTTP_200_OK)
def get_acronyms(api_key: APIKey = Depends(get_api_key)) -> dict:
    return resource.acronyms


@router.get("/_acronyms/{key}",
            summary="Returns an observation reference by its acronmy",
            status_code=status.HTTP_200_OK)
def get_reference_by_acronym(key: AcronymKeys,
                             api_key: APIKey = Depends(get_api_key)):
    try:
        acronym_value = resource.acronyms[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"acronym key {key} not found")

    return get_reference_by_key(acronym_value)


@router.get("/{key}",
            summary="Returns an observation reference by its reference key",
            status_code=status.HTTP_200_OK,
            response_model=Reference,
            response_model_exclude_unset=True)
def get_reference_by_key(key: ReferenceKeys,
                         api_key: APIKey = Depends(get_api_key)):
    try:
        reference = resource.references[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference key {key} not found")

    return reference


@router.get("/{key}/_referenceRange",
            summary="Returns observation reference range by its reference key",
            status_code=status.HTTP_200_OK,
            response_model=list[ReferenceRangeItem],
            response_model_exclude_unset=True)
def get_reference_range_by_key(key: ReferenceKeys,
                               api_key: APIKey = Depends(get_api_key)):
    try:
        referenceRange = resource.references[key]["referenceRange"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"referenceRange with key {key} not found")

    return referenceRange


@router.get("/{key}/_code",
            summary="Returns observation reference code by its reference key",
            status_code=status.HTTP_200_OK,
            tags=["References"])
def get_reference_code_by_key(key: ReferenceKeys,
                              api_key: APIKey = Depends(get_api_key)) -> Code:
    try:
        referenceCode = resource.references[key]["code"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference code with key {key} not found")

    return referenceCode


@router.post("/{key}",
             summary="Generate observation result by its reference key",
             status_code=status.HTTP_201_CREATED)
async def evaluate_observation(
    key: ReferenceKeys,
    observation: Annotated[
        dict,
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
        )], api_key: APIKey = Depends(get_api_key)):

    reference = get_reference_by_key(key)

    try:
        Observation.validate(observation)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Request payload is invalid: {e}.")

    if not __check_semantic_interoperable(observation, reference):
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Request code is not semantic interoperable.")

    if not __check_unit(observation, reference):
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Request unit is not semantic interoperable.")

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
    # identifier = dict(observation_payload)["identifier"]
    observation_status = observation["status"]
    subject = observation["subject"]["reference"]
    # effectivePeriodStart = observation["effectivePeriod"]["start"]
    # effectivePeriodend = observation["effectivePeriod"]["end"]
    # issued = dict(observation_payload)["issued"]
    # practitioner = dict(observation_payload)["performer"][0]["reference"]

    # text = {
    #     "status" : "generated",
    #     "div" : f"<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative: {resource_type}</b><a name=\"{id}\"> </a></p><div style=\"display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"><p style=\"margin-bottom: 0px\">Resource {resource_type} &quot;{id}&quot; </p></div><p><b>{identifier}</b>: id:\u00a06323\u00a0(use:\u00a0OFFICIAL)</p><p><b>status</b>: {status}</p><p><b>code</b>: {display} <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"https://loinc.org/\">LOINC</a>#15074-8)</span></p><p><b>subject</b>: <a href=\"patient-example-f001-pieter.html\">{subject}</a></p><p><b>effective</b>: {effectiveDateTime}</p><p><b>issued</b>: {issued}</p><p><b>performer</b>: <a href=\"practitioner-example-f005-al.html\">{practitioner}</a></p><p><b>value</b>: {value} {value_unit}<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code {value_code} = '{value_code} ')</span></p><p><b>interpretation</b>: High <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"http://terminology.hl7.org/5.4.0/CodeSystem-v3-ObservationInterpretation.html\">ObservationInterpretation</a>#H)</span></p><h3>ReferenceRanges</h3><table class=\"grid\"><tr><td style=\"display: none\">-</td><td><b>Low</b></td><td><b>High</b></td></tr><tr><td style=\"display: none\">*</td><td>{low} {low_unit}<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code {low_code} = '{low_code}')</span></td><td>{high} {high_unit}<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code {high_code} = '{high_code}')</span></td></tr></table></div>"
    # }
    text = {
        "status": "generated",
        "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative: {resource_type}</b><a name=\"{id}\"> </a></p><div style=\"display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"><p style=\"margin-bottom: 0px\">Resource {resource_type} &quot;{id}&quot; </p></div><p>: id:\u00a06323\u00a0(use:\u00a0OFFICIAL)</p><p><b>status</b>: {observation_status}</p><p><b>code</b>: {display} <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"https://loinc.org/\">LOINC</a>#15074-8)</span></p><p><b>subject</b>: <a href=\"patient-example-f001-pieter.html\">{subject}</a></p><p><b>value</b>: {value} {value_unit}<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code {value_code} = '{value_code} ')</span></p><p><b>interpretation</b>: High <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"http://terminology.hl7.org/5.4.0/CodeSystem-v3-ObservationInterpretation.html\">ObservationInterpretation</a>#H)</span></p><h3>ReferenceRanges</h3><table class=\"grid\"><tr><td style=\"display: none\">-</td><td><b>Low</b></td><td><b>High</b></td></tr><tr><td style=\"display: none\">*</td><td>{low} {low_unit}<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code {low_code} = '{low_code}')</span></td><td>{high} {high_unit}<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code {high_code} = '{high_code}')</span></td></tr></table></div>"
    }

    interpretation = [{
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                "code": code,
                "display": display
            }
        ]
    }]

    response = observation | reference
    response["text"] = text
    response["interpretation"] = interpretation

    try:
        Observation.validate(response)
    except Exception as e:
        raise Exception(f"observation {key} is invalid: {e}")

    return response
