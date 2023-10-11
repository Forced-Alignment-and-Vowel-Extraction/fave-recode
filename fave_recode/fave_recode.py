from aligned_textgrid.aligned_textgrid import AlignedTextGrid
from aligned_textgrid.sequences.word_and_phone import Word, Phone
from fave_recode.ruleschema import rule_validator, condition_validator
import functools
import yaml

# https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-subobjects-chained-properties
def rgetattr(obj, 
             attr : str, 
             *args):
    """_gets object attribute from string_

    Args:
        obj (_type_): _object_
        attr (_str_): attribute path attr.attr.attr
    """
    def _getattr(obj, attr: str):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))

def validate_rules(rule: dict):
    if not rule_validator(rule):
        errors = rule_validator.errors
        raise Exception("Problem with rule")

def validate_conditions(condition: dict):
    if not condition_validator(condition):
        errors = condition_validator.errors
        raise Exception("Problem with condition")


def read_ruleset(path: str):
    """_Read in yaml rule set_

    Args:
        path (str): _path to ruleset_

    Raises:
        Exception: _ruleset errors_
    """
    with(open(path)) as f:
        ruleset = yaml.safe_load(f)

    # Check it's a list
    if type(ruleset) is not list:
        raise Exception(f"Rulest in {path} is not formatted correctly. \
                        Make sure it is a list.")

    [validate_rules(rule) for rule in ruleset]
    [validate_conditions(condition) for rule in ruleset 
        for condition in rule["conditions"]]
    
    return(ruleset)



def cmu2plotnik(phone):
    if phone.label == "AH0":
        return "@" 
    if phone.label in ["IY0", "IY1", "IY2"] and \
       phone.fol.label == "#":
        return "iyF"
    if phone.label in ["EY0", "EY1", "EY2"] and \
       phone.fol.label == "#":
        return "eyF"
    if phone.label in ["OW0", "OW1", "OW2"] and \
       phone.fol.label == "#":
        return "owF"
    if phone.label in ["AY0", "AY1", "AY2"] and \
       phone.fol.label in ['CH', 'F', 'HH', 'K',  'P', 'S', 'SH', 'T', 'TH']:
        return "ay0"
    if phone.label in ["AA0", "AA1", "AA2"] and \
       phone.inword.label.lower() in ['father', 'father', "father's",
                                'ma', "ma's", 'pa', "pa's", 'spa',
                                'spas', "spa's", 'chicago', 
                                "chicago's", 'pasta', 'bra', 'bras',
                                "bra's", 'utah', 'taco', 'tacos',
                                "taco's", 'grandfather', 'grandfathers',
                                "grandfather's", 'calm', 'calmer', 
                                'calmest', 'calming', 'calmed', 'calms',
                                'palm', 'palms', 'balm', 'balms', 'almond',
                                'almonds', 'lager', 'salami', 'nirvana',
                                'karate', 'ah']:
        return "ah"
    if phone.label in ["UW0", "UW1", "UW2"] and \
       phone.prev.label in ["AXR", "D", "DX",
                            "EL", "EN", "L", "N",
                            "R", "S", "T", "Z"]:
        return "Tuw"
    if phone.label in ["IH0", "IH1", "IH2", "IY0", "IY1", "IY2"] and\
       phone.fol.label in ["AXR", "R"]:
        return "iyr"
    if phone.label in ["EY0", "EY1", "EY2"] and\
       phone.fol.label in ["AXR", "R"]:
        return "eyr"
    if phone.label in ["AA0", "AA1", "AA2"] and \
       phone.fol.label in ["AXR", "R"]:
        return "ahr"
    if phone.label in ["AO0", "AO1", "AO2", "OW0", "OW1", "OW2"] and \
       phone.fol.label in ["AXR", "R"]:
        return "owr"    
    if phone.label in ["UH0", "UH1", "UH2", "UW0", "UW1", "UW2"] and \
       phone.fol.label in ["AXR", "R"]:
        return "uwr"
    if phone.label in ['AA0', "AA1", "AA2"]: 
        return 'o'
    if phone.label in ['AE0', "AE1", "AE2"]: 
        return 'ae'
    if phone.label in ['AH1', "AH2"]: 
        return 'uh'
    if phone.label in ['AO0', "AO1", "AO2"]: 
        return 'oh'
    if phone.label in ['AW0', "AW1", "AW2"]: 
        return 'aw'
    if phone.label in ['AY0', "AW1", "AW2"]: 
        return 'ay'
    if phone.label in ["EH0", "EH1", "EH2"]:
        return "e"    
    if phone.label in ["ER0", "Er1", "ER2"]:
        return "*hr"
    if phone.label in ['EY0', "EY1", "EY2"]: 
        return 'ey' 
    if phone.label in ["IH0", "IH1", "IH2"]:
        return "i"
    if phone.label in ["IY0", "IY1", "IY2"]:
        return "iy"
    if phone.label in ['OW0', "OW1", "OW2"]: 
        return 'ow'
    if phone.label in ["OY0", "OY1", "OY2"]:
        return "oy"
    if phone.label in ["UH0", "UH1", "UH2"]:
        return "u"
    if phone.label in ["UW0", "UW1", "UW2"]:
        return "uw"
    return phone.label