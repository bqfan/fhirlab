import glob
import yaml, json
from yaml import SafeLoader
from backend.src.api.models.schemas.references import Reference

class Resource:
    BaseUrl = "http://localhost:8080"

    def __init__(self, organization: str="default"):
        self.base_url = "http://localhost:8080"
        self.organization = organization
        self.references = {}
        self.reference_keys = {}
        self.bundles = {}
        self.bundle_keys = {}
        self.acronyms = []

    def load(self) -> dict:
        self.references = self.__get_references()
        self.reference_keys = self.__get_reference_keys()
        self.bundles = self.__get_bundles()
        self.bundle_keys = self.__get_bundle_keys()
        self.acronyms = self.__get_acronyms()

        return self

    def __get_resources(self, organization: str):
        resource_files = glob.glob(f"backend/src/api/resources/{organization}/references/*.yaml") + \
            glob.glob(f"backend/src/api/resources/{organization}/bundles/*.yaml")

        resource_yaml_files = self.__concat_yaml_files(resource_files)
        #print(resource_yaml_files)
        yaml_obj = yaml.safe_load(resource_yaml_files)
        
        for k, v in yaml.safe_load(resource_yaml_files).items():
            print(k)
            print(v)
        resources_dict = yaml.load(resource_yaml_files, Loader=SafeLoader)
        #print(resources_dict.keys())
        return resources_dict

    def __get_references(self):
        resources_dict = self.__get_resources("default")

        observations = self.filter_resources_by_resource_type(resources_dict, "Observation")

        return observations

    def __get_reference_keys(self):
        return list(self.references.keys())

    def __get_bundles(self):
        resources_dict = self.__get_resources("default")
        bundles = self.filter_resources_by_resource_type(resources_dict, "Bundle")

        return bundles

    def __get_bundle_keys(self):
        return list(self.bundles.keys())

    def __get_acronyms(self):
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

    def filter_resources_by_resource_type(self, resources: dict, resource_type: str) -> dict:
        filtered_resources = {}
        for key, value in resources.items():
            if value['resourceType'] == resource_type:
                filtered_resources[key] = value

        return filtered_resources