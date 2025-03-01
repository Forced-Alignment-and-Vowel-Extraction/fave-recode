from aligned_textgrid.sequences.sequences import SequenceInterval
from aligned_textgrid.sequences.tiers import SequenceTier
from fave_recode.ruleschema import rule_validator, condition_validator
from fave_recode.relations import relation_dict
from collections.abc import Callable
import functools
import yaml
import re

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
        set (Union[str, list]): The comparison set 
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
        """Validate wellformedness of condititions

        Args:
            condition (dict): condition dictionary

        Raises:
            Exception: Any errors raised by the validator
        """
        if not condition_validator(condition):
            errors = condition_validator.errors
            raise Exception(repr(errors))
    
    def check_condition(
            self,
            obj:SequenceInterval
    )->bool:
        """_Check if the condition is met_

        Args:
            obj (SequenceInterval): The sequence interval
                against which the condition is checked

        Returns:
            (bool): True or False
        """
        lhs = rgetattr(obj, self.attribute)
        return self.relation(lhs, self.set)
    
class Rule:
    """_A rule class_

    Attributes:
        rule (str): The name of the rule
        conditions (list[Condition,...]): A  list of conditions
        output (str): The rewrite output
    """
    def __init__(
            self,
            rule: dict|'Rule'
    ):
        if isinstance(rule, Rule):
            self.conditions = rule.conditions
            self.rule = rule.rule
            self.name = rule.name
            self.output = rule.output
            self.updates = rule.updates
            return
        
        self.validate_rule(rule)
        self.conditions = [Condition(x) for x in rule["conditions"]]
        self.rule = rule["rule"]
        self.name = self.rule
        self.output = rule["return"]
        if "updates" in rule:
            self.updates = rule["updates"]
        else:
            self.updates = "label"
    
    def __repr__(self):
        return f"rule: {self.rule} with {len(self.conditions)} conditions. returns {self.output}"
    
    def validate_rule(
            self,
            rule:dict
    ):
        """_Validate the rule wellformedness_

        Args:
            rule (dict): The rule dictionary

        Raises:
            Exception: Any errors from the validator
        """
        if not rule_validator(rule):
            errors = rule_validator.errors
            raise Exception(repr(errors))
    
    def apply_rule(
            self,
            obj:SequenceInterval
    ) -> bool:
        """_Apply a single rile_

        Args:
            obj (SequenceInterval): The interval potentially being relabelled

        Raises:
            Exception: Any errors in checking the conditions

        Returns:
            (bool): `True` if the rule applied
        """
        try:
            cond_met = [c.check_condition(obj) for c in self.conditions]
        except:
            raise Exception
        
        if all(cond_met):
            output = self.parse_output(obj)
            obj.set_feature(self.updates, output)
            return True
        
    def parse_output(self, obj):
        get_features = re.findall(r"\{(.*?)\}", self.output)
        feature_dict = {
            f:rgetattr(obj, f)
            for f in get_features
        }
        output = self.output.format(**feature_dict)
        return output

class RuleSet:
    """A rule set class

    Pass `RuleSet` either a rules dictionary, or a path 
    to a rules yaml file

    Args:
        rules (list[dict,...]): A list of rule dictionaries
        rule_path (str): A path to a rules .yml file

    Attributes:
        rules (list[Rule,...]): 
    """
    def __init__(
            self,
            rules: list = [], 
            rule_path: str = None
    ):
        self.rules = []
        if rules and len(rules) > 0:
            self.rules = [Rule(r) for r in rules]
        elif rule_path:
            self.read_ruleset(rule_path)
    
    def __repr__(self):
        return f"A ruleset with {len(self.rules)} rules"

    def __add__(self, value:'RuleSet')->'RuleSet':
        if not isinstance(value, RuleSet):
            raise ValueError
        
        return RuleSet(
            rules= self.rules + value.rules
        )
    
    def apply_ruleset(
            self,
            obj: SequenceInterval
    ):
        """_Apply the ruleset_

        The rules are checked against the Sequence interval
        in sequence, and the first one applies, ceasing rule'
        application.

        Args:
            obj (SequenceInterval): The SequenceInterval undergoing rule application
        """
        for rule in self.rules:
            application = rule.apply_rule(obj)
            ## Crucial! 
            ## First rule wins
            if application:
                return True
                break
    
    def map_ruleset(
            self,
            obj: SequenceTier
    ):
        """_Apply the ruleset to all sequences_


        Args:
            obj (SequenceTier): A sequence tier to be recoded
        """
        for x in obj:
            self.apply_ruleset(x)

    def read_ruleset(
            self,
            path: str
    ):
        """_read in a ruleset_

        Args:
            path (str): A path to a ruleset

        Raises:
            Exception: Any errors in reading in the ruleset
        """
        with(open(path)) as f:
            ruleset = yaml.safe_load(f)
        if type(ruleset) is not list:
            raise Exception(f"Rulest in {path} is not formatted correctly. Make sure it is a list.")
        self.rules = [Rule(r) for r in ruleset]
