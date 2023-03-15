import glob
import yaml, json

def concatenate(lab_name="default"):
    filenames = glob.glob("app/schemas/labvalues/" + lab_name + "/*.yaml") + \
        glob.glob("app/schemas/labvalues/" + lab_name + "/acronyms/*.yaml") + \
            glob.glob("app/schemas/labvalues/" + lab_name + "/panels/*.yaml")
            

    labvalues_str = ""
    for filename in filenames:
        with open(filename, "r", encoding="latin-1") as f:
            labvalues_str = labvalues_str + f.read()

    labvalues_dict = yaml.full_load(labvalues_str)
    labvalues = json.loads(json.dumps(labvalues_dict, sort_keys=True, indent=2))

    return labvalues
