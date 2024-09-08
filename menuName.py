import os
import subprocess
import sys
import difflib
import csv

# ----------------------------------------------
def get_directory_name_from_csv(csv_file):
    """
    Get the directory name from the first row of the CSV file.
    
    Args:
        csv_file (str): Path to the CSV file.
    
    Returns:
        str: The directory name from the first row.
    """
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            first_row = next(reader, None)
            if first_row and first_row[0]:
                return first_row[0]
            else:
                raise ValueError("CSV file is empty or has no valid rows.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        raise

def find_root_directory(start_dir, target_dir_name):
    """Find the target directory starting from the start_dir and moving up through parent directories."""
    current_dir = os.path.abspath(start_dir)
    while True:
        potential_root = os.path.join(current_dir, target_dir_name)
        if os.path.isdir(potential_root):
            return potential_root
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            break
        current_dir = parent_dir
    raise FileNotFoundError(f"Directory '{target_dir_name}' not found.")
    
#----------------------------------------------    

def get_publishers(root_dir):
    """Get a list of publishers."""
    prefixes = ['__', '$_', '$__', '#_', '#__']
    return sorted([d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d)) and any(d.startswith(prefix) for prefix in prefixes)])

def get_topics(publisher_path):
    """Get a list of topics under a publisher."""
    return sorted([d for d in os.listdir(publisher_path) if os.path.isdir(os.path.join(publisher_path, d))])

def get_chapters(topic_path):
    """Get a list of chapters under a topic."""
    return sorted([d for d in os.listdir(topic_path) if os.path.isdir(os.path.join(topic_path, d))])

def count_files(chapter_path):
    """Count files in a chapter."""
    return len([f for f in os.listdir(chapter_path) if os.path.isfile(os.path.join(chapter_path, f))])

def display_publishers(root_dir):
    """Display the list of publishers."""
    publishers = get_publishers(root_dir)
    print("\nAvailable Publishers:")
    for index, publisher in enumerate(publishers):
        print(f"{index + 1}. {publisher}")
    return publishers

def display_topics(publisher_path):
    """Display the list of topics under a selected publisher."""
    topics = get_topics(publisher_path)
    print("\nAvailable Topics:")
    for index, topic in enumerate(topics):
        print(f"{index + 1}. {topic}")
    return topics

def display_chapters(topic_path):
    """Display the list of chapters under a selected topic."""
    chapters = get_chapters(topic_path)
    print("\nAvailable Chapters:")
    for index, chapter in enumerate(chapters):
        file_count = count_files(os.path.join(topic_path, chapter))
        print(f"{index + 1}. [{file_count} Files] - {chapter}")
    return chapters

def open_directory(path):
    """Open the directory in the file explorer."""
    if os.name == 'nt':  # Windows
        os.startfile(path)
    elif os.name == 'posix':  # macOS and Linux
        subprocess.run(['open', path] if sys.platform == 'darwin' else ['xdg-open', path])

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def find_matches(query, choices):
    """Find matches for a query in a list of choices, case-insensitive, and include substring matches."""
    query = query.lower()
    choices_lower = [choice.lower() for choice in choices]
    
    # Find matches based on fuzzy matching
    fuzzy_matches = difflib.get_close_matches(query, choices_lower, n=10, cutoff=0.5)
    
    # Find matches based on substring inclusion
    substring_matches = [choice.lower() for choice in choices if query in choice.lower()]
    
    # Combine fuzzy matches and substring matches, ensuring unique results
    combined_matches = set(fuzzy_matches + substring_matches)
    
    # Map combined matches back to original choices
    result_matches = []
    for match in combined_matches:
        if match in choices_lower:
            result_matches.append(choices[choices_lower.index(match)])
        else:
            # If the match is from substring_matches, directly append
            result_matches.extend([choice for choice in choices if match in choice.lower()])
    
    return list(set(result_matches))

def prompt_for_choice(prompt, choices):
    """Prompt the user for a choice and return the best match or handle multiple matches."""
    while True:
        choice = input(prompt).strip()
        if choice.lower() == 'back':
            return None
        elif choice.lower() == 'open':
            return 'open'
        elif choice.lower() == 'exit':
            return 'exit'       
            
        matches = find_matches(choice, choices)
        if not matches:
            print("No matching item found. Please try again.")
        elif len(matches) == 1:
            return matches[0]
        else:
            print("Multiple matches found:")
            for i, match in enumerate(matches):
                print(f"{i + 1}. {match}")
            
            while True:
                match_choice = input("Enter the number of your choice, or 'back' to go back: ").strip()
                if match_choice.lower() == 'back':
                    return None
                if match_choice.isdigit():
                    index = int(match_choice) - 1
                    if 0 <= index < len(matches):
                        return matches[index]
                print("Invalid choice. Please try again.")

def menu(root_dir):
    while True:
        clear_screen()
        publishers = display_publishers(root_dir)
        choice = prompt_for_choice("Enter the name of the publisher you want to choose, or 'exit' to quit: ", publishers)
        
        if choice == 'exit':
            break
        elif choice:
            publisher_path = os.path.join(root_dir, choice)
            
            while True:
                clear_screen()
                topics = display_topics(publisher_path)
                topic_choice = prompt_for_choice("Enter the name of the topic you want to choose, 'open' to open the publisher directory, or 'back' to go back: ", topics)
                
                if topic_choice == 'open':
                    open_directory(publisher_path)
                    input("Press Enter to return to the topic selection...")
                    continue
                elif topic_choice == 'back':
                    break
                elif topic_choice == 'exit':
                    return
                elif topic_choice is None:
                    break
                
                topic_path = os.path.join(publisher_path, topic_choice)
                
                while True:
                    clear_screen()
                    chapters = display_chapters(topic_path)
                    chapter_choice = prompt_for_choice("Enter the name of the chapter you want to choose, 'open' to open the topic directory, or 'back' to go back: ", chapters)
                    
                    if chapter_choice == 'open':
                        open_directory(topic_path)
                        input("Press Enter to return to the chapter selection...")
                        continue
                    elif chapter_choice == 'back':
                        break
                    elif chapter_choice == 'exit':
                        return
                    elif chapter_choice is None:
                        break

                    
                    chapter_path = os.path.join(topic_path, chapter_choice)
                    open_directory(chapter_path)
                    input("Press Enter to return to the chapter selection...")
        else:
            print("No matching publisher found.")
            input("Press Enter to continue...")

# Find the root directory
if __name__ == "__main__":
    csv_file = 'address.csv'  # Path to your CSV file
    try:
        target_dir_name = get_directory_name_from_csv(csv_file)
        root_dir = find_root_directory(os.getcwd(), target_dir_name)
        menu(root_dir)
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)
