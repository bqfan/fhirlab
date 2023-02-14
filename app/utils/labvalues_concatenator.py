import glob
import yaml, json

def concatenate(lab_name="default"):
    filenames = glob.glob("app/schemas/labvalues/" + lab_name + "/*.yaml")
    labvalues={}

    for file in filenames:
        with open(file) as f:
            labvalue = json.loads(json.dumps(yaml.full_load(f), sort_keys=True, indent=2))
            labvalues = dict(labvalues, **labvalue)
    # print("/////////////////////////////////////////////////////")
    # print(labvalues["Lipid Panel"])

    return labvalues
