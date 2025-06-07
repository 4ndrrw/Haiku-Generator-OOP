from haiku import Haiku
from sorted_list import SortedList
from processors.processor import Processor

# Zenizer class to replace words in a Haiku with the shortest synonym
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
