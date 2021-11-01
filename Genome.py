from os import path
from urllib.parse import urlparse

from ufuncs import empty, find_file

class Genome:
    '''
    Represent a genome according to this format
    <https://github.com/igvteam/igv.js/wiki/Reference-Genome>

    This is the main class to create a JSON genome file.
    Can read .genome files and translate them to the json format
    '''
    def __init__(self, fasta, bed, **kwargs):_id=None, name=None, cytoband=None):
        '''
            Parameters
                fasta: str - URL to fasta file
                bed: str - URL to bed file
                kwargs:
                    All properites details in the below link, using the same names
                    <https://github.com/igvteam/igv.js/wiki/Reference-Genome>
                    indexed is ignored on purpose to force fai files
                    chromosomeOrder - location of local file containg the array
                    of chromosme names

                    clever - should try the default fasta index filename when
                    fasta index supplied not found
            ----------
            Returns
            -------
        '''
        _clever = kwargs.get('clever', False)
        _fasta = find_file(fasta)
        if _fasta is None:
            # TODO raise exception, can't proceed
            pass

        info = {
            'id': _id,
            'name': self.get_name(fasta, name),
            'fastaURL': _fasta,
            'indexURL': self.get_fasta_index(fasta, kwargs.get('indexURL'),
                _clever),
        }

        url_keywords = ['cytobandURL', 'aliasURL']
        for keyword in url_keywords:
            info[keyword] = find_file(kwargs.get(keyword))
        }

        info['wholeGenomeView'] = kwargs.get('wholeGenomeView', True)
        info['chromosomeOrder'] = self.get_chromosome_order(kwargs.get('chromsomeOrder'))

        info['tracks'] = self.build_tracks(bed)



        self.info = {key: val for key, val in info.items() if val is not None}

    def get_name(self, fasta, name):
        '''
        Returns the best name for this genome ref

        Parameters
        ---------
        fasta: str - fasta file URL
        name: str - user supplied name, has priority

        Returns
        ------
        str
        name prefered name
        '''
        if not empty(name):
            return name
        url = urlparse(fasta)
        return path.base(url.path).split('.')[0]

    def get_fasta_index(self, fasta, fai, clever=False):
        '''
        Find the fasta index on the local machine

        Parameters
        ---------
        fasta: str - fasta file URL
        fai: str - fasta index URL
        clever: bool - should the function try the defualt function even if fai
        is specified?

        Returns
        ------
        str
        fasta index file name if exists, None if doesn't
        '''
        retry = clever
        if not empty(fai):
            fastai = fai
        else:
            fastai = f"{fasta}.fai"
            retry = False
        file = find_file(fastai)
        if retry and file is None:
            file = self._get_fasta_index(fasta=fasta, fai=None, clever=False)
        return file

    def get_chromosme_order(self, chromosome_order):
        '''
        Get the chromosme order array from a file

        Parameters
        ---------
        chromosome_order - path to file containing the chromsomes, each one in
        a new file

        Returns
        ------
        list[str]
        list of the chromosmes or None if the file doesn't exist
        '''
        if empty(chromosome_order):
            return None

        # TODO add excpetions
        try:
            with open(chromosome_order) as f:
                chrs = f.read()
                chr_ord = chrs.splitlines()
                return chr_ord
        except FileNotFoundError as e:
            # TODO add Warning message here, the user is expecting a read
            return None




