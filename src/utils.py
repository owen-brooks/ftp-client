"""
Owen Brooks
utils.py

This module provides helper functions
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


def parse_ftp_response(resp):
    """parse response from ftp server

    :param resp: full text of response
    :return: tuple (resp_code, respnse message)
    """
    resp_code = resp[:3]
    msg = resp[4:]
    return int(resp_code), msg


def host_is_ipv4(host):
    """determine if ip is ipv4

    :param host: ip address
    :return: True if ipv4
    """
    return "." in host


def build_port_cmd(host, port):
    """build cmd string for port cmd

    :param host: ip address
    :param port: port number
    :return: cmd string
    """
    if not host_is_ipv4(host):
        print("PORT only compatible with IPV4")
        raise ValueError

    host = ",".join(host.split("."))  # make host comma delimited
    p1 = port // 256
    p2 = port - (p1 * 256)
    return f"PORT {host},{str(p1)},{str(p2)}"


def build_eprt_cmd(host, port):
    """build cmd string for eprt cmd

    :param host: ip address
    :param port: port number
    :return: cmd string
    """
    if host_is_ipv4(host):
        return f"EPRT |1|{host}|{port}|"
    return f"EPRT |2|{host}|{port}|"


def parse_pasv_resp(resp):
    """parse port number out of pasv response

    :param resp: response from ftp server
    :return: port number
    """
    print(resp)
    resp = resp.split(",")[-2:]
    return int(resp[0]) * 256 + int(resp[1].split(")")[0])


def parse_epsv_resp(resp):
    """parse port number out of espv response

    :param resp: response from ftp server
    :return: port number
    """
    return int(resp.split("(|||")[-1].split("|)")[0])