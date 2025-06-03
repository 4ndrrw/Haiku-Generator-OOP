# Haiku class

# Stores the 3-line poem
# Methods to parse, display, and modify lines
# Word counting functionality

class Haiku:
  def __init__(self, line1, line2, line3):
    # Initialize the Haiku with three lines
    self._lines = [line1, line2, line3]  # Encapsulated data

  @classmethod
  def from_file(cls, filename):
    """Factory method to create Haiku from file"""
    # Read the first three lines from a file and create a Haiku object
    with open(filename, 'r') as f:
      lines = [line.strip() for line in f.readlines()[:3]]
    return cls(*lines)

  def __str__(self):
    # Return the haiku as a string with lines separated by newlines
    return "\n".join(self._lines)

  def __eq__(self, other):
    # Compare two Haiku objects for equality based on their lines
    return self._lines == other._lines

  def replace_word(self, old_word, new_word):
    """Replace all occurrences of a word in the haiku"""
    # Replace old_word with new_word in all lines
    self._lines = [line.replace(old_word, new_word) for line in self._lines]

  def get_words(self):
    """Get all words in the haiku"""
    # Split all lines into words, stripping punctuation
    words = []
    for line in self._lines:
      # Simple word splitting - may need enhancement
      words.extend(word.strip(".,!?") for word in line.split())
    return words