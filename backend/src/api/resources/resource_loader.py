import glob
import yaml, json
from yaml import SafeLoader
from backend.src.api.models.schemas.references import Reference

class Resource:
    BaseUrl = "http://localhost:8080"

    def __init__(self):
        self.base_url = "http://localhost:8080"
        self.organization = ""
        self.references = {}
        self.bundles = {}
        self.acronyms = {}

    def load(self, organization: str="default") -> dict:
        resources = self.__load_resources(organization)

        self.organization = organization
        self.references = self.__get_references(resources)
        self.bundles = self.__get_bundles(resources)
        self.acronyms = self.__get_acronyms(resources)
        
        return self

    def __load_resources(self, organization: str):
        resource_files = glob.glob(f"backend/src/api/resources/{organization}/references/*.yaml") + \
            glob.glob(f"backend/src/api/resources/{organization}/bundles/*.yaml") + \
                glob.glob(f"backend/src/api/resources/{organization}/acronyms/*.yaml")

        resource_yaml_files = self.__concat_yaml_files(resource_files)
        resources_dict = yaml.load(resource_yaml_files, Loader=SafeLoader)

        return resources_dict

    def __get_references(self, resources: dict):
        references = self.filter_resources_by_resource_type(resources, "Observation")

        return references

    def __get_bundles(self, resources: dict):
        bundles = self.filter_resources_by_resource_type(resources, "Bundle")

        return bundles

    def __get_acronyms(self, resources: dict):
        acronyms = self.filter_resources_by_resource_type(resources, "Acronym")

        return acronyms

    def __concat_yaml_files(self, yaml_files) -> str:
        yaml_str = ""
        for filename in yaml_files:
            with open(filename, "r", encoding="latin-1") as f:
                yaml_str += f.read()

        return yaml_str

    def filter_resources_by_resource_type(self, resources: dict, resource_type: str) -> dict:
        filtered_resources = {}
        for key, value in resources.items():
            if value['resourceType'] == resource_type:
                filtered_resources[key] = value

        return filtered_resources
