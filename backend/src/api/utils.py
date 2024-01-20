from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
import json
from backend.src.config import settings

api_key_header = APIKeyHeader(name=settings.api_key_name, auto_error=True)

async def get_api_key(
    api_key_header: str = Security(api_key_header),
):
    if api_key_header == settings.api_key:
        return api_key_header
    else:
        raise HTTPException(status_code=403)

def __bundle_formatter(resource):
    for _, value in resource.bundles.items():
        for entry in value['entry']:
            entry['fullUrl'] = entry['fullUrl'].replace('BaseUrl', resource.base_url)
            if isinstance(entry['resource'], str):
                entry['resource'] = resource.references[entry['resource']]

def get_json(obj):
  return json.loads(
    json.dumps(obj, default=lambda o: getattr(o, '__dict__', str(o)))
  )

def __check_semantic_interoperable(observation, reference):
    reference_code = reference["code"]
    observation_code = observation["code"]

    for observation_code_coding in observation_code["coding"]:
        for reference_code_coding in reference_code["coding"]:
            if observation_code_coding["system"] == reference_code_coding["system"] and \
                observation_code_coding["code"] == reference_code_coding["code"]:

                return True
    
    return False

def __check_unit(observation, reference):
    reference_ranges = reference["referenceRange"]
    observation_value_quantity = observation["valueQuantity"]

    for reference_range in reference_ranges:
        if "high" in reference_range and "low" in reference_range and \
                observation_value_quantity["system"] == reference_range["high"]["system"] and \
                    observation_value_quantity["unit"] == reference_range["high"]["unit"] and \
                        observation_value_quantity["system"] == reference_range["low"]["system"] and \
                            observation_value_quantity["unit"] == reference_range["low"]["unit"]:
                                return True
        elif "high" in reference_range and "low" not in reference_range and \
                observation_value_quantity["system"] == reference_range["high"]["system"] and \
                    observation_value_quantity["unit"] == reference_range["high"]["unit"]:
                        return True
        elif "high" not in reference_range and "low" in reference_range and \
                observation_value_quantity["system"] == reference_range["low"]["system"] and \
                    observation_value_quantity["unit"] == reference_range["low"]["unit"]:
                        return True

        else:
            return False
