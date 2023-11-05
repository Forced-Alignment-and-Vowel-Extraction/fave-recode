from aligned_textgrid.aligned_textgrid import AlignedTextGrid
from aligned_textgrid.sequences.word_and_phone import Word, Phone
from fave_recode.rule_classes import RuleSet
from fave_recode.schemes import all_schemes
from pathlib import Path
from typing import Union
import click
import cloup
import io

@cloup.command()
@cloup.option_group("Inputs", 
    cloup.option("-i", "--input_file", 
                 type = click.File('r'),
                 help="single input file"),
    cloup.option("-p", "--input_path", 
                 type = click.Path(exists=True),
                 help="Path to a set of files"),
    help= "File inputs. Either a single file with -i or a path with -p. Not both.", 
    constraint=cloup.constraints.RequireAtLeast(1)
)
@cloup.option_group("Outputs",
    cloup.option("-o", "--output_file",
                 type=click.STRING,
                 help = "An output file name"),
    cloup.option("-d", "--output_dest",
                 type = click.Path(exists=False),
                 help = "An output directory")
)
@cloup.constraint(
    cloup.constraints.mutually_exclusive,
    ["input_file", "input_path"]
)
@cloup.constraint(
    cloup.constraints.mutually_exclusive,
    ["output_file", "output_dest"]
)
@cloup.constraint(
    cloup.constraints.mutually_exclusive,
    ["input_file", "output_dest"]
)
@cloup.constraint(
    cloup.constraints.mutually_exclusive,
    ["input_path", "output_file"]
)
@click.option("-s", "--scheme",
              type=click.STRING,
              help = "Recoding scheme."\
                " Built in options are cmu2labov and cmu2phila",
            required = True)
@click.option("-r", "--recode_stem",
              type = click.STRING,
              help = "Stem to append to recoded TextGrid file names",
              default = "_recoded")
def cli(
    input_file = None,
    input_path = None,
    output_file = None,
    output_dest = None,
    scheme = None,
    save_recode = True,
    recode_stem = "_recoded"
):
    rules = get_rules(scheme)
    if input_file:
        process_file(
            input_file=input_file, 
            output_file=output_file, 
            scheme = rules, 
            recode_stem = recode_stem,
            save_recode = save_recode)


def get_rules(
        scheme: str
    ) -> RuleSet:
    if scheme in all_schemes:
        return RuleSet(rule_path = all_schemes[scheme])
    scheme_path = Path(scheme)
    if scheme_path.is_file():
        return RuleSet(rule_path = str(scheme_path))
    raise Exception(f"Cannot find rule schema file: {scheme}")

def process_file(
        input_file: io.TextIOWrapper, 
        output_file: str, 
        scheme: RuleSet,
        save_recode: bool,
        recode_stem:str = "_recoded"
    ):
    input_path = Path(input_file.name)
    atg = validate_input_file(input_path)
    if output_file and save_recode:
        output_path = Path(output_file)
    elif save_recode:
        output_path = make_output_path(
            input_path=input_path, 
            recode_stem=recode_stem
        )
    print(output_path)
    #validate_output_file(output_path)

def validate_input_file(
        input_path: Path
    ) -> AlignedTextGrid:
    try:
        atg = AlignedTextGrid(textgrid_path=str(input_path))
    except:
        if input_path.suffix != ".TextGrid":
            raise Exception(f"Problem encountered. "\
                            f"Perhaps input {str(input_path)} is not a TextGrid.")
        raise Exception(f"Problem ecountered. "\
                        f"Couldn't process input {str(input_path)}.")
    
    return atg

def make_output_path(
        input_path: Path,
        recode_stem: str,
        output_path: Union[Path, None] = None,
) -> Path:
    input_stem = input_path.stem

    if output_path is None:
        output_file_path= input_path.with_stem(input_stem+recode_stem)
        return output_file_path

    if output_path.suffix == "":
        new_name = input_path.with_stem(input_stem+recode_stem).name
        return output_path.joinpath(new_name)

    raise Exception(f"Provided output path {output_path} looks like a file name")
        
    
    

def validate_output_file(output_path):
    pass

if __name__ == "__main__":
    cli()