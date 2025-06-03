# Entry point for the Haikumator application

"""
Main entry point for the Haikumator application.

This script displays a welcome screen with student information and presents a main menu loop with the following options:
  1. Synonymize: Process input files to replace words with their synonyms.
  2. Zen-ize: Apply a 'Zen' transformation to the input files.
  3. Antonymize: Replace words in the input files with their antonyms.
  4. Batch process: Perform batch processing on multiple input files.
  5/6. Extra features: Additional functionalities as defined.
  7. Exit: Terminate the application.

For each menu option, the application follows a similar workflow:
  - Prompt the user to provide input files.
  - Process the files according to the selected option.
  - Display the results to the user.
  - Offer the option to save the results.
  - Allow the user to repeat the process if desired.
"""

import os
import random
from haiku import Haiku
from thesaurus import Thesaurus
from processor import Synonymizer, Zenizer, Antonymizer
from utils import get_valid_input, validate_choice, validate_file_exists, get_haiku_input

class HaikuGeneratorApp:
  def __init__(self):
    # Display welcome message on initialization
    self.display_welcome()
    
  def display_welcome(self):
    # Print welcome banner and student info
    print('************************************************************')
    print('* ST1507 DSAA: Welcome to:                                 *')
    print('*                                                          *')
    print('*  ~ Haikumator - Haiku Generator Application~             *')
    print('*----------------------------------------------------------*')
    print('*                                                          *')
    print('*  - Done by: Andrew Pang (2423708)                        *')
    print('*  - Class DAAA/2A/04                                      *')
    print('************************************************************')
    print()
    print()
    print('Press Enter, to continue...')

  def run(self):
    """Main application loop"""
    while True:
      # Show main menu and get user choice
      choice = self.display_main_menu()
      
      if choice == "1":
        self.handle_synonymize()
      elif choice == "2":
        self.handle_zenize()
      # ... other options
      elif choice == "7":
        # Exit the application
        print("\nBye, thanks for using ST1507 DSAA: Haikumator")
        break
        
  def display_main_menu(self):
    """Display and validate main menu choice"""
    # Wait for user to press Enter after welcome screen
    input()
    menu_text = """
Please select your choice: (1, 2, 3, 4, 5, 6, 7)
1. Synonymize Haiku
2. Zen-ize Haiku
3. Antonymize Haiku
4. Batch Processing
5. Extra Feature One (Haiku Validator)
6. Extra Feature Two (Haiku Mixer)
7. Exit
"""
    # Prompt user for menu choice and validate input
    return get_valid_input(
      menu_text + "\nEnter choice: ",
      lambda x: validate_choice(x, ["1", "2", "3", "4", "5", "6", "7"]),
      "Please enter a number between 1 and 7."
    )

  def handle_synonymize(self):
    """Handle synonymize option"""
    try:
      # Prompt for haiku and thesaurus files
      haiku_file = get_haiku_input()
      thesaurus_file = get_valid_input(
        "\nSelect a synonym thesaurus.\nPlease enter input file: ",
        validate_file_exists
      )
      input("\nPress Enter to continue...")
      
      # Load haiku and thesaurus data
      haiku = Haiku.from_file(haiku_file)
      thesaurus = Thesaurus()
      thesaurus.load_from_file(thesaurus_file)
      
      # Process haiku with synonyms
      processor = Synonymizer(haiku, thesaurus)
      processed = processor.process()
      
      # Offer to save and retry
      self.handle_save_option(processed)
      self.handle_retry_option(self.handle_synonymize)
      
    except Exception as e:
      # Handle any errors gracefully
      print(f"An error occurred: {str(e)}")
      input("Press Enter to continue...")

  def handle_save_option(self, processed_text):
    """Offer the user to save the processed text to a file."""
    print("\nProcessed Result:\n")
    print(processed_text)
    save_choice = get_valid_input(
      "\nWould you like to save the result to a file? (y/n): ",
      lambda x: x.lower() in ["y", "n"],
      "Please enter 'y' or 'n'."
    )
    if save_choice.lower() == "y":
      filename = input("Enter filename to save to: ").strip()
      try:
        with open(filename, "w", encoding="utf-8") as f:
          f.write(str(processed_text))
        print(f"Result saved to {filename}")
      except Exception as e:
        print(f"Failed to save file: {e}")
    else:
      print("Result not saved.")

  def handle_retry_option(self, retry_func):
    """Ask the user if they want to retry the operation."""
    retry_choice = get_valid_input(
      "\nWould you like to give this another try? (y/n): ",
      lambda x: x.lower() in ["y", "n"],
      "Please enter 'y' or 'n'."
    )
    if retry_choice.lower() == "y":
      retry_func()
    else:
      print("Returning to main menu...")

if __name__ == "__main__":
  # Start the application
  app = HaikuGeneratorApp()
  app.run()