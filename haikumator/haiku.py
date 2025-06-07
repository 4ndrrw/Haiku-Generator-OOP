# Haiku class

# Stores the 3-line poem
# Methods to parse, display, and modify lines
# Word counting functionality

class Haiku:
    def __init__(self, line1="", line2="", line3=""):
        self._lines = [line1, line2, line3]
        
    @classmethod
    def from_file(cls, filename):
        """Create Haiku from file"""
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines()[:3]]
        return cls(*lines)
        
    def __str__(self):
        return "\n".join(self._lines)
        
    def replace_word(self, old_word, new_word):
        """Replace words while preserving original case and punctuation"""
        for i in range(len(self._lines)):
            words = self._lines[i].split()
            for j in range(len(words)):
                # Compare without punctuation
                clean_word = words[j].rstrip('.,!?;:').lower()
                if clean_word == old_word.lower():
                    # Preserve original capitalization and punctuation
                    if words[j][0].isupper():
                        new_word_cased = new_word.capitalize()
                    else:
                        new_word_cased = new_word.lower()
                    
                    # Preserve punctuation
                    punctuation = words[j][len(clean_word):]
                    words[j] = new_word_cased + punctuation
            self._lines[i] = ' '.join(words)
        
    def get_words(self):
        """Get all unique words in haiku (lowercase, no punctuation)"""
        words = set()
        for line in self._lines:
            words.update(word.rstrip('.,!?;:').lower() for word in line.split())
        return words