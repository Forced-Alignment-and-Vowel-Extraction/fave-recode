from fave_recode.rule_classes import Rule, Condition, RuleSet

class TestCondtition:

    example_condition = {
        "attribute": "label",
        "relation": "==",
        "set": "AA1"
    }

    def test_creation(self):
        this_cond = Condition(self.example_condition)
        assert this_cond