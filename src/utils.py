"""
Owen Brooks
utils.py

This module provides utility functions
"""
import socket


def is_num(num):
    """check if num is a digit

    :param num: string
    :return : boolean
    """
    try:
        int(num)
    except ValueError:
        return False
    return True


def get_ip(host):
    """call dns to get ip for hostname

    :param hostname: server name
    :return : ip address
    """
    try:
        return socket.gethostbyname(host)
    except:
        raise ValueError(f"Could not get ip for host | host: {host}")


def parse_args(args):
    """parse command line args

    :param args: list of command line args
    :return : tuple (hostname, log file, port)
    """
    if len(args) < 2:
        raise ValueError(f"Not enough arguments supplied | args: {args}")
    elif len(args) > 3:
        raise ValueError(f"Too many arguments supplied | args: {args}")

    host = args[0]
    if not is_num(host[0]):  # if ip not given call dns
        host = get_ip(host)

    log_file = args[1]

    port = 21  # default port
    if len(args) == 3:
        if is_num(args[2]):
            port = int(args[2])
        else:
            raise ValueError(f"Not a valid port number | port: {args[2]}")

    return host, log_file, port
