import warnings
import argparse

from Genome import Genome
from ufuncs import warning_formatter
warnings.formatwarning = warning_formatter

def main():
    '''
        Main entry point of the program
        Parameters
        ----------
        Returns
        -------
    '''
    # TODO flags
    # k for clever
    # s for silenced
    # --bed <file>
    # --fa <fasta>
    # --fai <fasta index>
    parser = argparse.ArgumentParser(prog="IGJ", description="IGV Genome JSON\
    file creator creates IGV's genome files in the json format from fasta and\
    BED files\nRefer to https://github.com/igvteam/igv.js/wiki/Reference-Genome")

    parser.add_argument('--bed', '-b', action='store', help="path to BED file", required=True)
    parser.add_argument('--fa', '-f', action='store', help="path to fasta\
            file", metavar='FASTA', required=True)
    parser.add_argument('--fai', '-i', action='store', help="path to fasta\
        index file")
    parser.add_argument('--name', '-n', action='store', help="descriptive name")
    parser.add_argument('--id', action='store', help="UCSC or other id string")
    parser.add_argument('--chromosomeOrder', '-o', action='store',
    metavar='ORDER', help="path\
        to file containing chromosome names in new lines for the pulldown\
        selector")
    parser.add_argument('--alias', '-a', action='store', help="URL to\
        tab-delimited file defining aliases for chromosome names")
    parser.add_argument('--cytoband', '-c', action='store', help="URL to\
            cytoband ideogram file in UCSC format")
    parser.add_argument('--wholeGenomeView', '-w', action='store_false',
            help="If flag is present will NOT construct a \"whole genome\" view")
    parser.add_argument('--silence', '-s', action='store_true',
    help="Should the warnings be supressed")
    parser.add_argument('--clever', '-k', action='store_true',
            help="The program will search for a fasta index file if the\
            supplied one isn't found")
    parser.add_argument('--version', '-v', action='version', version='%(prog) v1.0.0')

    args = parser.parse_args()
    clever = True
    if clever:
        warnings.warn("Running with clever ON, this might pick a different\
                index file")
    fasta = "~/Documents/uni/2021/NSG/uORF2/genomes/merlin.fa"
    bed = "~/Documents/uni/2021/NSG/uORF2/genomes/cano_Aug2019_with_miR_with_RNA5_intron.ed"
    genome = Genome(fasta, bed, indexURL="https://a.com", clever=clever)
    print(genome.info)

if __name__ == "__main__":
    main()
