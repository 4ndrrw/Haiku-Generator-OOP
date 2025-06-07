# Base Processor class
# Synonymizer (inherits from Processor)
# Zenizer (inherits from Processor)
# Antonymizer (inherits from Processor)
# BatchProcessor (inherits from Processor)

from abc import ABC, abstractmethod

# Base processor class for all haiku processors
class Processor(ABC):
  def __init__(self, haiku, thesaurus):
    self.haiku = haiku
    self.thesaurus = thesaurus

  @abstractmethod
  def process(self):
    """Process the haiku according to specific rules"""
    pass