# Thesaurus class

# Base Thesaurus class
# SynonymThesaurus (inherits from Thesaurus)
# AntonymThesaurus (inherits from Thesaurus)
# Methods to load from file, find words, get random synonyms, etc.

# Base Thesaurus class
class Thesaurus:
  def __init__(self):
    self._data = {}

  def load_from_file(self, filename):
    """Load thesaurus data from file"""
    with open(filename, 'r') as f:
      for line in f:
        if ':' in line:
          word, synonyms = line.split(':', 1)
          self._data[word.strip().lower()] = [
            s.strip().lower() for s in synonyms.split(',')
          ]

  def get_entries(self, word):
    """Get entries for a word (case insensitive)"""
    return self._data.get(word.lower(), [])

  def __contains__(self, word):
    return word.lower() in self._data

  def __iter__(self):
    """Iterate over words in the thesaurus"""
    return iter(self._data)