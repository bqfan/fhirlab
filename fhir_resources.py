from fhir.resources.observation import Observation
from fhir.resources.bundle import Bundle

data1 = b"""
---
resourceType: Observation
status: preliminary
code:
  coding:
  - system: http://loinc.org
    code: 15074-8
    display: Glucose [Moles/volume] in Blood
referenceRange:
- low:
    value: 3.1
    unit: mmol/l
    system: http://unitsofmeasure.org
    code: mmol/L
  high:
    value: 6.2
    unit: mmol/l
    system: http://unitsofmeasure.org
    code: mmol/L
"""
data2 = b"""
---
resourceType: Observation
id: '8892395'
meta:
  versionId: '1'
  lastUpdated: '2023-03-28T11:47:32.696+00:00'
  source: "#kfVW4VF0cQM8qBJe"
status: final
code:
  coding:
  - system: http://loinc.org
    code: 8867-4
    display: Heart rate
subject:
  reference: Patient/7304958
effectivePeriod:
  start: '2023-03-25T20:11:00.000+00:00'
  end: '2023-03-25T20:11:00.000+00:00'
valueQuantity:
  value: 66
  unit: beats/min
  system: http://unitsofmeasure.org
  code: "/min"
"""

data3 = b"""
---

"""

observation_obj1 = Observation.parse_raw(data1, content_type="text/yaml")
observation_obj2 = Observation.parse_raw(data2, content_type="text/yaml")
bundle_obj = Bundle.parse_file("bundle.yaml", content_type="text/yaml")
print(bundle_obj)
observation = Observation.parse_file("fhir_resources_observation.yml")

# filtered_attributes = {attr: value for attr, value in observation_obj2.dict().items() if value is not None}
# print(filtered_attributes)
# filtered_observation = Observation(**filtered_attributes)
# print(type(filtered_observation))
# print(observation_obj2)
# print(observation_obj2.json(indent=True))
#print(type(observation))
json_str1 = observation_obj1.json(indent=True)
observation1 = Observation.parse_raw(json_str1)
#print(observation1)
#print(observation1.referenceRange)

observation_obj2 = Observation.parse_raw(data2, content_type="text/yaml")
json_str2 = observation_obj2.json(indent=True)
observation2 = Observation.parse_raw(json_str2)

# merged_observation = Observation()

# # Merge attributes from obs1
# merged_observation.update(obs1.as_json())
# observation2.referenceRange = observation1.referenceRange
# Assuming obs is an Observation object

# def serialize_observation(observation):
#     serialized_observation = observation.as_json()

#     # Filter out None attributes
#     filtered_observation = {key: value for key, value in serialized_observation.items() if value is not None}

#     return filtered_observation

# #print(observation2.__dict__)
# obj = observation2.__dict__
# print(obj)
# for k, v in obj.items():
#     print(k)
#     print(v)
#     if v is None:
#         #delattr(obj, k)
#         obj.__delattr__(k)

# print(obj)
#print(observation2.referenceRange)

# def merge_observations(obs1, obs2):
#     merged = Observation()

#     # Merge attributes from obs1
#     for key, value in obs1.as_json().items():
#         if hasattr(obs2, key):
#             # Handle nested attributes recursively
#             if isinstance(value, dict) and isinstance(getattr(obs2, key), dict):
#                 merged_value = merge_observations(Observation(**value), Observation(**getattr(obs2, key)))
#                 setattr(merged, key, merged_value)
#             else:
#                 setattr(merged, key, value)
#         else:
#             setattr(merged, key, value)

#     # Merge attributes from obs2 that are not in obs1
#     for key, value in obs2.as_json().items():
#         if not hasattr(obs1, key):
#             setattr(merged, key, value)

#     return merged

# print(merge_observations(observation1, observation2))
# # print(type(observation1))
# # print(observation2)
# # print(type(observation2))
# # print(dict(observation_obj1) | dict(observation_obj2))

# # def merge_observations(obs1, obs2):
# #     merged = Observation()

# #     # Merge attributes from obs1
# #     for key, value in obs1.as_json().items():
# #         if hasattr(obs2, key):
# #             # Handle nested attributes recursively
# #             if isinstance(value, dict) and isinstance(getattr(obs2, key), dict):
# #                 merged_value = merge_observations(Observation(**value), Observation(**getattr(obs2, key)))
# #                 setattr(merged, key, merged_value)
# #             else:
# #                 setattr(merged, key, value)
# #         else:
# #             setattr(merged, key, value)

# #     # Merge attributes from obs2 that are not in obs1
# #     for key, value in obs2.as_json().items():
# #         if not hasattr(obs1, key):
# #             setattr(merged, key, value)

# #     return merged
