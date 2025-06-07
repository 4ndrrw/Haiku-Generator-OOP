import random
from haiku import Haiku
from processors.processor import Processor

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
