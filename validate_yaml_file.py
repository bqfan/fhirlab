from fhir.resources.observation import Observation
import yaml
from jsonasobj import loads

def validate_observation_from_yaml(yaml_file_path):
    # Load the YAML file
    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)
    
    #print(yaml_data)
    # Convert YAML to JSON-like object
    # json_data = loads(yaml.dump(yaml_data))
    # print(json_data)
    # Try parsing the JSON-like object as an Observation resource
    try:
        observation = Observation.parse_obj(yaml_data)
        #print(observation)
        glucose = {"glucose": observation}
        #print(glucose["glucose"])
        print(Observation.parse_obj(glucose["glucose"]).json(indent=True))
        glucose.update({"glucose1": observation})
        # 
        #print(glucose)
        # print(glucose["glucose"])
        print("Validation successful! The YAML file contains a valid Observation resource.")
        return True
    except Exception as e:
        print(f"Validation failed: {e}")
        return False

# Replace 'path_to_your_yaml_file.yaml' with the actual path to your YAML file
yaml_file_path = 'backend/src/api/resources/default/references/glucose.yaml'
validation_result = validate_observation_from_yaml(yaml_file_path)

# if validation_result:
#     # If no exception is raised, the YAML content is valid
#     print("Observation YAML is valid.")
# else:
#     # Exception occurred, indicating invalid YAML content or structure
#     print(f"Invalid Observation YAML")

