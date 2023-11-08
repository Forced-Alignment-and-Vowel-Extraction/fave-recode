from fave_recode.relations import relation_dict

class TestRelations:
    def test_in(self):
        in_rel = relation_dict["in"]
        assert in_rel("a", "abc")
        assert in_rel("a", ["a", "b", "c"])

    def test_not_in(self):
        not_in_rel = relation_dict["not in"]
        assert not_in_rel("z", "abc")
        assert not_in_rel("z", ["a", "b", "c"])

    def test_contains(self):
        contains_rel = relation_dict["contains"]
        assert contains_rel("abc", "a")
        assert contains_rel(["a", "b", "c"], "a")

    def test_excludes(self):
        excludes_rel = relation_dict["excludes"]
        assert excludes_rel("abc", 'z')
        assert excludes_rel(["a", "b", "c"], "z")

    def test_equal(self):
        equal_rel = relation_dict["=="]
        assert equal_rel("a", "a")

    def test_not_equal(self):
        nequal_rel = relation_dict["!="]
        assert nequal_rel("z", "a")

    def test_rematches(self):
        rematch_rel = relation_dict["rematches"]

        assert rematch_rel("AH0", "[0-9]")
        assert rematch_rel("Hello there!", "the")

    def test_reunmatches(self):
        unmatch_rel = relation_dict["reunmatches"]
        assert unmatch_rel("AH", "[0-9]")
        