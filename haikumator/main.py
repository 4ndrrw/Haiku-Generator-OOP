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
from processor import Synonymizer, Zenizer, Antonymizer, BatchProcessor
from utils import get_valid_input, validate_choice, validate_file_exists, validate_folder_exists, get_haiku_input

class HaikuGeneratorApp:
  def __init__(self):
    # Display welcome message on initialization
    self.display_welcome()
  
  # Display welcome message with student information
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

  # Main application loop
  def run(self):
    """Main application loop"""
    while True:
      # Show main menu and get user choice
      choice = self.display_main_menu()
      
      if choice == "1":
        self.handle_synonymize()
      elif choice == "2":
        self.handle_zenize()
      elif choice == "3":
        self.handle_antonymize()
      elif choice == "4":
        self.handle_batch_processing()

      # ... other options
      elif choice == "7":
        # Exit the application
        print("\nBye, thanks for using ST1507 DSAA: Haikumator")
        break
  
  # Display the main menu and validate user input
  def display_main_menu(self):
    """Display and validate main menu choice"""
    # Wait for user to press Enter after welcome screen
    input()
    menu_text = """Please select your choice: (1, 2, 3, 4, 5, 6, 7)
1. Synonymize Haiku
2. Zen-ize Haiku
3. Antonymize Haiku
4. Batch Processing
5. Extra Feature One (Haiku Validator)
6. Extra Feature Two (Haiku Mixer)
7. Exit"""

    # Prompt user for menu choice and validate input
    return get_valid_input(
      menu_text + "\nEnter choice: ",
      lambda x: validate_choice(x, ["1", "2", "3", "4", "5", "6", "7"]),
      "Please enter a number between 1 and 7."
    )

  # Handle the Synonymize option (Option 1)
  def handle_synonymize(self, haiku_file=None, thesaurus_file=None):
    """Handle synonymize option"""
    retry = True
    while retry:
      try:
        # Prompt for haiku and thesaurus files only on first run or if not provided
        if haiku_file is None:
          haiku_file = get_haiku_input()
        
        if thesaurus_file is None:
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

        # Offer to save
        self.handle_save_option(processed)

        # Ask if user wants to regenerate with same input
        retry_choice = get_valid_input(
          "\nWould you like to regenerate? (y/n): ",
          lambda x: x.lower() in ["y", "n"],
          "Please enter 'y' or 'n'."
        )

        if retry_choice.lower() == "y":
          retry = True
        else:
          retry = False
          print("Press Enter to return to main menu...")

      except Exception as e:
        print(f"An error occurred: {str(e)}")
        input("Press Enter to continue...")
        retry = False

  # Handle the Zen-ize option (Option 2)
  def handle_zenize(self, haiku_file=None, thesaurus_file=None):
    """Handle zen-ize option"""
    retry = True
    while retry:
      try:
        # Prompt for haiku file only on first run or if not provided
        if haiku_file is None:
          haiku_file = get_haiku_input()

        if thesaurus_file is None:
          thesaurus_file = get_valid_input(
            "\nSelect a synonym thesaurus file for Zen transformation.\nPlease enter input file: ",
            validate_file_exists
          )
          input("\nPress Enter to continue...")

        # Load haiku and thesaurus data
        haiku = Haiku.from_file(haiku_file)
        thesaurus = Thesaurus()
        thesaurus.load_from_file(thesaurus_file)

        # Process haiku with Zen transformation
        processor = Zenizer(haiku, thesaurus)
        processed = processor.process()

        # Offer to save
        self.handle_save_option(processed)

        # Ask if user wants to regenerate with same input
        retry_choice = get_valid_input(
          "\nWould you like to regenerate? (y/n): ",
          lambda x: x.lower() in ["y", "n"],
          "Please enter 'y' or 'n'."
        )

        if retry_choice.lower() == "y":
          retry = True
        else:
          retry = False
          print("Press Enter to return to main menu...")

      except Exception as e:
        print(f"An error occurred: {str(e)}")
        input("Press Enter to continue...")
        retry = False

  # Handle the Antonymize option (Option 3)
  def handle_antonymize(self, haiku_file=None, synonym_thesaurus_file=None, antonym_thesaurus_file=None):
    """Handle antonymize option"""
    retry = True
    while retry:
      try:
        # Prompt for haiku file if not provided
        if haiku_file is None:
          haiku_file = get_haiku_input()

        # Prompt for synonym thesaurus file if not provided
        if synonym_thesaurus_file is None:
          synonym_thesaurus_file = get_valid_input(
            "\nSelect a synonym thesaurus file.\nPlease enter input file: ",
            validate_file_exists
          )

        # Prompt for antonym thesaurus file if not provided
        if antonym_thesaurus_file is None:
          antonym_thesaurus_file = get_valid_input(
            "\nSelect an antonym thesaurus file.\nPlease enter input file: ",
            validate_file_exists
          )
          input("\nPress Enter to continue...")

        # Load haiku and thesaurus data
        haiku = Haiku.from_file(haiku_file)
        synonym_thesaurus = Thesaurus()
        synonym_thesaurus.load_from_file(synonym_thesaurus_file)
        antonym_thesaurus = Thesaurus()
        antonym_thesaurus.load_from_file(antonym_thesaurus_file)

        # Process haiku with antonyms
        processor = Antonymizer(haiku, synonym_thesaurus, antonym_thesaurus)
        processed = processor.process()

        # Offer to save
        self.handle_save_option(processed)

        # Ask if user wants to regenerate with same input
        retry_choice = get_valid_input(
          "\nWould you like to regenerate? (y/n): ",
          lambda x: x.lower() in ["y", "n"],
          "Please enter 'y' or 'n'."
        )

        if retry_choice.lower() == "y":
          retry = True
        else:
          retry = False
          print("Press Enter to return to main menu...")

      except Exception as e:
        print(f"An error occurred: {str(e)}")
        input("Press Enter to continue...")
        retry = False

  # Handle the batch processing option (Option 4)
  def handle_batch_processing(self):
    """Handle batch processing option"""
    try:
        haiku_file = get_valid_input(
            "\nSelect the Haiku you want to process\nPlease enter input file: ",
            validate_file_exists,
            "File not found. Please enter a valid filename."
        )

        thesaurus_file = get_valid_input(
            "\nSelect a synonym thesaurus.\nPlease enter input file: ",
            validate_file_exists,
            "File not found. Please enter a valid filename."
        )

        haiku = Haiku.from_file(haiku_file)
        thesaurus = Thesaurus()
        thesaurus.load_from_file(thesaurus_file)

        processor = BatchProcessor(haiku, thesaurus)
        processor.process()
        
    except Exception as e:
        print(f"\nError during batch processing: {str(e)}")
        input("\nPress Enter to continue...")

  # Handle the extra first feature options (Option 5)


  # Handle the extra second feature options (Option 6)


  # Handle the save option for processed text
  def handle_save_option(self, processed_text):
    """Offer the user to save the processed text to a file."""
    save_choice = get_valid_input(
      "Would you like to save the result to a file? (y/n): ",
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

# Start the application if this script is run directly
if __name__ == "__main__":
  # Start the application
  app = HaikuGeneratorApp()
  app.run()