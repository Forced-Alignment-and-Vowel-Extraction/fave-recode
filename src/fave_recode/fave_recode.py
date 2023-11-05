from aligned_textgrid import AlignedTextGrid, custom_classes, Word, Phone
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
@click.option("-t", "--target_tier",
              type = click.STRING,
              help = "Target tier to recode",
              default = "Phone")
def cli(
    input_file = None,
    input_path = None,
    output_file = None,
    output_dest = None,
    scheme = None,
    save_recode = True,
    recode_stem = "_recoded",
    target_tier = "Phone"
):
    rules = get_rules(scheme)
    if input_file:
        process_file(
            input_file=input_file, 
            output_file=output_file, 
            scheme = rules, 
            recode_stem = recode_stem,
            save_recode = save_recode,
            target_tier = target_tier)

## core fave_recode operations
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
        recode_stem:str = "_recoded",
        target_tier: str = "Phone"
    ):
    input_path = Path(input_file.name)
    atg = validate_input_file(input_path)
    run_recode(atg, scheme, target_tier)

    if output_file and save_recode:
        output_path = Path(output_file)
        validate_output_file(output_path)
        atg.save_textgrid(
            save_path=str(output_path),
            format="long_textgrid"
        )
    elif save_recode:
        output_path = make_output_path(
            input_path=input_path, 
            recode_stem=recode_stem
        )
        validate_output_file(output_path)
        atg.save_textgrid(
            save_path=str(output_path),
            format="long_textgrid"
        )

## support operations
def ask_for_dir_creation(
        output_path: Path, 
        reask:bool = False
    ) -> bool:
    msg = f"The destination directory {str(output_path)} does not exist."\
          f"\n\n Create destination directory?\ty/n:\t"
    if reask:
        msg = "\nPlease enter 'y' or 'n'. \n\n" + msg
    
    dir_create = input(msg)
    if dir_create.lower()[0] == "y":
        return True
    if dir_create.lower()[0] == "n":
        return False
    
    return ask_for_dir_creation(output_path, reask=True)

def ask_for_file_overwrite(
        output_path: Path,
        reask: bool = False
    ) -> bool:
    msg = f"The file {output_path.name} already exists "\
            f"in destination directory {str(output_path.parent.resolve())} "\
            f"\n\n Overwrite?\ty/n:\t"
    if reask:
        msg = "\nPlease enter 'y' or 'n'. \n\n" + msg

    overwrite = input(msg)
    if overwrite.lower()[0] == "y":
        return True
    if overwrite.lower()[0] == "n":
        return False
    
    return ask_for_file_overwrite(output_path, reask=True)

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
         
def run_recode(
        atg: AlignedTextGrid, 
        scheme: RuleSet, 
        target_tier: str
    ):
    all_targets = [t for tgr in atg 
                   for t in tgr 
                   if t.entry_class.__name__ == target_tier]
    for tier in all_targets:
        scheme.map_ruleset(tier)

def validate_input_file(
        input_path: Path
    ) -> AlignedTextGrid:
    try:
        atg = AlignedTextGrid(textgrid_path=str(input_path),
                              entry_classes=[Word, Phone])
    except:
        if input_path.suffix != ".TextGrid":
            raise Exception(f"Problem encountered. "\
                            f"Perhaps input {str(input_path)} is not a TextGrid.")
        raise Exception(f"Problem ecountered. "\
                        f"Couldn't process input {str(input_path)}.")
    
    return atg

def validate_output_file(
        output_path: Path
    ) -> bool:
    if not output_path.parent.is_dir():
        dir_create = ask_for_dir_creation(output_path.parent)

        if not dir_create:
            raise Exception(f"Specified destination directory "\
                            f"{str(output_path.parent)} does not exist.")
        
        output_path.parent.mkdir(exist_ok=False, parents=True)

        return True

    if output_path.is_file():
        overwrite = ask_for_file_overwrite(output_path)

        if not overwrite:
            raise Exception(f"Specified output file "\
                            f"{output_path.name} already exists.")
        
        return True
    
    return True

if __name__ == "__main__":
    cli()