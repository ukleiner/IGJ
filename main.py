from Genome import Genome
def main():
    '''
        Main entry point of the program
        Parameters
        ----------
        Returns
        -------
    '''
    fasta = "~/Documents/uni/2021/NSG/uORF2/genomes/merlin.fa"
    bed = "~/Documents/uni/2021/NSG/uORF2/genomes/cano_Aug2019_with_miR_with_RNA5_intron.bed"
    genome = Genome(fasta, bed, indexURL="https://a.com", clever=True)
    print(genome.info)

if __name__ == "__main__":
    main()
