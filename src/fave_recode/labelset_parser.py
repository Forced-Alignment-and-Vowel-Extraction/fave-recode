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
        for property in self.properties:
            application = property.rules.apply_ruleset(obj)
            if not application:
                obj.set_feature(
                    property.exposed_as,
                    property.default
                )

    def map_parser(self, obj: SequenceTier):
        for seq in obj:
            self.apply_parser(seq)

    def read_parser(self, path: Path):
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
    def __init__(self, property: dict = None):
        if property:
            self.validate_property(property)
            self.rules = RuleSet(property["value_rules"])
            self.exposed_as = property["exposed_as"]
            self.default = property["default"]
        else:
            self.rules = RuleSet()
            self.exposed_as = "_"
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

