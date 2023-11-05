from fave_recode.rule_classes import RuleSet
from aligned_textgrid import AlignedTextGrid
from fave_recode.fave_recode import get_rules, \
                                    validate_input_file
from fave_recode.schemes import all_schemes
from pathlib import Path
import pytest
import unittest.mock
class TestCLIComponents:

    def test_get_rules(self):
        rules1 = get_rules("cmu2labov")
        assert isinstance(rules1, RuleSet)

        with pytest.raises(Exception):
            get_rules("non_file")

        schwa_path = Path().joinpath("tests", "test_data", "just_schwa.yml")
        rules2 = get_rules(str(schwa_path))
        assert isinstance(rules2, RuleSet)
    
    def test_validate_input(self):
        tg_path = Path("tests/test_data/josef-fruehwald_speaker.TextGrid")
        atg1 = validate_input_file(tg_path)
        assert isinstance(atg1, AlignedTextGrid)
    
        with pytest.raises(Exception) as exec_info1:
            not_tg = Path("tests/test_data/just_schwa.yml")
            validate_input_file(not_tg)
        assert exec_info1.match("is not a TextGrid")

        with pytest.raises(Exception) as exec_info2:
            not_file = Path("fake.TextGrid")
            validate_input_file(not_file)
        assert exec_info2.match("Couldn't process input")
