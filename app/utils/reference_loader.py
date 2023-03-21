import glob
import yaml, json
from yaml import SafeLoader

def load_references(lab_name: str="default") -> dict:
    references_str = cancatenate_yaml_files(lab_name)
    references_dict = yaml.load(references_str, Loader=SafeLoader)
    references_json = json.loads(json.dumps(references_dict))

    observations = filter_references_by_resource_type(references_json, 'Observation')
    bundles = filter_references_by_resource_type(references_json, 'Bundle')

    observation_keys = get_reference_keys(observations)
    bundle_keys = get_reference_keys(bundles)

    observation_keys_dict = {}
    for key in observation_keys:
        observation_keys_dict[key] = key

    bundle_keys_dict = {}
    for key in bundle_keys:
        bundle_keys_dict[key] = key

    references ={
        'Observation': observations,
        'Observation_keys': observation_keys_dict,
        'Bundle': bundles,
        'Bundle_keys': bundle_keys_dict
        }
    return references

def get_reference_keys(references: dict) -> dict:
    keys = list(references.keys())
    return keys

def cancatenate_yaml_files(lab_name: str) -> str:
    filenames = glob.glob("app/schemas/references/" + lab_name + "/*.yaml") + \
        glob.glob("app/schemas/references/" + lab_name + "/acronyms/*.yaml") + \
            glob.glob("app/schemas/references/" + lab_name + "/panels/*.yaml")

    references_str = ""
    for filename in filenames:
        with open(filename, "r", encoding="latin-1") as f:
            references_str = references_str + f.read()

    return references_str

def filter_references_by_resource_type(references: dict, resource_type: str) -> dict:
    filtered_references = {}
    for key, val in references.items():
        if val['resourceType'] == resource_type:
            filtered_references[key] = val

    return filtered_references
