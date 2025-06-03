class SortedList:
  def __init__(self, iterable=None, key=None):
    # Initialize the sorted list and optional key function
    self._items = []
    self._key = key or (lambda x: x)  # Default key is identity
    if iterable:
      # Add each item from the iterable, maintaining sort order
      for item in iterable:
        self.add(item)
    
  def add(self, item):
    """Add item while maintaining sort order"""
    # Compute the key value for the new item
    value = self._key(item)
    # Find the correct position to insert the item
    for i, existing in enumerate(self._items):
      if value < self._key(existing):
        self._items.insert(i, item)
        return
    # If not inserted, append to the end
    self._items.append(item)
  
  def __getitem__(self, index):
    # Allow indexing into the sorted list
    return self._items[index]
  
  def __len__(self):
    # Return the number of items in the list
    return len(self._items)
  
  def __iter__(self):
    # Allow iteration over the sorted list
    return iter(self._items)
  
  def get_shortest(self):
    """Get shortest item (first item since sorted)"""
    # Return the first item if the list is not empty, else None
    return self._items[0] if self._items else None