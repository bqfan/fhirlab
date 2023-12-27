from fhir.resources.patient import Patient

data = b"""
resourceType: Patient
active: true
name:
- text: Primal Kons
  family: Kons
  given:
  - Primal
gender: male
birthDate: 2000-09-18
"""
patient_obj = Patient.parse_raw(data, content_type="text/yaml")
json_str = patient_obj.json(indent=True)
print(json_str)
