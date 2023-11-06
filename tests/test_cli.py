from fave_recode.rule_classes import RuleSet
from aligned_textgrid import AlignedTextGrid, Word, Phone
from fave_recode.fave_recode import get_rules, \
                                    ask_for_dir_creation,\
                                    ask_for_file_overwrite, \
                                    make_output_path,\
                                    run_recode,\
                                    validate_input_file,\
                                    validate_output_file
from fave_recode.schemes import all_schemes
from pathlib import Path
import pytest

class TestCLIComponents:

    ## core fave_recode operations
    def test_get_rules(self):
        rules1 = get_rules("cmu2labov")
        assert isinstance(rules1, RuleSet)

        with pytest.raises(Exception):
            get_rules("non_file")

        schwa_path = Path().joinpath("tests", "test_data", "just_schwa.yml")
        rules2 = get_rules(str(schwa_path))
        assert isinstance(rules2, RuleSet)

    ## support operations
    def test_ask_for_dir_creation(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr("builtins.input", lambda _: "y")
        test1 = ask_for_dir_creation(Path())
        assert test1

        monkeypatch.setattr("builtins.input", lambda _: "n")
        assert not ask_for_dir_creation(Path())

        input_sequence = iter(["ok", "YES"])
        monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))
        assert ask_for_dir_creation(Path())

    def test_ask_for_file_overwrite(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr("builtins.input", lambda _: "y")
        test1 = ask_for_file_overwrite(Path())
        assert test1

        monkeypatch.setattr("builtins.input", lambda _: "n")
        assert not ask_for_file_overwrite(Path())

        input_sequence = iter(["ok", "YES"])
        monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))
        assert ask_for_file_overwrite(Path())

    def test_make_output(self):
        input_path = Path("dir/input.TextGrid")
        recode_stem = "_recoded"
        output_path = Path("output")

        path1 = make_output_path(
            input_path=input_path, 
            recode_stem=recode_stem
        )

        assert path1.name == "input_recoded.TextGrid"
        assert path1.parent == input_path.parent

        path2 = make_output_path(
            input_path=input_path,
            recode_stem=recode_stem,
            output_path=output_path
        )

        assert path2.name == "input_recoded.TextGrid"
        assert path2.parent == output_path

        with pytest.raises(Exception):
            make_output_path(
                input_path=input_path,
                recode_stem=recode_stem,
                output_path="fake.TextGrid"
            )

    def test_run_recode(self):

        atg_path = Path().joinpath(
            "tests", 
            "test_data",
            "josef-fruehwald_speaker.TextGrid"
            )
        atg = AlignedTextGrid(
            textgrid_path=str(atg_path),
            entry_classes=[Word, Phone]
            )
        schwa_path = Path().joinpath(
            "tests",
            "test_data",
            "just_schwa.yml"
        )
        scheme = RuleSet(rule_path=str(schwa_path))
        target_tier = "Phone"

        run_recode(atg, scheme, target_tier)
        ptier = atg[0].Phone
        schwa_ints = [x for x in ptier if x.label == "@"]
        assert len(schwa_ints) > 0

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

    def test_validate_output_file(self, monkeypatch):
        input_sequence = iter(["y"])
        monkeypatch.setattr("builtins.input", lambda _:next(input_sequence))
        output_path = Path("fake_path/Output.TextGrid")

        try:
            did_it = validate_output_file(output_path=output_path)
            assert did_it
        finally:
            output_path.parent.rmdir()
