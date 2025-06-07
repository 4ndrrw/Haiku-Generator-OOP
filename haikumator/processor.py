# Processing classes for the Haikumator application

# Base Processor class
# Synonymizer (inherits from Processor)
# Zenizer (inherits from Processor)
# Antonymizer (inherits from Processor)
# BatchProcessor (inherits from Processor)

import random
import os
from itertools import product
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

  def _build_reverse_syn_map(self):
    reverse_syn = {}
    for key in self.synonym_thesaurus:
        reverse_syn[key.lower()] = key                   # map the key to itself
        for val in self.synonym_thesaurus.get_entries(key):
            reverse_syn[val.lower()] = key
    return reverse_syn

  def _find_antonyms(self, word, reverse_syn):
    canonical = reverse_syn.get(word.lower(), word)
    antonyms = self.antonym_thesaurus.get_entries(canonical)
    if not antonyms and canonical in self.synonym_thesaurus:
        for syn in reversed(self.synonym_thesaurus.get_entries(canonical)):
            antonyms = self.antonym_thesaurus.get_entries(syn)
            if antonyms:
                break
    return antonyms

  def process(self):
    original = str(self.haiku)
    processed_haiku = Haiku(*self.haiku._lines)          # clone

    reverse_syn = self._build_reverse_syn_map()

    for word in processed_haiku.get_words():
        antonyms = self._find_antonyms(word, reverse_syn)
        if antonyms:
            new_word = random.choice(antonyms)
            processed_haiku.replace_word(word, new_word)

    for i, line in enumerate(processed_haiku._lines):
        if line:
            processed_haiku._lines[i] = line.capitalize()

    self.display_results(original, processed_haiku)
    return processed_haiku
  
# BatchProcessor class: Create all possible alternatives of an existing haiku
class BatchProcessor:
    def __init__(self, haiku, thesaurus):
        self.haiku = haiku
        self.thesaurus = thesaurus
        
    def process(self):
        """Generate all possible permutations of the haiku"""
        # Get all replaceable words with their synonyms
        replaceable_words = {}
        for word in self.haiku.get_words():
            if word in self.thesaurus:
                synonyms = self.thesaurus.get_entries(word)
                if synonyms:
                    replaceable_words[word] = synonyms
        
        if not replaceable_words:
            print("No replaceable words found in thesaurus.")
            input("Press Enter to continue...")
            return None
        
        # Get output folder
        folder = input("\nSelect an existing folder to store the batch processed haikus\n"
                      "Please enter the folder name: ").strip()
        while not os.path.isdir(folder):
            print("Folder not found. Please enter an existing directory.")
            folder = input("Please enter the folder name: ").strip()
        
        input('\nPress Enter to start batch processing...\n')
        print("\nBatch processing started!")
        
        # Generate all possible combinations
        words = list(replaceable_words.keys())
        synonym_lists = [replaceable_words[word] for word in words]
        
        # Process each combination
        count = 0
        for combo in product(*synonym_lists):
            processed_haiku = Haiku(*self.haiku._lines)
            for word, replacement in zip(words, combo):
                processed_haiku.replace_word(word, replacement)
            
            # Save to file with v{number}.txt naming
            filename = os.path.join(folder, f"v{count+1}.txt")
            with open(filename, 'w') as f:
                f.write(str(processed_haiku))
            
            print('.', end='', flush=True)
            count += 1
        
        print(f"\nBatch processing completed with {count} permutations")
        print("Press Enter to continue....")
        return count