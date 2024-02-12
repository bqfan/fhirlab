from fastapi import status, HTTPException, Depends
from fastapi import APIRouter
from fastapi.security.api_key import APIKey
from backend.src.api.resources.resource_loader import Resource
from backend.src.api.models.schemas.references import Bundle, TempEnum
from backend.src.api.utils import get_api_key, __bundle_formatter

router = APIRouter(
    prefix="/Bundles",
    tags=['Bundles']
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


@router.get("/_references",
            summary="Returns all bundle references",
            status_code=status.HTTP_200_OK, tags=["Bundles"])
def get_bundles(api_key: APIKey = Depends(get_api_key)) -> dict:
    __bundle_formatter(resource)

    return resource.bundles


@router.get("/_keys",
            summary="Returns all bundle keys",
            tags=["Bundles"])
def get_bundle_keys(api_key: APIKey = Depends(get_api_key)) -> list:
    return resource.bundle_keys


@router.get("/{key}/_references",
            summary="Returns a bundle's references by bundle key",
            status_code=status.HTTP_200_OK,
            response_model=Bundle,
            response_model_exclude_unset=True, tags=["Bundles"])
def get_bundle_by_key(key: BundleKeys, api_key: APIKey = Depends(get_api_key)):
    try:
        __bundle_formatter(resource)
        bundle = resource.bundles[key]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"bundle key {key} not found")

    return bundle
