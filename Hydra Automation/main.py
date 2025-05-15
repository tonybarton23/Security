import pysftp
import getpass
import subprocess

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
