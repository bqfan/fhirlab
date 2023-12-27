from fhir.resources.observation import Observation
import yaml

def validate_observation_from_yaml(yaml_content):
    try:
        # Load YAML content
        observation_data = yaml.safe_load(yaml_content)

        # Create an Observation object
        observation = Observation.parse_obj(observation_data)

        # If no exception is raised, the YAML content is valid
        print("Observation YAML is valid.")
        return True

    except Exception as e:
        # Exception occurred, indicating invalid YAML content or structure
        print(f"Invalid Observation YAML: {e}")
        return False

# Sample YAML Observation content (replace this with your YAML content)
sample_yaml_observation = """
resourceType: Observation
status: final
code:
  coding:
    - system: http://loinc.org
      code: 29463-7
      display: Body Weight
subject:
  reference: Patient/123
valueQuantity:
  value: 75
  unit: kg
"""

# Call the validation function with the sample YAML content
validate_observation_from_yaml(sample_yaml_observation)
