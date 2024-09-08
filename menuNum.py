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
    

def find_tag_files(root_dir):
    """Find all 'tag.txt' files in the directory tree starting from root_dir."""
    tag_files = []
    for root, dirs, files in os.walk(root_dir):
        if 'tag.txt' in files:
            tag_files.append(os.path.join(root, 'tag.txt'))
    return tag_files

def load_tags_from_file(tag_file_path):
    """Load tags from the given tag file path."""
    if not os.path.isfile(tag_file_path):
        return []
    with open(tag_file_path, 'r') as file:
        line = file.read().strip()
    return [tag.strip() for tag in line.split(',') if tag.strip()]

def save_tags_to_file(tag_file_path, tags):
    """Save tags to the given tag file path."""
    with open(tag_file_path, 'w') as file:
        file.write(', '.join(tags))

def create_or_edit_tag_file(directory):
    """Create or edit the 'tag.txt' file in the specified directory."""
    tag_file_path = os.path.join(directory, 'tag.txt')
    if not os.path.isfile(tag_file_path):
        print(f"'tag.txt' not found in {directory}. Creating new file.")
        open(tag_file_path, 'w').close()
    
    print(f"Editing tags in '{tag_file_path}'.")
    current_tags = load_tags_from_file(tag_file_path)
    if current_tags:
        print(f"Current tags: {', '.join(current_tags)}")
    else:
        print("No tags found.")
    
    new_tags = input("Enter new tags separated by commas: ").strip()
    new_tags_list = [tag.strip() for tag in new_tags.split(',') if tag.strip()]
    save_tags_to_file(tag_file_path, new_tags_list)
    print("Tags updated successfully.")
    input("Press Enter to continue...")

def get_publishers(root_dir):
    """Get a list of publishers that start with certain prefixes."""
    prefixes = ('$_', '$__', '#_', '#__', '__')
    publishers = [d for d in os.listdir(root_dir)
                  if os.path.isdir(os.path.join(root_dir, d)) and d.startswith(prefixes)]
    return sorted(publishers)

def get_topics(publisher_path, tags=None):
    """Get a list of topics under a publisher, optionally filtered by tags."""
    topics = [d for d in os.listdir(publisher_path) if os.path.isdir(os.path.join(publisher_path, d))]
    if tags:
        tagged_topics = set()
        for topic in topics:
            topic_path = os.path.join(publisher_path, topic)
            tag_files = find_tag_files(topic_path)
            for tag_file in tag_files:
                topic_tags = load_tags_from_file(tag_file)
                if any(tag in topic_tags for tag in tags):
                    tagged_topics.add(topic)
        return sorted(tagged_topics)
    return sorted(topics)

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

def filter_topics_by_tags(root_dir, tags):
    """Filter topics by the provided tags across all publishers."""
    filtered_topics = []
    publishers = get_publishers(root_dir)
    for publisher in publishers:
        publisher_path = os.path.join(root_dir, publisher)
        topics = get_topics(publisher_path, tags)
        for topic in topics:
            filtered_topics.append((publisher, topic))
    return filtered_topics

