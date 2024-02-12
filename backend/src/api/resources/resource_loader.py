import glob
from fastapi import status, HTTPException
import yaml, json
from yaml import SafeLoader
from backend.src.api.models.schemas.references import Reference
from fhir.resources.observation import Observation
from fhir.resources.bundle import Bundle

class Resource:
    BaseUrl = "http://localhost:8000"

    def __init__(self, organization: str="default"):
        self.base_url = "http://localhost:8000"
        self.organization = organization
        self.references = {}
        self.reference_keys = {}
        self.bundles = {}
        self.bundle_keys = {}
        self.acronyms = []

    def load(self) -> dict:
        resources = self.__load_resources(self.organization)
        self.references = self.__references(resources)
        self.reference_keys = self.__reference_keys()
        self.bundles = self.__bundles(resources)
        self.bundle_keys = self.__bundle_keys()
        self.acronyms = self.__acronyms()

        return self

    def __load_resources(self, organization: str):
        resource_files = glob.glob(f"backend/src/api/resources/{organization}/references/*.yaml") + \
            glob.glob(f"backend/src/api/resources/{organization}/bundles/*.yaml")

        resources_yaml = self.__concat_yaml_files(resource_files)
        resources_dict = yaml.load(resources_yaml, Loader=SafeLoader)

        return resources_dict

    def __references(self, resources):
        references = self.__filter_resources_by_resource_type(resources, "Observation")

        for key in references.keys():
            try:
                Observation.validate(references[key])
            except Exception as e:
                raise Exception(f"reference {key} is invalid: {e}")

        return references

    def __reference_keys(self):
        return list(self.references.keys())

    def __bundles(self, resources):
        bundles = self.__filter_resources_by_resource_type(resources, "Bundle")
 
        for key in bundles.keys():
            try:
                Bundle.validate(bundles[key])
            except Exception as e:
                raise Exception(f"bundle {key} is invalid: {e}")

        return bundles

    def __bundle_keys(self):
        return list(self.bundles.keys())

    def __acronyms(self):
        acronym_files = glob.glob(f"backend/src/api/resources/{self.organization}/acronyms/*.yaml")
        acronyms_str = self.__concat_yaml_files(acronym_files)
        acronyms_dict = yaml.load(acronyms_str, Loader=SafeLoader)

        return acronyms_dict

    def __concat_yaml_files(self, yaml_files) -> str:
        yaml_str = ""
        for filename in yaml_files:
            with open(filename, "r", encoding="latin-1") as f:
                yaml_str += f.read()

        return yaml_str

    def __filter_resources_by_resource_type(self, resources: dict, resource_type: str) -> dict:
        filtered_resources = {}
        for key, value in resources.items():
            if value['resourceType'] == resource_type:
                filtered_resources[key] = value

        return filtered_resources