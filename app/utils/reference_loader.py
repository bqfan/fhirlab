import glob
import yaml, json
from yaml import SafeLoader

def load_references(lab_name: str="default") -> dict:
    references_str = cancatenate_yaml_files(lab_name)
    references_dict = yaml.load(references_str, Loader=SafeLoader)
    references_json = json.loads(json.dumps(references_dict))
   
    #acronyms = references_json['acronyms']

    observations = filter_references_by_resource_type(references_json, 'Observation')
    observation_acronyms = filter_references_by_resource_type(references_json['acronyms'], 'Observation')
    observation_keys = get_reference_keys(observations)
    observation_acronyms_keys = get_reference_keys(observation_acronyms)
    
    bundles = filter_references_by_resource_type(references_json, 'Bundle')
    bundle_acronyms = filter_references_by_resource_type(references_json['acronyms'], 'Bundle')
    bundle_keys = get_reference_keys(bundles)
    bundle_acronyms_keys = get_reference_keys(bundle_acronyms)

    # print(panel_keys)
    # print(panel_acronyms_keys)


    observation_keys_dict = {}
    for key in observation_keys:
        observation_keys_dict[key] = key

    observation_acronyms_keys_dict = {}
    for key in observation_acronyms_keys:
        observation_acronyms_keys_dict[key] = key

    bundle_keys_dict = {}
    for key in bundle_keys:
        bundle_keys_dict[key] = key

    bundle_acronyms_keys_dict = {}
    for key in bundle_acronyms_keys:
        bundle_acronyms_keys_dict[key] = key

    references ={
        'Observations': observations,
        'ObservationKeys': observation_keys_dict,
        'ObservationAcronyms': observation_acronyms,
        'ObservationAcronymsKeys': observation_acronyms_keys_dict,
        'Bundles': bundles,
        'BundleKeys': bundle_keys_dict,
        'BundleAcronyms': bundle_acronyms,
        'BundleAcronymsKeys': bundle_acronyms_keys_dict
        }
    #print(references)
    return references

def get_reference_keys(references: dict) -> dict:
    keys = list(references.keys())
    return keys

def cancatenate_yaml_files(lab_name: str) -> str:
    filenames = glob.glob("app/schemas/references/" + lab_name + "/observations/*.yaml") + \
        glob.glob("app/schemas/references/" + lab_name + "/bundles/*.yaml") + \
            glob.glob("app/schemas/references/" + lab_name + "/acronyms/*.yaml") 

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
