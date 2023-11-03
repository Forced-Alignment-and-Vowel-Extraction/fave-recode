from importlib.resources import files

cmu2labov_path = str(files("fave_recode").joinpath("resources", "cmu2labov.yml"))
cmu2phila_path = str(files("fave_recode").joinpath("resources", "cmu2phila.yml"))