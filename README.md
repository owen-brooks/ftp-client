# HW2 FTP Client
> ftp client in python

Owen Brooks

## Requirements

* python3

## How to use
To see example usage using the Drexel FTP server simply run:

```
make run
```

This will create and use a log file: **ftp.log**

To run using your own specified server and log file use the following convention:

```
python3 run.py <server-name> <log-file> <port>
```

*Note: the port argument is optional - port 21 is used by default*

The UI looks like this:
```
Choose a command by number ...
1 CWD
2 PASV
3 EPSV
4 PORT
5 EPRT
6 RETR
7 STOR
8 PWD
9 LIST
10 USER
11 PASS
12 QUIT

> 
```

Simply enter the number of the command you wish to run. For commands that require additional arguments, the program will prompt the user for the values accordingly.

An example of a sample run can be found in the file **sample_run.txt**. The corresponding log file can be found in the file **ftp.log**

## Questions

1. Think about the conversation of FTP – how does each side validate the other (on the
connection and data ports – think of each separately)? How do they trust that they’re getting
a connection from the right person? Or to the right servers? 

ANSWER: The server validate the user on the connection by requesting a user name and password in order to access the resources. The user is connecting to the servers ip address - this ensures it is connecting with the right server. On the data side the server either recieves or supplies a port number for the data connection. This is communicated over the control connection and allows the two parties to know "where" they will be sending data back and forth. The appropriate party can then accept the connection on that port and thus know who they are communicating with.

2. How does your client know that it’s sending the right commands in the right order? How
does it know the sender is trustworthy? What happened when you didn’t send the right
messages or send them in the wrong order? 

ANSWER: The client knows it sending messages in the right order because the order is defined the FTP RFC. If it does not use the right order it will get error response. For example if you try to send a LIST command without first specifying the data connection it will send you a response you need to run PASV or PORT first and set up that connection. If you dont send them in the right order the UI will default back to the command choice state. Things like entering username and password must be done in a certain order otherwise the response will prompt the user to re-enter the commands
