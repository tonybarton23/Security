import pysftp
import getpass
import main

def connect_sftp():
    hostname = input("Enter Hostname: ")
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    try:
        with pysftp.Connection(hostname, username=username, password=password) as sftp:
            print("Connection Successful")
    except pysftp.ConnectionException as e:
        print(f"Connection Error: {e}")
    except IOError as e:
        print(f"File operation error: {e}")

def import_file_menu():
    print("1) SFTP")
    print("2) HTTP")
    print("q) Go Back")
    importFileSelection = input("Please Select an Option: ")
    match importFileSelection:
        case "1":
            connect_sftp()
        case "q":
            print("Testing")
            main.main_menu()


