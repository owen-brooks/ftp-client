"""
CS472 – Homework  # 2
Owen Brooks
static_vars.py

This module provides static variables such as response codes,
available ftp commands, etc. used in the ftp client
"""

FTP_CMDS = {
    1: "CWD",  # Change working dir
    2: "PASV",  # Enter passive mode.
    3: "EPSV",  # Enter extended passive mode.
    4: "PORT",  # Specifies an address and port to which the server should connect.
    5: "EPRT",  # Specifies an extended address and port to which the server should connect.
    6: "RETR",  # Retrieve a copy of the file
    7: "STOR",  # Accept the data and to store the data as a file at the server site
    8: "PWD",  # Print working directory. Returns the current directory of the host.
    9: "LIST",  # Returns information of a file or directory if specified, else information of the current working directory is returned.
    10: "USER",
    11: "PASS",
    12: "QUIT",
}

CMD_PROMPT = "\nChoose a command by number ...\n"
for key, value in FTP_CMDS.items():
    CMD_PROMPT += f"{str(key)} {value}\n"

CONNECTION_SUCCESS = 220
LOGIN_SUCCESS = 230
EXIT = 221
TIMEOUT = 421
