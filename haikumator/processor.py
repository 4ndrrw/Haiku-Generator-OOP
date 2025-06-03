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

# Synonymizer class: replaces words with random synonyms
class Synonymizer(Processor):
  def display_results(self, original, processed_haiku):
      """Display before/after results"""
      print("\nThe Haiku before processing:")
      print("-" * 40)
      print(original)
      print("\nThe Synonymized Haiku after processing:")
      print("-" * 40)
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
  def display_results(self, original, processed_haiku):
      """Display before/after results"""
      print("\nThe Haiku before processing:")
      print("-" * 40)
      print(original)
      print("\nThe Zen-ized Haiku after processing:")
      print("-" * 40)
      print(processed_haiku)
      print("\nPress Enter to continue...")
      input()

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
    
    # Capitalize the first letter of each line
    for i, line in enumerate(processed_haiku._lines):
        if line:
            processed_haiku._lines[i] = line.capitalize()
            
    self.display_results(original, processed_haiku)
    return processed_haiku
  
# Antonymizer class: replaces words with antonyms (if available)
class Antonymizer(Processor):
  def __init__(self, haiku, synonym_thesaurus, antonym_thesaurus):
    self.haiku = haiku
    self.synonym_thesaurus = synonym_thesaurus  # Synonym thesaurus for fallback
    self.antonym_thesaurus = antonym_thesaurus

  def display_results(self, original, processed_haiku):
    """Display before/after results"""
    print("\nThe Haiku before processing:")
    print("-" * 40)
    print(original)
    print("\nThe Antonymized Haiku after processing:")
    print("-" * 40)
    print(processed_haiku)
    print("\nPress Enter to continue...")
    input()

  def process(self):
    original = str(self.haiku)
    processed_haiku = Haiku(*self.haiku._lines)          # clone

    # ---------- build a map that points every synonym (and the key itself) ➜ canonical key
    reverse_syn = {}
    for key in self.synonym_thesaurus:
        reverse_syn[key.lower()] = key                   # map the key to itself
        for val in self.synonym_thesaurus.get_entries(key):
            reverse_syn[val.lower()] = key

    # ---------- replace each word with a random antonym (via the canonical key)
    for word in processed_haiku.get_words():
        canonical = reverse_syn.get(word.lower(), word)  # e.g. “final” ➜ “last”

        # 1️⃣ direct antonyms of the canonical form
        antonyms = self.antonym_thesaurus.get_entries(canonical)

        # 2️⃣ if none, try antonyms of its synonyms (search in reverse order)
        if not antonyms and canonical in self.synonym_thesaurus:
            for syn in reversed(self.synonym_thesaurus.get_entries(canonical)):
                antonyms = self.antonym_thesaurus.get_entries(syn)
                if antonyms:
                    break

        # 3️⃣ perform the replacement (keep original casing)
        if antonyms:
            new_word = random.choice(antonyms)
            processed_haiku.replace_word(word, new_word)

    # ---------- tidy up casing
    for i, line in enumerate(processed_haiku._lines):
        if line:
            processed_haiku._lines[i] = line.capitalize()

    self.display_results(original, processed_haiku)
    return processed_haiku