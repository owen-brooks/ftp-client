# ftp-client
> simple sockets based ftp client in python

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

