from aligned_textgrid.sequences.sequences import SequenceInterval
from aligned_textgrid.sequences.tiers import SequenceTier
from fave_recode.ruleschema import rule_validator, \
    condition_validator, \
    label_parser_validator,\
    parser_property_validator
from fave_recode.rule_classes import RuleSet
from fave_recode.relations import relation_dict
from collections.abc import Callable
from pathlib import Path
import functools
import yaml


class LabelSetParser():
    """A labelset parser object

    Args:
        parser (dict, optional): 
            A dictionary defining the parser rules. Defaults to None.
        parser_path (Path, optional): 
            A path to a yaml file definition of the parser. Defaults to None.
    """

    def __init__(self, parser: dict = None, parser_path: Path = None):
        if parser:
            self.validate_parser(parser)
            self.name = parser["parser"]
            self.properties = [
                LabelSetParserProperties(property)
                for property in parser["properties"]
            ]
        elif parser_path:
            self.read_parser(parser_path)
        else:
            self.properties = [LabelSetParserProperties()]
        

    def apply_parser(self, obj: SequenceInterval):
        """Apply the parser to a single interval

        Args:
            obj (SequenceInterval): A SequenceInterval
        """
        for property in self.properties:
            application = property.rules.apply_ruleset(obj)
            if not application:
                obj.set_feature(
                    property.updates,
                    property.default
                )

    def map_parser(self, obj: SequenceTier):
        """Map the parser to an entire sequence tier.

        Args:
            obj (SequenceTier): A SequenceTier
        """
        for seq in obj:
            self.apply_parser(seq)

    def read_parser(self, path: Path):
        """Read in a yaml file defining the parser

        Args:
            path (Path): 
                Path to the yaml file definition.
        """
        with path.open("r") as f:
            parser = yaml.safe_load(f)
        
        self.validate_parser(parser)
        self.name = parser["parser"]
        self.properties = [
                LabelSetParserProperties(property)
                for property in parser["properties"]
            ]        


    def validate_parser(self, parser: dict):
        """Validate wellformedness of parser
        Args:
            parser (dict): parser dictionary

        Raises:
            Exception: Any errors raised by the validator
        """
        if not label_parser_validator(parser):
            errors = label_parser_validator.errors
            raise Exception(repr(errors))
        


class LabelSetParserProperties():
    """A property of the labelset, including rules that
    ought to be applied and the SequenceInterval property to update.

    Args:
        property (dict, optional): 
            A dictionary defining the property. Defaults to None.
    """

    def __init__(self, property: dict = None):
        if property:
            self.validate_property(property)
            self.rules = RuleSet(property["rules"])
            self.updates = property["updates"]
            for rule in self.rules.rules:
                rule.updates = self.updates
            self.default = property["default"]
        else:
            self.rules = RuleSet()
            self.updates = "_"
            self.default = None

    def validate_property(self, property: dict):
        """Validate wellformedness of parser property
        Args:
            parser (dict): property dictionary

        Raises:
            Exception: Any errors raised by the validator
        """
        if not parser_property_validator(property):
            errors = label_parser_validator.errors
            raise Exception(repr(errors))

