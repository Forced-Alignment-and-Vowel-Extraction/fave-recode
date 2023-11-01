from fave_recode.rule_classes import Rule, Condition, RuleSet
from aligned_textgrid import Word, Phone
from praatio.utilities.utils import Interval
import pytest



class TestCondtition:

    example_condition = {
        "attribute": "label",
        "relation": "==",
        "set": "AA1"
    }

    example_bad_condition = {
        "attribute": "label.len",
        "relation": "==",
        "set": "AA1"
    }

    sample_phone1 = Phone(Interval(0, 1, "AA1"))
    sample_phone2 = Phone(Interval(1, 2, "AE1"))

    sample_phone1.set_fol(sample_phone2)

    def test_creation(self):
        this_cond = Condition(self.example_condition)
        assert this_cond
    
    def test_bad_creation(self):
        with pytest.raises(Exception):
            this_cond = Condition(self.example_bad_condition)
    
    def test_check(self):
        this_cond = Condition(self.example_condition)
        assert this_cond.check_condition(self.sample_phone1)
        assert not this_cond.check_condition(self.sample_phone2)
    
    def test_condition_attr(self):
        this_cond = Condition(self.example_condition)
        assert type(this_cond.attribute) is str
        assert callable(this_cond.relation)
        assert type(this_cond.set) in [str, list]