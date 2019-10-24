"""
Owen Brooks
ftp_client.py

This module contains the client module, with the main processing loop
"""
import socket


class Client:
    """ FTP client object"""

    def __init__(self, logger):
        """Init method for ftp client object"""
        self._logger = logger
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        """connect to server specified in cmd line args

        :param host: ip of server
        :param port: port number
        :return:
        """
        try:
            self._logger.info(f"Connecting to {host}")
            self._socket.connect((host, port))
            self._logger.info("Received: 220 FTP Server ready")
        except:
            self._logger.info(f"Failed to connect to {host}")
            raise

    def run(self):
        """main processing loop"""
        close_connection = False
        reply_file = this._socket.makefile('r')
        print(f.readline())

        self._socket.close()
        self._logger.info("Closing connection to host.")
        return
