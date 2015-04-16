import codecs
import re
import os

from nltk.util import Index

from nltk.corpus.reader.util import *
from nltk.corpus.reader.api import *

class CrubadanCorpusReader(CorpusReader):

    FILE_TYPES = ["urls", "chartrigrams", "wordbigrams", "words"]

    def entries(self, languageCode=None, fileType=None):
        """
        :return: the file of the specified language code and file type as
            a list containing tuples of words, word bigrams, or character trigrams
            and their frequencies or a list containing url strings
        :param languageCode: The language code of the desired file
        :param fileType: The file type of the desired file
            (i.e. 'urls', 'words', 'wordbigrams', or 'chartrigrams')
        """
        # Check the file type
        if not fileType in self.FILE_TYPES:
            raise ValueError("The file type '"+fileType+"' does not exist.")
        # Create the Path Pointer for the StreamBackedCorpusView
        for f in self._fileids:
            if (f.startswith(languageCode+"/") or f.startswith(languageCode+"-")) and f.endswith("-"+fileType+".txt"):
                path = FileSystemPathPointer(self._root+"/"+f)
                break
        # Determine the correct function to use for the StreamBackedCorpusView
        if fileType == "urls":
            func = read_one_column_block
        elif fileType == "chartrigrams" or fileType == "words":
            func = read_two_column_block
        else:
            func = read_three_column_block
        return StreamBackedCorpusView(path, func, encoding=self._encoding)

    def raw(self, languageCode, fileType):
        """
        :return: the file of the specified language code and file type as a raw string
        :param languageCode: The language code of the desired file
        :param fileType: The file type of the desired file
            (i.e. 'urls', 'words', 'wordbigrams', or 'chartrigrams')
        """
        # Check the file type
        if not fileType in self.FILE_TYPES:
            raise ValueError("The file type '"+fileType+"' does not exist.")        
        # Determine the fileid
        fileid = ''
        for f in self._fileids:
            if f.startswith(languageCode+"-") and f.endswith("-"+fileType+".txt"):
                fileid = f
                break
        return self.open(f).read()

    def words(self, languageCode, fileType):
        """
        :return: a list of all urls, words, bigrams, or trigrams defined 
            in the file of the specified language code and file type
        :param languageCode: The language code of the desired file
        :param fileType: The file type of the desired file
            (i.e. 'urls', 'words', 'wordbigrams', or 'chartrigrams')
        """
        if fileType == "urls":
            return [word for (word) in self.entries(languageCode, fileType)]
        else:
            return [word for (word, _) in self.entries(languageCode, fileType)]

    def dict(self, languageCode, fileType):
        """
        :return: the file of the specified language code and file type as a
            dictionary, whose keys are words, word bigrams, or character trigrams
            and whose values are integers representing frequencies
        :param languageCode: The language code of the desired file
        :param fileType: The file type of the desired file
            (i.e. 'urls', 'words', 'wordbigrams', or 'chartrigrams')
        """
        if fileType == "urls":
            raise ValueError("Cannot a get dict for the file type 'urls'")
        else:
            return dict(Index(self.entries(languageCode, fileType)))

    def setEncoding(self, encoding):
        """
        :param encoding: The encoding that the Corpus Reader should use
        """
        if isinstance(encoding, list):
            encoding_dict = {}
            for fileid in self._fileids:
                for x in encoding:
                    (regexp, enc) = x
                    if re.match(regexp, fileid):
                        encoding_dict[fileid] = enc
                        break
            encoding = encoding_dict
        self._encoding = encoding

# Functions for the StreamBackedCorpusView
def read_one_column_block(stream):
    entries = []
    while len(entries) < 100: # Read 100 at a time.
        line = stream.readline()
        if line == '': return entries # end of file.
        pieces = line.split()
        entries.append((pieces[0]))
    return entries

def read_two_column_block(stream):
    entries = []
    while len(entries) < 100: # Read 100 at a time.
        line = stream.readline()
        if line == '': return entries # end of file.
        pieces = line.split()
        entries.append((pieces[0], pieces[1]))
    return entries

def read_three_column_block(stream):
    entries = []
    while len(entries) < 100: # Read 100 at a time.
        line = stream.readline()
        if line == '': return entries # end of file.
        pieces = line.split()
        entries.append(((pieces[0], pieces[1]), pieces[2]))
    return entries

