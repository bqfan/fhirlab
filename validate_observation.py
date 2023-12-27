from fhir.resources.observation import Observation

data = {
  "resourceType": "Observation",
  "id": "8892395",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2023-03-28T11:47:32.696+00:00",
    "source": "#kfVW4VF0cQM8qBJe"
  },
  "status": "final",
  "code": {
    "coding": [ {
      "system": "http://loinc.org",
      "code": "8867-4",
      "display": "Heart rate"
    } ]
  },
  "subject": {
    "reference": "Patient/7304958"
  },
  "effectivePeriod": {
    "start": "2023-03-25T20:11:00.000+00:00",
    "end": "2023-03-25T20:11:00.000+00:00"
  },
  "valueQuantity": {
    "value": 66.0,
    "unit": "beats/min",
    "system": "http://unitsofmeasure.org",
    "code": "/min"
  }
}
observation = Observation(**data)
print(observation)