import glob
import yaml, json
from yaml import SafeLoader

def load_references(lab_name: str="default") -> dict:
    references_str = cancatenate_yaml_files(lab_name)
    references_dict = yaml.load(references_str, Loader=SafeLoader)
    references_json = json.loads(json.dumps(references_dict))

    observations = filter_references_by_resource_type(references_json, 'Observation')
    observation_acronyms = filter_references_by_resource_type(references_json['acronyms'], 'Observation')
    observation_keys = get_reference_keys(observations)
    observation_acronyms_keys = get_reference_keys(observation_acronyms)
    
    bundles = filter_references_by_resource_type(references_json, 'Bundle')
    bundle_acronyms = filter_references_by_resource_type(references_json['acronyms'], 'Bundle')
    bundle_keys = get_reference_keys(bundles)
    bundle_acronyms_keys = get_reference_keys(bundle_acronyms)

    references ={
        'Observations': observations,
        'ObservationKeys': observation_keys,
        'ObservationAcronyms': observation_acronyms,
        'ObservationAcronymsKeys': observation_acronyms_keys,
        'Bundles': bundles,
        'BundleKeys': bundle_keys,
        'BundleAcronyms': bundle_acronyms,
        'BundleAcronymsKeys': bundle_acronyms_keys
        }

    return references

def get_reference_keys(references: dict) -> dict:
    keys = list(references.keys())
    return keys

def cancatenate_yaml_files(lab_name: str) -> str:
    filenames = glob.glob("app/resources/references/" + lab_name + "/observations/*.yaml") + \
        glob.glob("app/resources/references/" + lab_name + "/bundles/*.yaml") + \
            glob.glob("app/resources/references/" + lab_name + "/acronyms/*.yaml") 

    references_str = ""
    for filename in filenames:
        with open(filename, "r", encoding="latin-1") as f:
            references_str = references_str + f.read()

    return references_str

def filter_references_by_resource_type(references: dict, resource_type: str) -> dict:
    filtered_references = {}
    for key, val in references.items():
        if 'resourceType' in val.keys():
            if val['resourceType'] == resource_type:
                filtered_references[key] = val

    return filtered_references
