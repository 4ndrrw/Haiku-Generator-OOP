# Processing classes for the Haikumator application

# Base Processor class
# Synonymizer (inherits from Processor)
# Zenizer (inherits from Processor)
# Antonymizer (inherits from Processor)
# BatchProcessor (inherits from Processor)

import random
from abc import ABC, abstractmethod
from haiku import Haiku
from thesaurus import Thesaurus
from sorted_list import SortedList  # Assuming you have a SortedList implementation

# Base processor class for all haiku processors
class Processor(ABC):
  def __init__(self, haiku, thesaurus):
    self.haiku = haiku
    self.thesaurus = thesaurus

  @abstractmethod
  def process(self):
    """Process the haiku according to specific rules"""
    pass

# Antonymizer class: replaces words with antonyms (if available)
class Antonymizer(Processor):
  def display_results(self, original, processed_haiku):
      """Display before/after results"""
      print("\nThe Haiku before processing:")
      print("-" * 20)
      print(original)
      print("\nThe Antonymized Haiku after processing:")
      print("-" * 20)
      print(processed_haiku)
      print("\nPress Enter to continue...")
      input()

  def process(self):
    original = str(self.haiku)
    processed_haiku = Haiku(*self.haiku._lines)  # Make a copy

    for word in processed_haiku.get_words():
      if word.lower() in self.thesaurus:
        synonyms = self.thesaurus.get_entries(word)
        if synonyms:
          new_word = random.choice(synonyms)  # Random synonym
          processed_haiku.replace_word(word, new_word)
    self.display_results(original, processed_haiku)
    return processed_haiku

# Synonymizer class: replaces words with random synonyms
class Synonymizer(Processor):
  def display_results(self, original, processed_haiku):
      """Display before/after results"""
      print("\nThe Haiku before processing:")
      print("-" * 20)
      print(original)
      print("\nThe Synonymized Haiku after processing:")
      print("-" * 20)
      print(processed_haiku)
      print("\nPress Enter to continue...")
      input()

  def process(self):
    original = str(self.haiku)
    processed_haiku = Haiku(*self.haiku._lines)  # Make a copy

    for word in processed_haiku.get_words():
      if word.lower() in self.thesaurus:
        synonyms = self.thesaurus.get_entries(word)
        if synonyms:
          new_word = random.choice(synonyms)
          processed_haiku.replace_word(word, new_word)

    # Capitalize the first letter of each line
    for i, line in enumerate(processed_haiku._lines):
        if line:
            processed_haiku._lines[i] = line.capitalize()
    self.display_results(original, processed_haiku)
    return processed_haiku

# Zenizer class: replaces words with the shortest synonym
class Zenizer(Processor):
  def process(self):
    original = str(self.haiku)
    processed_haiku = Haiku(*self.haiku._lines)

    for word in processed_haiku.get_words():
      if word.lower() in self.thesaurus:
        synonyms = self.thesaurus.get_entries(word)
        if synonyms:
          # Use our SortedList to find shortest synonym
          sorted_syns = SortedList(synonyms, key=len)
          shortest = sorted_syns.get_shortest()
          processed_haiku.replace_word(word, shortest)

    self.display_results(original, processed_haiku)
    return processed_haiku