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