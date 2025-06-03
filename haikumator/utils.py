import os

# Input validation utilities

def get_valid_input(prompt, validation_func, error_msg="Invalid input. Please try again."):
  """
  Prompt the user for input and validate it using the provided validation function.
  Repeats until valid input is received.

  Args:
    prompt (str): The message displayed to the user.
    validation_func (callable): Function to validate the input.
    error_msg (str): Message displayed on invalid input.

  Returns:
    str: The validated user input.
  """
  while True:
    user_input = input(prompt).strip()
    if validation_func(user_input):
      return user_input
    print(error_msg)

def validate_file_exists(filename):
  """
  Check if a file exists at the given path.

  Args:
    filename (str): Path to the file.

  Returns:
    bool: True if file exists, False otherwise.
  """
  return os.path.isfile(filename)

def validate_choice(choice, valid_options):
  """
  Validate if the user's choice is within the allowed options.

  Args:
    choice (str): The user's input.
    valid_options (iterable): Allowed options.

  Returns:
    bool: True if choice is valid, False otherwise.
  """
  return choice in valid_options

def get_haiku_input():
  """
  Prompt the user to enter a haiku filename and validate its existence.

  Returns:
    str: The validated filename.
  """
  return get_valid_input(
    "\nSelect the Haiku you want to process\nPlease enter input file: ",
    validate_file_exists,
    "File not found. Please enter a valid filename."
  )