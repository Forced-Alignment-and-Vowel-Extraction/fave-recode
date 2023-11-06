import pytest
from fave_recode.schemes import cmu2labov_path, cmu2phila_path
from pathlib import Path

class TestResoures:
    def test_cmu2labov(self):
       assert Path(cmu2labov_path).is_file()
    
    def test_cmu2phila(self):
        assert Path(cmu2phila_path).is_file()