from os import path
from urllib.parse import urlparse
import warnings

from ufuncs import empty, find_file

class Genome:
    '''
    Represent a genome according to this format
    <https://github.com/igvteam/igv.js/wiki/Reference-Genome>

    This is the main class to create a JSON genome file.
    Can read .genome files and translate them to the json format
    '''
    def __init__(self, fasta, bed, **kwargs):
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
        _id = kwargs.get('id')
        _name = kwargs.get('name')
        _clever = kwargs.get('clever', False)
        _fasta = find_file(fasta)
        if _fasta is None:
            # TODO raise exception, can't proceed
            pass

        info = {
            'id': _id,
            'name': self.get_name(fasta, _name),
            'fastaURL': _fasta,
            'indexURL': self.get_fasta_index(fasta, kwargs.get('indexURL'),
                _clever),
        }

        url_keywords = ['cytobandURL', 'aliasURL']
        for keyword in url_keywords:
            info[keyword] = find_file(kwargs.get(keyword))

        info['wholeGenomeView'] = kwargs.get('wholeGenomeView', True)
        info['chromosomeOrder'] = self.get_chromosome_order(kwargs.get('chromsomeOrder'))

        track = self.build_track(bed)
        if track is not None:
            info['tracks'] = [track]

        non_none  = {key: val for key, val in info.items() if val is not None}
        valid = self.check_validity(non_none)
        if valid:
            pass
        else:
            # TODO raise error
            pass
        self.info = info

    def get_name(self, url, name):
        '''
        Returns the best name for this genome ref

        Parameters
        ---------
        url: str - file URL
        name: str - user supplied name, has priority

        Returns
        ------
        str
        name prefered name
        '''
        if not empty(name):
            return name

        purl = urlparse(url)
        return path.basename(purl.path).split('.')[0]

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
            file = self.get_fasta_index(fasta=fasta, fai=None, clever=False)
        return file

    def get_chromosome_order(self, chromosome_order):
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

        try:
            with open(chromosome_order) as f:
                chrs = f.read()
                chr_ord = chrs.splitlines()
                return chr_ord
        except FileNotFoundError as e:
            warnings.warn(f"chromosomeOrder file {chromosome_order} was\
                    supplied but wasn't found")
            return None

    def build_track(self, bed):
        '''
        Transform a bed file to a list of tracks

        Parameters
        ---------
        bed: str - the local path to the bed file

        Return
        -----
        dict
        track entry accordin to
        <https://github.com/igvteam/igv/wiki/JSON-Genome-Format#file-paths>
        returns None if bed file not found
        '''
        if find_file(bed) is None:
            return None

        return {
            "name": self.get_name(bed),
            "format": "bed",
            "url": bed
        }

    def check_validity(self, info):
        '''
        Check all obligatory properties are in the info dict

        Parameters
        ----------
        info: dict - non-None values representing genome

        Returns
        -------
        bool
        If valid or not
        '''
        musts = []
        return all(m in info for m in musts)
