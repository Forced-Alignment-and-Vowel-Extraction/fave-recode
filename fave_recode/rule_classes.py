from aligned_textgrid.sequences.sequences import SequenceInterval
from aligned_textgrid.sequences.tiers import SequenceTier
from fave_recode.ruleschema import rule_validator, condition_validator
from fave_recode.relations import relation_dict
import functools
import yaml

def rgetattr(obj: SequenceInterval, 
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


class Condition:
    """_A rule condition_

    Attributes:
        attribute (str): The attribute path for a `SequenceInterval`
        relation (Callable): The relation function to be used
    """
    def __init__(self, 
                 condition: dict):

        self.validate_condition(condition)
        self.attribute = condition["attribute"]
        self.relation = relation_dict[condition["relation"]]
        self.set = condition["set"]
    
    def __repr__(self):
        return f"runs: {self.relation.__name__}(obj.{self.attribute}, {self.set})"
    
    def validate_condition(self, condition: dict):
        if not condition_validator(condition):
            errors = condition_validator.errors
            raise Exception(repr(errors))
    
    def check_condition(
            self,
            obj:SequenceInterval
    ):
        lhs = rgetattr(obj, self.attribute)
        return self.relation(lhs, self.set)
    
class Rule:
    def __init__(
            self,
            rule: dict
    ):
        self.validate_rule(rule)
        self.conditions = [Condition(x) for x in rule["conditions"]]
        self.rule = rule["rule"]
        self.name = self.rule
        self.output = rule["return"]
    
    def __repr__(self):
        return f"rule: {self.rule} with {len(self.conditions)} conditions. returns {self.output}"
    
    def validate_rule(
            self,
            rule:dict
    ):
        if not rule_validator(rule):
            errors = rule_validator.errors
            raise Exception(repr(errors))
    
    def apply_rule(
            self,
            obj:SequenceInterval
    ):
        try:
            cond_met = [c.check_condition(obj) for c in self.conditions]
        except:
            raise Exception
        
        if all(cond_met):
            obj.label = self.output
            return True

class RuleSet:
    def __init__(
            self,
            rules: list = None, 
            rule_path: str = None
    ):
        if rules:
            self.rules = [Rule(r) for r in rules]
        elif rule_path:
            self.read_ruleset(rule_path)
    
    def __repr__(self):
        return f"A ruleset with {len(self.rules)} rules"
    
    def apply_ruleset(
            self,
            obj: SequenceInterval
    ):
        for rule in self.rules:
            application = rule.apply_rule(obj)
            ## Crucial! 
            ## First rule wins
            if application:
                break
    
    def map_ruleset(
            self,
            obj: SequenceTier
    ):
        for x in obj:
            self.apply_ruleset(x)

    def read_ruleset(
            self,
            path: str
    ):
        with(open(path)) as f:
            ruleset = yaml.safe_load(f)
        if type(ruleset) is not list:
            raise Exception(f"Rulest in {path} is not formatted correctly. \
                            Make sure it is a list.")
        self.rules = [Rule(r) for r in ruleset]
