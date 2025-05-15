import pysftp
import getpass
import subprocess
import import_file

def main_menu():
    print("1) Import File")
    print("q) Quit")
    mainMenuInput = input("Please choose an option: ")
    match mainMenuInput:
    #Option 1 Import File
        case "1":
            import_file.import_file_menu()
    #Option 2
    #Last Option
        case "q":
            exit
    return mainMenuInput

def main():
    main_menu()
    
    

main()