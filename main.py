import subprocess
from os import system
import platform

'''
----------------------------
For Windows , Mac and Linux
-----------------------------

The subprocess module is cross-platform and works similarly on Windows, macOS, and Linux.
Python handles the command execution uniformly across different platforms using this module.
'''
def clear_screen():
    # Get the current operating system
    current_os = platform.system()

    if current_os == 'Windows':
        subprocess.run('cls', shell=True)
    else:  # For macOS and Linux
        subprocess.run('clear', shell=True)
        
def display_menu():
    clear_screen()
    print("Menu:")
    print("1. Input by Number")
    print("2. Input by Name")
    print("3. Search")
    print("4. Exit")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            subprocess.run(['python', 'menuNum.py'])
        elif choice == '2':
            subprocess.run(['python', 'menuName.py'])
        elif choice == '3':
            subprocess.run(['python', 'search.py'])
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please select a number between 1 and 4.")

if __name__ == "__main__":
    main()
