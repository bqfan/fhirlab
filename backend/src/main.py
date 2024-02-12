from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.api.routers import references, bundles
# from . import models
# from .database import engine
# from .routers import post, user, auth, vote
# from .config import settings


# models.Base.metadata.create_all(bind=engine)

description = """
fhirlab uses customized FHIR resource paths to fetch lab test references and evaluate labvalues and return FHIR compatible resources. 🚀

## References

You can **get observation references, acronyms, reference code and ranges**.
You can **evaluate lab values (observations) against reference ranges**.

## Bundles

You can **get bundles references, acronyms**.
You can **evaluate bundles of observations against reference ranges** (_not implemented_).
"""
tags_metadata = [
    {"name": "References",
     "description": "Reference values (intervals) for blood, urine, cerebrospinal fluid (CSF), stool, and other fluids (eg, gastric acid). In FHIR, observation resources can be used to describe observations which may need to be evaluated in order to determine whether a specific medicine can be administered or held (e.g., weight, lab value result) and provide guidance on the dose to be administered (e.g., sliding scale insulin dose)."},
    {"name": "Bundles",
     "description": "In FHIR bundles is referred to as \"bundling\" the resources together."
     }
]

# settings = SettingsConfigDict()
app = FastAPI(
    title="fhirlab",
    description=description,
    summary="Healthq Opensource.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "bqfan",
        "url": "https://healthq.io",
        "email": "bqfan@healthq.io",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
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

app.include_router(references.router)
app.include_router(bundles.router)
