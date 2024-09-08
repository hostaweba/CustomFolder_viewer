import os
import subprocess
import sys
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
    return sorted([d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d)) and d.startswith('__')])

def get_topics(publisher_path):
    """Get a list of topics under a publisher."""
    return sorted([d for d in os.listdir(publisher_path) if os.path.isdir(os.path.join(publisher_path, d))])

def get_chapters(topic_path):
    """Get a list of chapters under a topic."""
    return sorted([d for d in os.listdir(topic_path) if os.path.isdir(os.path.join(topic_path, d))])

def count_files(chapter_path):
    """Count files in a chapter."""
    return len([f for f in os.listdir(chapter_path) if os.path.isfile(os.path.join(chapter_path, f))])

def display_topics(topics):
    """Display the list of topics."""
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

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def search_topics(root_dir, search_query):
    """Search for topics across all publishers that match the search query with at least 3 characters."""
    search_query = search_query.lower()
    matched_topics = []
    publishers = get_publishers(root_dir)
    
    for publisher in publishers:
        publisher_path = os.path.join(root_dir, publisher)
        topics = get_topics(publisher_path)
        for topic in topics:
            if search_query in topic.lower() and len(search_query) >= 3:
                matched_topics.append((topic, publisher_path))
    
    return sorted(matched_topics)

def open_directory(path):
    """Open the directory in the file explorer."""
    if os.name == 'nt':  # Windows
        os.startfile(path)
    elif os.name == 'posix':  # macOS and Linux
        subprocess.run(['open', path] if sys.platform == 'darwin' else ['xdg-open', path])

def menu(root_dir):
    while True:
        clear_screen()
        search_query = input("\nEnter a topic search query (at least 3 characters) or type 'exit' to quit: ").strip()
        
        if search_query.lower() == 'exit':
            break
        
        if len(search_query) < 3:
            print("Search query must be at least 3 characters long.")
            input("Press Enter to continue...")
            continue
        
        matched_topics = search_topics(root_dir, search_query)
        
        if not matched_topics:
            print("No topics found.")
            input("Press Enter to search again...")
            continue
        
        while True:
            clear_screen()
            print("\nMatching Topics:")
            for index, (topic, _) in enumerate(matched_topics):
                print(f"{index + 1}. {topic}")
            
            topic_choice = input("\nEnter the number of the topic you want to choose, 'search' to search again, or 'exit' to quit: ").strip()
            
            if topic_choice.lower() == 'search':
                break
            elif topic_choice.lower() == 'exit':
                return
            else:
                try:
                    topic_index = int(topic_choice) - 1
                    if 0 <= topic_index < len(matched_topics):
                        topic, publisher_path = matched_topics[topic_index]
                        topic_path = os.path.join(publisher_path, topic)
                        
                        while True:
                            clear_screen()
                            chapters = display_chapters(topic_path)
                            chapter_choice = input("\nEnter the number of the chapter you want to choose, 'open' to open topic directory, or 'back' to go back: ").strip()
                            
                            if chapter_choice.lower() == 'exit':
                                return
                            elif chapter_choice.lower() == 'open':
                                open_directory(topic_path)
                                print(f"Opened directory: {topic_path}")
                                input("Press Enter to continue...")
                            elif chapter_choice.lower() == 'back':
                                break
                            else:
                                try:
                                    chapter_index = int(chapter_choice) - 1
                                    if 0 <= chapter_index < len(chapters):
                                        chapter = chapters[chapter_index]
                                        chapter_path = os.path.join(topic_path, chapter)
                                        open_directory(chapter_path)
                                        print(f"Opened directory: {chapter_path}")
                                        input("Press Enter to continue...")
                                    else:
                                        print("Invalid chapter number.")
                                        input("Press Enter to continue...")
                                except ValueError:
                                    print("Invalid input. Please enter a number.")
                                    input("Press Enter to continue...")
                    else:
                        print("Invalid topic number.")
                        input("Press Enter to continue...")
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    input("Press Enter to continue...")




csv_file = 'address.csv'  # Path to your CSV file
try:
    target_dir_name = get_directory_name_from_csv(csv_file)
    root_directory = find_root_directory(os.getcwd(), target_dir_name)
    menu(root_directory)
except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)






