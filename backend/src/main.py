from fastapi import FastAPI, status, HTTPException, Depends
from typing import Annotated, Final, List
from fastapi.responses import RedirectResponse
from backend.src.api.resources.resource_loader import Resource
# from pydantic import BaseModel, create_model
from fastapi.middleware.cors import CORSMiddleware
from backend.src.api.models.schemas.references import CodingItem, Code, High, Low, ReferenceRangeItem, Reference, Bundle, Acronyms, TempEnum
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

organizations = ["default", "mylab"]
organization_keys = {}
for organization in organizations:
    organization_keys[organization] = organization
OrganizationKeys = TempEnum("OrganizationKeys", organization_keys)

resources = {}
for organization in organizations:
    resource = Resource().load(organization)
    resources[organization] = resource

reference_keys1 = {}
ReferenceKeys1 = {}
for organization in organizations:
    resource = resources[organization]
    reference_keys2 = {}
    for key in resource.references.keys():
        reference_keys2[key] = key

    reference_keys1[organization] = reference_keys2
    ReferenceKeys1[organization] = TempEnum("ReferenceKeys1", reference_keys1[organization])

bundle_keys = {}
for key in resource.bundles.keys():
    bundle_keys[key] = key

BundleKeys = TempEnum("BundleKeys", bundle_keys)

acronym_keys = {}
for key in resource.acronyms:
    acronym_keys[key] = key

AcronymKeys = TempEnum("AcronymKeys", acronym_keys)

@app.get("/{organization}/References")
def get_references(organization: OrganizationKeys) -> dict:
    return resources[organization].references

# @app.get("/References/keys")
# def get_reference_keys() -> list:
#     return resource.references.keys()

@app.get("/{organization}/References/keys")
def get_reference_keys(organization: OrganizationKeys) -> list:
    return resources[organization].references.keys()

@app.get("/{organization}/References/{key}", response_model=Reference, response_model_exclude_unset=True)
def get_reference_by_key(organization: OrganizationKeys, key: ReferenceKeys1["default"]):
    try:
        reference = resources[organization].references[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference key {key} not found")

    return reference

@app.get("/{organization}/References/{key}/referenceRange", response_model=List[ReferenceRangeItem], response_model_exclude_unset=True)
def get_reference_range_by_key(organization: OrganizationKeys, key: ReferenceKeys1[organization]):
    try:
        referenceRange = resources[organization].references[key]["referenceRange"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"referenceRange with key {key} not found")

    return referenceRange

@app.get("/{organization}/References/{key}/code")
def get_reference_code_by_key(organization: OrganizationKeys, key: ReferenceKeys1[organization]) -> Code:
    try:
        referenceCode = resources[organization].references[key]["code"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference code with key {key} not found")

    return referenceCode

@app.get("/{organization}/Bundles")
def get_bundles(organization: OrganizationKeys) -> dict:
    __bundle_formatter()

    return resources[organization].bundles

@app.get("/{organization}/Bundles/keys")
def get_bundle_keys(organization: OrganizationKeys) -> list:
    return resources[organization].bundles.keys()

@app.get("/{organization}/Bundles/{key}", response_model=Bundle, response_model_exclude_unset=True)
def get_bundle_by_key(organization: OrganizationKeys, key: BundleKeys):
    try:
        bundle = resources[organization].bundles[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"bundle key {key} not found")

    return bundle

@app.get("/{organization}/Acronyms")
def get_acronyms(organization: OrganizationKeys) -> dict:
    return resources[organization].acronyms

@app.get("/{organization}/Acronyms/{key}")
def get_acronym_by_key(organization: OrganizationKeys, key: AcronymKeys):
    try:
        acronym = resources[organization].acronyms[key]

    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"acronym key {key} not found")
    if 'reference' in acronym:
        return get_reference_by_key(organization, acronym['reference'])
    elif 'bundle' in acronym:
        return get_bundle_by_key(organization, acronym['bundle'])
    else:
        raise HTTPException(status_code=404, detail="not found")


def __bundle_formatter():
    for _, value in resource.bundles.items():
        for entry in value['entry']:
            entry['fullUrl'] = entry['fullUrl'].replace('BaseUrl', resource.base_url)
            if isinstance(entry['resource'], str):
                entry['resource'] = resource.references[entry['resource']]
