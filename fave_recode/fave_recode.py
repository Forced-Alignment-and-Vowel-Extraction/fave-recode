from aligned_textgrid.aligned_textgrid import AlignedTextGrid
from aligned_textgrid.sequences.word_and_phone import Word, Phone
from fave_recode.ruleschema import rule_validator, condition_validator
from fave_recode.relations import relation
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
        try:
            return getattr(obj, attr, *args)
        except:
            return ''
    return functools.reduce(_getattr, [obj] + attr.split('.'))

def validate_rules(rule: dict):
    if not rule_validator(rule):
        errors = rule_validator.errors
        raise Exception(repr(errors))
    

def validate_conditions(condition: dict):
    if not condition_validator(condition):
        errors = condition_validator.errors
        raise Exception(repr(errors))


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

def check_condition(phone, condition):
    """_Check if condition is met_

    Args:
        phone (_type_): _an alignedTextGrid.Phone object_
        condition (_type_): _A condition dictionary_
    """
    r = relation[condition["relation"]]
    lhs = rgetattr(phone, condition["attribute"])
    rhs = condition["set"]

    return(r(lhs, rhs))

def check_all_conditions(phone, conditions):
    """_check if all conditions are met_

    Args:
        phone (_type_): _an alignedTextGrid.Phone object_
        conditions (_type_): _A list of condition dictionaries_
    """
    
    all_conditions = [check_condition(phone, c) for c in conditions]
    return(all(all_conditions))

def apply_rule(phone, rule):
    """_apply a rule_

    Args:
        phone (_type_): _an alignedTextGrid.Phone object_
        rule (_type_): _a rule dictionary_
    """
    try:
     if check_all_conditions(phone, rule['conditions']):
         phone.label = rule["return"]
    except:
        raise Exception(f"Problem applying {rule['rule']} to phone {phone.tier_index}")

    # if check_all_conditions(phone, rule['conditions']):
    #     phone.label = rule['return']
    #     return(True)

def apply_ruleset(phone, ruleset):
    """_apply a ruleset_

    Args:
        phone (_type_): _an alignedTextGrid.Phone object_
        ruleset (_type_): _a list of rule dictionaries_
    """

    for rule in ruleset:
        application = apply_rule(phone, rule)
        if application:
            break

def map_ruleset(phone_tier, ruleset):
    """_map a ruleset to a phone tier_

    Args:
        phone_tier (_type_): _an alignedTextGrid.IntervalTier object__
        ruleset (_type_): _a list of rule dictionaries_
    """
    for phone in phone_tier:
        apply_ruleset(phone, ruleset)
    