# Thesaurus class

# Base Thesaurus class
# SynonymThesaurus (inherits from Thesaurus)
# AntonymThesaurus (inherits from Thesaurus)
# Methods to load from file, find words, get random synonyms, etc.

# Base Thesaurus class
class Thesaurus:
  def __init__(self):
    # Encapsulated dictionary to store thesaurus data
    self._data = {}

  def load_from_file(self, filename):
    """Load thesaurus data from a file.
    Each line should be in the format: word: synonym1, synonym2, ...
    """
    with open(filename, 'r') as f:
      for line in f:
        if ':' in line:
          # Split the line into the word and its synonyms
          word, synonyms = line.split(':', 1)
          # Store the word and a list of its synonyms (all lowercased and stripped)
          self._data[word.strip().lower()] = [
            s.strip().lower() for s in synonyms.split(',')
          ]

  def get_entries(self, word):
    """Get entries (list of synonyms/antonyms) for a word (case insensitive)."""
    return self._data.get(word.lower(), [])

  def __contains__(self, word):
    """Overload 'in' operator to check if a word exists in the thesaurus."""
    return word.lower() in self._data