import glob
import yaml, json
from yaml import SafeLoader
from backend.src.api.models.schemas.references import Reference

class Resource:
    BaseUrl = "http://localhost:8080"

    def __init__(self, lab_name: str="default"):
        self.base_url = "http://localhost:8080"
        self.lab_name = lab_name
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

    def __get_references(self):
        references_path = f"backend/src/api/resources/{self.lab_name}/references"
        references_str = self.__concat_yaml_files(references_path)
        references_dict = yaml.load(references_str, Loader=SafeLoader)

        return references_dict

    def __get_reference_keys(self):
        return list(self.references.keys())

    def __get_bundles(self):
        bundles_path = f"backend/src/api/resources/{self.lab_name}/bundles"
        bundles_str = self.__concat_yaml_files(bundles_path)
        bundles_dict = yaml.load(bundles_str, Loader=SafeLoader)

        return bundles_dict

    def __get_bundle_keys(self):
        return list(self.bundles.keys())

    def __get_acronyms(self):
        acronyms_path = f"backend/src/api/resources/{self.lab_name}/acronyms"
        acronyms_str = self.__concat_yaml_files(acronyms_path)
        acronyms_dict = yaml.load(acronyms_str, Loader=SafeLoader)

        return acronyms_dict

    def __concat_yaml_files(self, yaml_file_path) -> str:
        filenames = glob.glob(f"{yaml_file_path}/*.yaml")

        references_str = ""
        for filename in filenames:
            with open(filename, "r", encoding="latin-1") as f:
                references_str = references_str + f.read()

        return references_str
