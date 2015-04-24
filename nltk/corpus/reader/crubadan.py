from nltk.util import Index

from nltk.corpus.reader.api import *

class CrubadanCorpusReader(CorpusReader):
    def url_entries(self, languageCode):
        """
        :return: A list of urls for the desired language
        :param languageCode: The language code for the desired language
        """
        return self._entries(languageCode, "urls")

    def word_entries(self, languageCode):
        """
        :return: A list of tuples, sorted by frequencies, each containing
            a word of the desired language at index 0 and its frequency 
            at index 1
        :param languageCode: The language code for the desired language
        """
        return self._entries(languageCode, "words")

    def wordbigram_entries(self, languageCode):
        """
        :return: A list of tuples, sorted by frequencies, each containing
            an inner tuple of a bigram of the desired language at index 0
            and its frequency at index 1
        :param languageCode: The language code for the desired language
        """
        return self._entries(languageCode, "wordbigrams")

    def chartrigram_entries(self, languageCode):
        """
        :return: A list of tuples, sorted by frequencies, each containing
            a character trigram of the desired language at index 0 and 
            its frequency at index 1
        :param languageCode: The language code for the desired language
        """
        return self._entries(languageCode, "chartrigrams")

    def url_dict(self, languageCode):
        """
        :return: A dictionary with urls of the desired language
             as keys and empty strings as values
        :param languageCode: The language code for the desired language
        """
        return dict(Index([(url, "") for (url,) in self._entries(languageCode, "urls")]))

    def word_dict(self, languageCode): 
        """
        :return: A dictionary with words of the desired language
             as keys and their frequencies as values
        :param languageCode: The language code for the desired language
        """
        return dict(Index(self._entries(languageCode, "words")))

    def wordbigram_dict(self, languageCode):
        """
        :return: A dictionary with word bigrams of the desired language
             as keys and their frequencies as values
        :param languageCode: The language code for the desired language
        """ 
        return dict(Index(self._entries(languageCode, "wordbigrams")))

    def chartrigram_dict(self, languageCode):
        """
        :return: A dictionary with character trigrams of the desired 
            language as keys and their frequencies as values
        :param languageCode: The language code for the desired language
        """
        return dict(Index(self._entries(languageCode, "chartrigrams")))

    def _entries(self, languageCode, fileType):
        # Find the file id based on the language code and file type
        fileid = ""
        for f in self._fileids:
            if f.startswith((languageCode+"/", languageCode+"-")) and f.endswith("-"+fileType+".txt"): 
                fileid = f
        # Check that the file id was found
        if fileid == "":
            raise ValueError("A file for language '"+languageCode+"' of type '"+fileType+"' does not exist.")
        # Create and return the StreamBackedCorpusView        
        path = FileSystemPathPointer(self._root+"/"+fileid)
        return StreamBackedCorpusView(path, read_block, encoding=self._encoding)

# Function for the StreamBackedCorpusView
def read_block(stream):
    entries = []
    while len(entries) < 100: # Read 100 at a time.
        line = stream.readline()
        if line == '': return entries # end of file.
        pieces = line.split()
        if (len(pieces) == 1):   # file type is "urls"
            entries.append((pieces[0],))
        elif (len(pieces) == 2): # file type is "chartrigrams" or "words"
            entries.append((pieces[0], pieces[1]))
        else:                    # file type is "word bigrams"
            entries.append(((pieces[0], pieces[1]), pieces[2]))
    return entries
