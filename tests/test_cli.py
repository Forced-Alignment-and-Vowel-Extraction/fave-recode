from fave_recode.rule_classes import RuleSet
from fave_recode.fave_recode import get_rules
from fave_recode.schemes import all_schemes
from pathlib import Path
import pytest

class TestCLIComponents:

    def test_get_rules(self):
        rules1 = get_rules("cmu2labov")
        assert isinstance(rules1, RuleSet)

        with pytest.raises(Exception):
            get_rules("non_file")

        schwa_path = Path().joinpath("tests", "test_data", "just_schwa.yml")
        rules2 = get_rules(str(schwa_path))
        assert isinstance(rules2, RuleSet)