from helpers.haiku import Haiku
from helpers.sorted_list import SortedList
from processors.processor import Processor

# Lengthener class to replace words in a Haiku with the longest synonym
class Lengthener(Processor):
  def display_results(self, original, processed_haiku):
    """Display before/after results"""
    print("\nThe Haiku before processing:")
    print("-" * 40)
    print(original)
    print("\nThe Lengthened Haiku after processing:")
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
          # Use our SortedList to find longest synonym
          sorted_syns = SortedList(synonyms, key=len)
          longest = sorted_syns.get_longest()
          processed_haiku.replace_word(word, longest)

    # Capitalize the first letter of each line
    for i, line in enumerate(processed_haiku._lines):
      if line:
        processed_haiku._lines[i] = line.capitalize()

    self.display_results(original, processed_haiku)
    return processed_haiku
