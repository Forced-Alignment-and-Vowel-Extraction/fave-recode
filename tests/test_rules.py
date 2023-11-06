from fave_recode.rule_classes import Rule, Condition, RuleSet
from fave_recode.schemes import cmu2labov_path, cmu2phila_path
from aligned_textgrid import Word, Phone, SequenceTier
from praatio.utilities.utils import Interval
import pytest



class TestCondtition:

    example_condition = {
        "attribute": "label",
        "relation": "==",
        "set": "AA1"
    }

    example_condition2 = {
        "attribute": "inword.fol.first.label",
        "relation": "==",
        "set": "L"
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

        this_cond2 = Condition(self.example_condition2)
        assert this_cond2
    
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

class TestRule:
    example_rule = {
        "rule": "test-rule",
        "conditions": [{
            "attribute": "label",
            "relation": "==",
            "set": "AE1"
        }],
        "return": "ae"
    }

    example_rule2 = {
        "rule": "test-rule2",
        "conditions": [
            {
                "attribute": "label",
                "relation": "==",
                "set": "AA1"
            },
            {
                "attribute": "fol.label",
                "relation": "==",
                "set" : "L"
            }
        ],
        "return": "oh"
    }

    example_rule_no_return = {
        "rule": "test-rule2",
        "conditions": [{
            "attribute": "label",
            "relation": "==",
            "set": "AE1"
        }]
    }

    def test_rule_creation(self):
        this_rule = Rule(self.example_rule)
        assert this_rule

        this_rule2 = Rule(self.example_rule2)
        assert(this_rule2)

    def test_bad_rule(self):
        with pytest.raises(Exception):
            this_rule = Rule(self.example_rule_no_return)
    
    def test_rule_application(self):
        example_phone1 = Phone(Interval(0, 1, "AA1"))
        example_phone2 = Phone(Interval(0, 1, "AE1"))
        example_phone3 = Phone(Interval(1,3, "L"))
        example_phone1.set_fol(example_phone3)

        this_rule = Rule(self.example_rule)
        this_rule.apply_rule(example_phone1)
        this_rule.apply_rule(example_phone2)

        assert example_phone1.label == "AA1"
        assert example_phone2.label == "ae"

        this_rule2 = Rule(self.example_rule2)
        this_rule2.apply_rule(example_phone1)
        assert example_phone1.label == "oh"

class TestRuleSet:

    def test_read_ruleset(self):
        these_rules = RuleSet(rule_path=cmu2labov_path)
        assert these_rules

    def test_manual_ruleset(self):
        these_rules_list = [
            {
                "rule": "ae",
                "conditions": [
                    {
                        "attribute": "label",
                        "relation": "==",
                        "set": "AE1"
                    }
                ],
                "return": "ae"
            },
            {
                "rule": "oh",
                "conditions": [
                    {
                        "attribute": "label",
                        "relation": "==",
                        "set": "AO1"
                    }
                ],
                "return": "oh"
            }            
        ]

        these_rules = RuleSet(these_rules_list)
        assert these_rules

    def test_ruleset_elsewhere(self):
        # Higher up rules cannot feed lower down rules.
        these_rules_list = [
            {
                "rule": "uwl",
                "conditions": [
                    {
                        "attribute": "label",
                        "relation": "==",
                        "set": "UW"
                    },
                    {
                        "attribute": "fol.label",
                        "relation": "==",
                        "set": "L"
                    }
                ],
                "return": "uwl"
            },
            {
                "rule": "uwl2",
                "conditions": [
                    {
                        "attribute": "label",
                        "relation": "==",
                        "set": "uwl"
                    }
                ],
                "return": "x"
            }            
        ]

        uw = Phone(Interval(0,1,"UW"))
        l = Phone(Interval(1,2, "L"))
        uw.set_fol(l)

        these_rules = RuleSet(these_rules_list)
        these_rules.apply_ruleset(uw)

        assert uw.label == "uwl"
        assert uw.label != "x"

    def test_map_ruleset(self):
        cmu2labov_rules = RuleSet(rule_path=cmu2labov_path)
        AE = Interval(0,1,"AE1")
        N = Interval(1,2, "N")

        tier = SequenceTier(tier = [AE, N])
        cmu2labov_rules.map_ruleset(tier)

        assert tier.first.label == "ae"
        assert tier.first.fol.label == "N"

    def test_empty_ruleset(self):
        these_rules = RuleSet()
        this_phone = Phone(Interval(0,1,"AE"))

        these_rules.apply_ruleset(this_phone)
        assert this_phone.label == "AE"