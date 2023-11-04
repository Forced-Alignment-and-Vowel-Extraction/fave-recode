from aligned_textgrid.aligned_textgrid import AlignedTextGrid
from aligned_textgrid.sequences.word_and_phone import Word, Phone
from fave_recode.rule_classes import RuleSet
from fave_recode.schemes import all_schemes
import click
import cloup
from pathlib import Path

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
def cli(
    input_file = None,
    input_path = None,
    output_file = None,
    output_dest = None,
    scheme = None
):
    rules = get_rules(scheme)
    print(rules)


def get_rules(scheme):
    if scheme in all_schemes:
        return RuleSet(rule_path = all_schemes[scheme])
    scheme_path = Path(scheme)
    if scheme_path.is_file():
        return RuleSet(rule_path = str(scheme_path))
    raise Exception(f"Cannot find rule schema file: {scheme}")

if __name__ == "__main__":
    cli()