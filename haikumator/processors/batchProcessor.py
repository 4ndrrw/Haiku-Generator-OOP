import os
from itertools import product
from helpers.haiku import Haiku
from processors.processor import Processor

# BatchProcessor class: Create all possible alternatives of an existing haiku
class BatchProcessor(Processor):
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
