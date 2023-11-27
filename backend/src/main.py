from fastapi import FastAPI, status, HTTPException, Depends
from typing import Final, List
from backend.src.api.resources.resource_loader import Resource
# from pydantic import BaseModel, create_model
from fastapi.middleware.cors import CORSMiddleware
from backend.src.api.models.schemas.references import CodingItem, Code, High, Low, ReferenceRangeItem, Reference, Acronyms, TempEnum
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
print(reference_keys)
ReferenceKeys = TempEnum("ReferenceKeys", reference_keys)

bundle_keys = {}
for key in resource.bundle_keys:
    bundle_keys[key] = key
print(bundle_keys)
BundleKeys = TempEnum("BundleKeys", bundle_keys)

@app.get("/v1/References")
def get_references() -> dict:
    return resource.references

@app.get("/v1/References/keys")
def get_reference_keys() -> list:
    return resource.reference_keys

@app.get("/v1/References/{key}", response_model=Reference, response_model_exclude_unset=True)
def get_reference_by_key(key: ReferenceKeys):
    try:
        reference = resource.references[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference key {key} not found")

    return reference

@app.get("/v1/References/{key}/referenceRange")
def get_reference_range_by_key(key: ReferenceKeys, response_model=List[ReferenceRangeItem], response_model_exclude_unset=True):
    try:
        referenceRange = resource.references[key]["referenceRange"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"referenceRange with key {key} not found")

    return referenceRange

@app.get("/v1/References/{key}/code")
def get_reference_code_by_key(key: ReferenceKeys) -> Code:
    try:
        referenceCode = resource.references[key]["code"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"reference code with key {key} not found")

    return referenceCode

@app.get("/v1/Bundles")
def get_bundles() -> dict:
    return resource.bundles

@app.get("/v1/Bundles/keys")
def get_bundle_keys() -> list:
    return resource.bundle_keys

@app.get("/v1/Bundles/{key}")
def get_bundle_by_key(key: BundleKeys):
    try:
        bundle = resource.bundles[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"bundle key {key} not found")

    return bundle
