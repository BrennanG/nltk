import re

from nltk.util import Index

from nltk.corpus.reader.util import *
from nltk.corpus.reader.api import *

class CrubadanCorpusReader(CorpusReader):

    _FILE_TYPES = ["urls", "chartrigrams", "wordbigrams", "words"]

    def entries(self, languageCode, fileType):
        """
        :return: the file of the specified language code and file type as
            a list containing tuples of words, word bigrams, or character trigrams
            and their frequencies or a list containing url strings
        :param languageCode: The language code of the desired file
        :param fileType: The file type of the desired file
            (i.e. 'urls', 'words', 'wordbigrams', or 'chartrigrams')
        """
        self._check_file_type(fileType)
        path = FileSystemPathPointer(self._root+"/"+self._get_file_id(languageCode, fileType))
        return StreamBackedCorpusView(path, read_block, encoding=self._encoding)

    def raw(self, languageCode, fileType):
        """
        :return: the file of the specified language code and file type as a raw string
        :param languageCode: The language code of the desired file
        :param fileType: The file type of the desired file
            (i.e. 'urls', 'words', 'wordbigrams', or 'chartrigrams')
        """
        self._check_file_type(fileType)
        fileid = self._get_file_id(languageCode, fileType)
        return self.open(fileid).read()

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
            raise ValueError("Cannot a get dict for the file type 'urls'.")
        else:
            return dict(Index(self.entries(languageCode, fileType)))

    def set_encoding(self, encoding):
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

    def _check_file_type(self, fileType):
        """
        Checks the validity of the fileType
        """
        if not fileType in self._FILE_TYPES:
            raise ValueError("The file type '"+fileType+"' does not exist.")

    def _get_file_id(self, languageCode, fileType):
        """
        Returns the file id based on the language code and the file type
        If the file does not exist, raises an error
        """
        for f in self._fileids:
            if (f.startswith(languageCode+"/") or f.startswith(languageCode+"-")) and f.endswith("-"+fileType+".txt"): 
                return f
        raise ValueError("A file for language '"+languageCode+"' of type '"+fileType+"' does not exist.")

# Function for the StreamBackedCorpusView
def read_block(stream):
    entries = []
    while len(entries) < 100: # Read 100 at a time.
        line = stream.readline()
        if line == '': return entries # end of file.
        pieces = line.split()
        if (len(pieces) == 1): # file type is "urls"
            entries.append((pieces[0]))
        elif (len(pieces) == 2): # file type is "chartrigrams" or "words"
            entries.append((pieces[0], pieces[1]))
        else: # file type is "word bigrams"
            entries.append(((pieces[0], pieces[1]), pieces[2]))
    return entries

