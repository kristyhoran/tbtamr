import pathlib, argparse, sys, os, logging
from tbtamr.AmrSetup import SetuptbAMR

from tbtamr.version import __version__

"""
tbtamr is designed to implement TB-profiler and parse the results compatible for MDU use. It may also be used for other purposes where the format of output is compatible

"""

def run_pipeline(args):
    P = SetuptbAMR(args)
    input_data = P.setup()
    T = RunProfiler(input_data)
    amr_data = T.run()
    

def mdu(args):
   pass


def set_parsers():
    parser = argparse.ArgumentParser(
        description="Genomic AMR prediction pipeline for Mtb", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    
    subparsers = parser.add_subparsers(help="Task to perform")
    parser_sub_run = subparsers.add_parser('run', help='Run abritamr', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_sub_run.add_argument(
        "--read1",
        "-r1",
        default="",
        help="Path to read1 - not required if tab-delimited file (--data) provided.",
    )
    parser_sub_run.add_argument(
        "--read2",
        "-r2",
        default="",
        help="Path to read2 - not required if tab-delimited file (--data) provided.",
    )
    parser_sub_run.add_argument(
        "--prefix",
        "-px",
        default="tbtamr",
        help="If running on a single sample, please provide a prefix for output directory",
    )
    parser_sub_run.add_argument(
        "--data",
        "-d",
        default="",
        help="Tab-delimited file with sample ID as column 1 and path to read1 and read2 as column 2 and 3. ",
    )
    parser_sub_run.add_argument(
        "--jobs", 
        "-j", 
        default=1, 
        help="Number of TB-profile jobs to run in parallel - strongly recommended to limit this to < 4. THIS IS NOT CPUS. Each TB-profiler job will be allocated 8 cpus."
    )
    parser_sub_run.add_argument(
        "--database", 
        "-db", 
        default='tbdb', 
        help="Database of drug-resistance mutations."
    )
    # parser_sub_run.add_argument(
    #     "--amrfinder_db", 
    #     "-d", 
    #     default=f"{os.environ.get('AMRFINDER_DB')}", 
    #     help="Path to amrfinder DB to use"
    # )
    
    

    
    
    parser_sub_run.set_defaults(func=run_pipeline)
    # parser_mdu.set_defaults(func = mdu)
    args = parser.parse_args()
    return args


def main():
    """
    run pipeline
    """

    args = set_parsers()
    if vars(args) == {}:
        parser.print_help(sys.stderr)
    else:
        args.func(args)
    

if __name__ == "__main__":
    main()
