"""
Owen Brooks
ftp_client.py

This module contains the client module, with the main processing loop
"""
import socket

from .utils import *
from .static_vars import *


class Client:
    """ FTP client object"""

    def __init__(self, logger):
        """Init method for ftp client object"""
        self._logger = logger
        self._control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._data_socket = None
        self._host = None
        self._client = socket.gethostbyname(socket.gethostname())
        self._passive = False

    def _read_resp(self):
        """read resp from control socket

        :return: response
        """
        f = self._control_socket.makefile("r")
        resp = f.readline()
        self._logger.info(f"Recieved: {resp.rstrip()}")
        f.close()
        return resp

    def connect(self, host, port):
        """connect socket to server

        :param host: ip of server
        :param port: port number
        :return: True if connection successfull, false if not
        """
        try:
            self._logger.info(f"Connecting to {host} on port {port}")
            self._control_socket.connect((host, port))
            resp = self._read_resp()
            if parse_ftp_response(resp)[0] == CONNECTION_SUCCESS:
                self._logger.info(f"Recieved: {resp}")
                self._host = host
                return True
        except:
            pass
        self._logger.info(f"Failed to connect to {host} on port {port}")
        return False

    def _set_up_data_socket(self, port, local=False):
        """Create data socket

        :param port: port #
        :param local: if connection should be locally or on server
        """
        if self._data_socket:
            self._data_socket.close()
        self._data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if local:
                self._passive = False
                self._data_socket.bind((socket.gethostname(), port))
                self._data_socket.listen(1)

            else:
                self._passive = True
                self._data_socket.connect((self._host, port))
            print(f"New data connection created on port {port}")
        except Exception as e:
            self._logger.info(e)
            print(f"Failed to create data connection on port {port}")

    def _handle_data_socket(self, cmd):
        """Manage the data socket connection

        :param cmd: cmd that requires data socket
        """
        if not self._passive:
            try:
                self._data_socket = self._data_socket.accept()[0]
            except:
                print("Active mode not correctly set up ...")
                return
        f = self._data_socket.makefile("r")
        data = ""
        if "STOR" in cmd:
            try:
                local_f = open(input("> FILE PATH ON LOCAL: "), "r")
                data = local_f.read() + "\r\n"
                local_f.close()
                self._data_socket.send(data.encode())
                print("Sucessfull stored file ...")
            except Exception as e:
                self._logger.info(f"ERROR: {e}")
                print("Failed to read local file ...")

        else:
            line = f.readline()
            while line:
                data += line
                line = f.readline()
            if cmd == "LIST":
                print(data)
            elif "RETR" in cmd:
                try:
                    local_f = open(input("> FILE PATH ON LOCAL: "), "w")
                    local_f.write(data)
                    local_f.close()
                    print("Sucessfull retrieved file ...")
                except Exception as e:
                    self._logger.info(f"ERROR: {e}")
                    print("Failed to read local file ...")

    def _send_cmd(self, socket, cmd_str):
        """Send cmd to socket

        :param socket: socket object
        :param cmd_str: CMD w/o carriage return 
        """
        self._logger.info(f"Sent: {cmd_str}")
        try:
            socket.send(f"{cmd_str}\r\n".encode())
        except Exception as e:
            self._logger.info(f"ERROR: {e}")
            raise

    def _login(self,):
        """Control flow to login to ftp server, takes username and password

        :return: True if login success, False otherwise
        """
        self._send_cmd(self._control_socket, "USER " + input("USERNAME: "))
        self._read_resp()
        self._send_cmd(self._control_socket, "PASS " + input("PASSWORD: "))
        password_resp = self._read_resp()
        if parse_ftp_response(password_resp)[0] == LOGIN_SUCCESS:
            return True
        return False

    def _get_cmd(self):
        """Take user inputs and format ftp cmd

        :return: ftp command, port if active mode
        """
        print(CMD_PROMPT)
        try:
            user_choice = int(input("> "))
            if user_choice in range(1, 13):
                cmd = FTP_CMDS[user_choice]
                if cmd in ["PORT", "EPRT"]:
                    port = int(input("> PORT (less than 65535): "))
                    if 0 > port > 65535:
                        print("> Invalid port ...")
                        raise ValueError
                    if cmd == "PORT":
                        return build_port_cmd(self._client, port), port
                    else:
                        return build_eprt_cmd(self._client, port), port
                elif cmd in ["RETR", "STOR"]:
                    return f"{cmd} {input('> FILE PATH ON SERVER: ')}", None
                elif cmd == "CWD":
                    return f"{cmd} {input('> DIR: ')}", None
                elif cmd in ["USER", "PASS"]:
                    return f"{cmd} {input('> '+cmd + ': ')}", None
                else:
                    return cmd, None

        except ValueError:
            pass

        return self._get_cmd()

    def run(self):
        """main processing loop for client"""
        if not self._login():
            print("Login failed ... closing connection to host")
            self._logger.info("Closing connection to host.")
            self._control_socket.close()
            return

        keep_alive = True
        while keep_alive:
            cmd, port = self._get_cmd()
            if port:  # set up data socket for active connections
                self._set_up_data_socket(port, local=True)

            try:
                self._send_cmd(self._control_socket, cmd)
                resp_code, msg = parse_ftp_response(self._read_resp())

                if resp_code in [
                    550,
                    EXIT,
                    425,
                    257,
                    TIMEOUT,
                    250,
                    500,
                    331,
                    230,
                    530,
                    200,
                    503,
                ]:
                    print(msg.rstrip())
                    if resp_code in [EXIT, TIMEOUT]:
                        keep_alive = False
                elif resp_code == 200:  # PASV
                    self._set_up_data_socket(port, local=True)
                elif resp_code == 227:  # PASV
                    port = parse_pasv_resp(msg)
                    self._set_up_data_socket(port)
                elif resp_code == 229:  # EPSV
                    port = parse_epsv_resp(msg)
                    self._set_up_data_socket(port)
                elif resp_code == 150:  # Data!
                    self._handle_data_socket(cmd)
                    self._data_socket.close()
                    self._data_socket = None
                    ack_code, ack_resp = parse_ftp_response(self._read_resp())
                else:
                    raise ValueError(
                        f"Unhandled response code: {resp_code}, msg: {msg}"
                    )

            except TimeoutError as e:
                keep_alive = False
                self._logger.info(e)
                print("Timeout ... exiting ...")
            except ConnectionAbortedError as e:
                keep_alive = False
                self._logger.info(e)
                print("Connection Aborted ... exiting ...")

        self._control_socket.close()
        if self._data_socket:
            self._data_socket.close()
