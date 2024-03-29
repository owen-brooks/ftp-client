"""
Owen Brooks
run.py

This module provides command line connection for the ftp_client module
"""

import sys
import logging

from src.utils import parse_args
from src.ftp_client import Client


host, log_file, port = parse_args(sys.argv[1:])  # exclude filename

logging.basicConfig(
    filename=log_file, format="%(asctime)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger()

ftp_client = Client(logger)
if ftp_client.connect(host, port):
    ftp_client.run()
else:
    print("Connection to server failed ... exiting")

