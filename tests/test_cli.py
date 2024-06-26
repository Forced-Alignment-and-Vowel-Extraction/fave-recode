from fave_recode.rule_classes import RuleSet
from aligned_textgrid import AlignedTextGrid, Word, Phone
from fave_recode.fave_recode import get_rules, \
                                    process_directory,\
                                    process_file,\
                                    ask_for_dir_creation,\
                                    ask_for_file_overwrite, \
                                    get_target_list,\
                                    make_output_path,\
                                    run_recode,\
                                    validate_input_file,\
                                    validate_output_file
from fave_recode.schemes import all_schemes
from fave_recode.labelset_parser import LabelSetParser
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

    def test_process_file(self, monkeypatch):
        # mocking input from click

        real_file = "tests/test_data/josef-fruehwald_speaker.TextGrid"
        real_path = Path(real_file)
        schwa_scheme = "tests/test_data/just_schwa.yml"
        scheme = RuleSet(rule_path=schwa_scheme)

        ratg = process_file(
            input_path = real_path,
            scheme = scheme,
            save_recode=False,
            target_tier="Phone"
        )

        assert isinstance(ratg, AlignedTextGrid)

        # testing recode saving without naming an output file
        try:
            input_sequence = iter(["y"])
            monkeypatch.setattr(
                    "builtins.input", 
                    lambda _:next(input_sequence)
            )            
            recode_stem = "_recoded"
            output_path = make_output_path(
                real_path,
                recode_stem=recode_stem
            )
            ratg = process_file(
                input_path = real_path,
                scheme = scheme,
                save_recode = True,
                recode_stem = recode_stem,
                target_tier = "Phone"
            )

            assert output_path.is_file()
            assert output_path.parent == real_path.parent
        finally:
            output_path.unlink()

        # testing recode when output file provided
        try:
            output_file = "tests/test_data/here.TextGrid"
            output_path = Path(output_file)
            ratg = process_file(
                input_path = real_path,
                output_file = output_file,
                scheme = scheme,
                save_recode = True,
                target_tier = "Phone"
            )

            assert output_path.is_file()

        finally:
            output_path.unlink()

        # testing recode when output file is in 
        # non-existing directory
        try:
            output_file = "tests/test_data/non_dir/here.TextGrid"
            output_path = Path(output_file)
            ratg = process_file(
                input_path = real_path,
                output_file = output_file,
                scheme = scheme,
                save_recode = True,
                target_tier = "Phone"
            )

            assert output_path.is_file()            
        finally:
            output_path.unlink()
            output_path.parent.rmdir()

    def test_process_directory(self, monkeypatch: pytest.MonkeyPatch):

        scheme = get_rules("tests/test_data/just_schwa.yml")
        ratg_list = process_directory(
            input_path="tests/test_data",
            scheme = scheme,
            save_recode=False
        )
        assert isinstance(ratg_list[0], AlignedTextGrid)

        input_sequence = iter(["y"])
        monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))
        tg_list = get_target_list(Path("tests/test_data"))
        output_paths = [
            make_output_path(
                tg, 
                recode_stem = "_recoded", 
                output_path=Path("tests/test_data/foo")
            )
            for tg in tg_list
        ]

        try:
            process_directory(
                input_path="tests/test_data",
                output_dest="tests/test_data/foo",
                scheme=scheme,
                recode_stem="_recoded",
                save_recode=True
            )
            for op in output_paths:
                assert op.is_file()
        finally:
            for op in output_paths:
                op.unlink()
            output_paths[0].parent.rmdir()


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

    def test_get_targets(self):
        tg_dir = "tests/test_data/"
        tg_dir_path = Path(tg_dir)

        not_tg_path = Path()

        text_grids = get_target_list(tg_dir_path)
        assert len(text_grids) > 0

        with pytest.raises(Exception):
            get_target_list(not_tg_path)

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
        parser = LabelSetParser()
        target_tier = "Phone"

        run_recode(atg, parser, scheme, target_tier)
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
        monkeypatch.setattr(
            "builtins.input", 
            lambda _:next(input_sequence)
            )
        output_path = Path("fake_path/Output.TextGrid")

        try:
            did_it = validate_output_file(output_path=output_path)
            assert did_it
        finally:
            output_path.parent.rmdir()
        
        input_sequence = iter(["n"])
        monkeypatch.setattr(
            "builtins.input", 
            lambda _:next(input_sequence)
            )
        
        with pytest.raises(Exception):
            validate_output_file(Path("fake_path/Output.TextGrid"))
