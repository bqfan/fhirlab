import glob
import yaml, json
from yaml import SafeLoader
from backend.src.api.models.schemas.references import Reference

class Resource:
    def __init__(self, lab_name: str="default"):
        self.lab_name = lab_name
        self.references = {}
        self.reference_keys = {}
        self.bundles = {}
        self.acronyms = []

    def load(self) -> dict:

        self.references = self.__get_references()
        self.reference_keys = self.__get_reference_keys()
    
        return self

    def __get_references(self):
        references_path = f"backend/src/api/resources/{self.lab_name}/references"
        references_str = self.__concat_yaml_files(references_path)
        references_dict = yaml.load(references_str, Loader=SafeLoader)

        return references_dict

    def __get_reference_keys(self):
        return list(self.references.keys())

    def __concat_yaml_files(self, yaml_file_path) -> str:
        filenames = glob.glob(f"{yaml_file_path}/*.yaml")

        references_str = ""
        for filename in filenames:
            with open(filename, "r", encoding="latin-1") as f:
                references_str = references_str + f.read()

        return references_str
