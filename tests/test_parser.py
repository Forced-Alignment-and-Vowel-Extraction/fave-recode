from fave_recode.labelset_parser import LabelSetParser, LabelSetParserProperties
from fave_recode.schemes import cmu_parser_path
from aligned_textgrid import Word, Phone, SequenceTier
from praatio.utilities.utils import Interval
from pathlib import Path
import pytest

example_property = {
    "name": "vowel",
    "exposed_as": "V",
    "default": "",
    "value_rules": [
        {
            "rule": "vowel",
            "updates": "V",
            "conditions": [
                {
                    "attribute": "label",
                    "relation": "rematches",
                    "set": "[AEIOU]"
                }
            ],
            "return": "vowel"
        }
    ]
}

example_parser = {
    "parser": "test",
    "properties": [example_property]
}


class TestProperties:

    def test_creation(self):
        property = LabelSetParserProperties(example_property)
        assert isinstance(property, LabelSetParserProperties)


class TestParser:

    seq1 = Phone(Interval(0, 1, "AH1"))
    seq2 = Phone(Interval(2, 3, "HH"))

    tier = SequenceTier(
        [
            Interval(0, 1, "AH1"),
            Interval(1, 3, "HH")
        ]
    )

    def test_creation(self):
        parser = LabelSetParser(example_parser)
        assert isinstance(parser, LabelSetParser)

    def test_apply(self):
        parser = LabelSetParser(example_parser)
        parser.apply_parser(self.seq1)
        parser.apply_parser(self.seq2)

        assert self.seq1.V == "vowel"
        assert self.seq2.V == ""

    def test_map(self):
        parser = LabelSetParser(example_parser)
        parser.map_parser(self.tier)

        assert self.tier[0].V == "vowel"
        assert self.tier[1].V == ""

    def test_default(self):
        parser = LabelSetParser()
        parser.map_parser(self.tier)
        getattr(self.tier[0], "_") == ""

    def test_read_parser(self):
        parser = LabelSetParser(parser_path=Path(cmu_parser_path))
        parser.map_parser(self.tier)

        assert self.tier[0].stress == "1"
    