def menu(root_dir):
    while True:
        clear_screen()
        publishers = display_publishers(root_dir)
        choice = input("\nEnter the number, 'tags', 'exit' : ").strip()
        
        if choice.lower() == 'exit':
            break
        elif choice.lower() == 'tags':
            # Find all 'tag.txt' files in the directory tree and collect unique tags
            tag_files = find_tag_files(root_dir)
            all_tags = set()
            for tag_file in tag_files:
                all_tags.update(load_tags_from_file(tag_file))
            
            if not all_tags:
                print("No tags available to filter by.")
                input("Press Enter to continue...")
                continue

            clear_screen()
            print("\nAvailable Tags:")
            for index, tag in enumerate(sorted(all_tags)):
                print(f"{index + 1}. {tag}")
            
            tag_choice = input("\nEnter the number, 'back' : ").strip()
            
            if tag_choice.lower() == 'back':
                continue
            
            try:
                tag_index = int(tag_choice) - 1
                if 0 <= tag_index < len(all_tags):
                    selected_tag = sorted(all_tags)[tag_index]
                    filtered_topics = filter_topics_by_tags(root_dir, [selected_tag])
                    
                    if not filtered_topics:
                        print(f"No topics found with the tag '{selected_tag}'.")
                        input("Press Enter to continue...")
                        continue
                    
                    while True:
                        clear_screen()
                        print(f"\nTopics with the tag '{selected_tag}':")
                        for index, (publisher, topic) in enumerate(filtered_topics):
                            print(f"{index + 1}. [{publisher} ] ➡ {topic}")
                        
                        topic_choice = input("\nEnter the number, 'back', 'edit', 'open' : ").strip()
                        
                        if topic_choice.lower() == 'back':
                            break
                        elif topic_choice.lower() == 'open':
                            # Open the publisher directory
                            publisher_index = int(input("Enter the number to open: ").strip()) - 1
                            if 0 <= publisher_index < len(publishers):
                                publisher_path = os.path.join(root_dir, publishers[publisher_index])
                                open_directory(publisher_path)
                                input("Press Enter to return to the topic selection...")
                            continue
                        elif topic_choice.lower() == 'edit':
                            # Edit tags for the selected topic
                            topic_index = int(input("Enter the number to edit tags for: ").strip()) - 1
                            if 0 <= topic_index < len(filtered_topics):
                                publisher, topic = filtered_topics[topic_index]
                                topic_path = os.path.join(root_dir, publisher, topic)
                                create_or_edit_tag_file(topic_path)
                                continue
                            else:
                                print("Invalid topic number.")
                                input("Press Enter to continue...")
                                continue
                        
                        try:
                            topic_index = int(topic_choice) - 1
                            if 0 <= topic_index < len(filtered_topics):
                                publisher, topic = filtered_topics[topic_index]
                                topic_path = os.path.join(root_dir, publisher, topic)
                                while True:
                                    clear_screen()
                                    chapters = display_chapters(topic_path)
                                    chapter_choice = input("\nEnter the number, 'open', 'edit', 'back' : ").strip()
                                    
                                    if chapter_choice.lower() == 'back':
                                        break
                                    elif chapter_choice.lower() == 'open':
                                        open_directory(topic_path)
                                        input("Press Enter to return to the chapter selection...")
                                        continue
                                    elif chapter_choice.lower() == 'edit':
                                        create_or_edit_tag_file(topic_path)
                                        continue
                                    elif chapter_choice.lower() == 'exit':
                                        return
                                    else:
                                        try:
                                            chapter_index = int(chapter_choice) - 1
                                            if 0 <= chapter_index < len(chapters):
                                                chapter_path = os.path.join(topic_path, chapters[chapter_index])
                                                open_directory(chapter_path)
                                            else:
                                                print("Invalid chapter number.")
                                        except ValueError:
                                            print("Invalid input.")
                                        input("Press Enter to continue...")
                        except ValueError:
                            print("Invalid input.")
                            input("Press Enter to continue...")
                else:
                    print("Invalid tag number.")
                    input("Press Enter to continue...")
            except ValueError:
                print("Invalid input. Please enter a number.")
                input("Press Enter to continue...")
        else:
            try:
                publisher_index = int(choice) - 1
                if 0 <= publisher_index < len(publishers):
                    publisher_path = os.path.join(root_dir, publishers[publisher_index])
                    while True:
                        clear_screen()
                        topics = display_topics(publisher_path)
                        topic_choice = input("\nEnter the number, 'back', 'edit', 'open' : ").strip()
                        
                        if topic_choice.lower() == 'back':
                            break
                        elif topic_choice.lower() == 'open':
                            open_directory(publisher_path)
                            input("Press Enter to return to the publisher selection...")
                            continue
                        elif topic_choice.lower() == 'edit':
                            create_or_edit_tag_file(publisher_path)
                            continue
                        
                        try:
                            topic_index = int(topic_choice) - 1
                            if 0 <= topic_index < len(topics):
                                topic_path = os.path.join(publisher_path, topics[topic_index])
                                while True:
                                    clear_screen()
                                    chapters = display_chapters(topic_path)
                                    chapter_choice = input("\nEnter the number, 'open', 'edit', 'back' : ").strip()
                                    
                                    if chapter_choice.lower() == 'back':
                                        break
                                    elif chapter_choice.lower() == 'open':
                                        open_directory(topic_path)
                                        input("Press Enter to return to the chapter selection...")
                                        continue
                                    elif chapter_choice.lower() == 'edit':
                                        create_or_edit_tag_file(topic_path)
                                        continue
                                    
                                    try:
                                        chapter_index = int(chapter_choice) - 1
                                        if 0 <= chapter_index < len(chapters):
                                            chapter = chapters[chapter_index]
                                            chapter_path = os.path.join(topic_path, chapter)
                                            open_directory(chapter_path)
                                        else:
                                            print("Invalid chapter number.")
                                    except ValueError:
                                        print("Invalid input.")
                                    input("Press Enter to continue...")
                        except ValueError:
                            print("Invalid input.")
                            input("Press Enter to continue...")
                else:
                    print("Invalid publisher number.")
                    input("Press Enter to continue...")
            except ValueError:
                print("Invalid input. Please enter a number.")
                input("Press Enter to continue...")

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

