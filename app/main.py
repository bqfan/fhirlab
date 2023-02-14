from fastapi import FastAPI
from app.utils import labvalues_concatenator
# from fastapi.middleware.cors import CORSMiddleware

# from . import models
# from .database import engine
# from .routers import post, user, auth, vote
# from .config import settings


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(post.router)
# app.include_router(user.router)
# app.include_router(auth.router)
# app.include_router(vote.router)


@app.get("/v1/labvalues/")
def root():
    vabvalues = labvalues_concatenator.concatenate("default")
    return vabvalues

@app.get("/v1/labvalues/{id}")
def labvalue_by_id(id):
    vabvalue = labvalues_concatenator.concatenate("default")[id]
    return vabvalue

@app.get("/v1/labvalues/acronyms/{id}")
def labvalue_acronyms_by_id(id):
    vabvalue = labvalues_concatenator.concatenate("default")["acronyms"][id]
    return vabvalue