import warnings
import argparse

from Genome import Genome
from ufuncs import warning_formatter
warnings.formatwarning = warning_formatter

def parser_creator():
    '''Creates a parser with all command line arguemnts'''
    parser = argparse.ArgumentParser(prog="IGJ", description="IGV Genome JSON\
    file creator creates IGV's genome files in the json format from fasta and\
    BED files\nRefer to https://github.com/igvteam/igv.js/wiki/Reference-Genome")

    parser.add_argument('--bed', '-b', action='store', help="REQUIRED path to BED file",
            required=True, dest="bed", metavar="URL")
    parser.add_argument('--fa', '-f', action='store', help="path to fasta\
            file", required=True, dest="fasta", metavar="URL")
    parser.add_argument('--fai', '-i', action='store', help="REQUIRED path to fasta\
        index file", dest="indexURL", metavar="URL")
    parser.add_argument('--name', '-n', action='store', help="descriptive\
            name", dest="name")
    parser.add_argument('--id', action='store', help="UCSC or other id string",
            dest="id")
    parser.add_argument('--chromosomeOrder', '-o', action='store',
    metavar='PATH', help="path\
        to file containing chromosome names in new lines for the pulldown\
        selector", dest="chromosomeOrder")
    parser.add_argument('--alias', '-a', action='store', help="URL to\
        tab-delimited file defining aliases for chromosome names",
        dest="aliasURLS", metavar="URL")
    parser.add_argument('--cytoband', '-c', action='store', help="URL to\
            cytoband ideogram file in UCSC format", dest="cytobandURL",
            metavar="URL")
    parser.add_argument('--wholeGenomeView', '-w', action='store_false',
            help="If flag is present will NOT construct a \"whole genome\"\
            view", dest="wholeGenomeView")
    parser.add_argument('--silence', '-s', action='store_true',
    help="Should the warnings be supressed", dest="silence")
    parser.add_argument('--clever', '-k', action='store_true',
            help="The program will search for a fasta index file if the\
            supplied one isn't found", dest="clever")
    parser.add_argument('--output', '-x', action='store',
            help="filename to store output overriding existing data. Without\
                    it the program will print the json", dest="output", metavar="PATH")
    parser.add_argument('--version', '-v', action='version', version='%(prog) v1.0.0')

    return parser

def main():
    '''
        Main entry point of the program
        Parameters
        ----------
        Returns
        -------
    '''
    parser = parser_creator()
    args = parser.parse_args()

    clever = args.clever
    silence = args.silence
    output = args.output

    if silence:
        warnings.filterwarnings("ignore")
    if clever:
        warnings.warn("Running with clever ON, this might pick a different index file")

    params = vars(args)
    genome = Genome(**params)
    if output is None:
        print(genome.info)
    else:
        try:
            with open(output, 'w') as f:
                f.write(genome.info)
        except PermissionError:
            warnings.warn(f"Permission denied to {output}, outputing to stdout")
            print(genome.info)

if __name__ == "__main__":
    main()
