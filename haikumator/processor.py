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
    
# Season Detector class: Detects the season based on haiku content
class SeasonDetector:
    SEASON_WORDS = {
      'spring': {
        'flowers': [
          'blossom', 'cherry', 'tulip', 'daffodil', 'peach', 'plum', 'apricot', 'magnolia',
          'camellia', 'azalea', 'wisteria', 'violet', 'iris', 'peony', 'forsythia', 'pansy',
          'dandelion', 'primrose', 'snowdrop', 'crocus'
        ],
        'weather': [
          'rain', 'shower', 'breeze', 'spring', 'thaw', 'sprout', 'drizzle', 'warmth',
          'rainbow', 'sprinkle', 'fresh', 'budding', 'melt', 'awakening'
        ],
        'animals': [
          'swallow', 'frog', 'butterfly', 'lamb', 'duckling', 'bee', 'caterpillar', 'tadpole',
          'chick', 'robin', 'nest', 'songbird', 'sparrow', 'stork'
        ]
      },
      'summer': {
        'plants': [
          'hydrangea', 'lotus', 'grass', 'sunflower', 'rose', 'morning-glory', 'lily',
          'bamboo', 'watermelon', 'melon', 'corn', 'tomato', 'cucumber', 'mint', 'zinnia'
        ],
        'weather': [
          'sunshine', 'humidity', 'dry', 'summer', 'heat', 'scorch', 'swelter', 'solstice',
          'hot', 'sizzle', 'drought', 'glare','basking', 'sunstroke', 'sweat', 'sun'
        ],
        'animals': [
          'cicada', 'dragonfly', 'firefly', 'cricket', 'mosquito', 'beetle', 'ant', 'swallowtail',
          'wasp', 'swarm', 'locust', 'swim', 'fish', 'turtle'
        ]
      },
      'autumn': {
        'plants': [
          'maple', 'ginkgo', 'harvest', 'chrysanthemum', 'persimmon', 'apple', 'pumpkin',
          'acorn', 'oak', 'mushroom', 'grape', 'pomegranate', 'sweet potato', 'barley', 'wheat'
        ],
        'weather': [
          'cool', 'mist', 'dew', 'autumn', 'breeze', 'equinox', 'fog', 'crisp', 'chill',
          'fallen', 'frost', 'overcast', 'drizzle', 'gust'
        ],
        'animals': [
          'deer', 'goose', 'cricket', 'crow', 'squirrel', 'spider', 'wild goose', 'owl',
          'hawk', 'bat', 'migratory', 'hedgehog', 'fox'
        ]
      },
      'winter': {
        'plants': [
          'evergreen', 'holly', 'pine', 'camellia', 'plum', 'bamboo', 'winterberry', 'fir',
          'mistletoe', 'ivy', 'snowdrop', 'cyclamen', 'turnip', 'radish'
        ],
        'weather': [
          'snow', 'frost', 'cold', 'freeze', 'winter', 'blizzard', 'hail', 'icicle', 'chill',
          'solstice', 'shiver', 'storm', 'sleet', 'numb', 'white', 'frozen'
        ],
        'animals': [
          'owl', 'rabbit', 'fox', 'wolf', 'bear', 'deer', 'crow', 'sparrow', 'crane',
          'penguin', 'seal', 'reindeer', 'ermine', 'swan'
        ]
      }
    }

    def __init__(self, haiku):
        self.haiku = haiku
        self.season = None
        self.keywords = []

    def detect_season(self):
        """Detect the dominant season in the haiku"""
        season_counts = {season: 0 for season in self.SEASON_WORDS}
        
        for line in self.haiku._lines:
            words = line.lower().split()
            for word in words:
                clean_word = word.strip('.,!?;:')
                self._update_season_counts(clean_word, season_counts)
        
        total = sum(season_counts.values())
        if total > 0:
            self.season = max(season_counts.items(), key=lambda x: x[1])[0]
        
        return self.season

    def _update_season_counts(self, clean_word, season_counts):
        for season, categories in self.SEASON_WORDS.items():
            for category, season_list in categories.items():
                if clean_word in season_list:
                    season_counts[season] += 1
                    self.keywords.append((clean_word, season, category))

    def get_detailed_report(self):
        """Generate a detailed season analysis report"""
        if not self.season:
            return "No seasonal references detected."
        
        report = []
        report.append(f"Detected Season: {self.season.capitalize()} ")
        report.append("\nSeasonal Keywords Found:")
        
        for keyword, season, category in self.keywords:
            report.append(f"- '{keyword}' ({category}, {season})")
        
        return "\n".join(report)

#