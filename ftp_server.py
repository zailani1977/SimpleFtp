"""
Simple FTP Server using pyftpdlib.

This script implements a basic FTP server that allows anonymous read/write access
to the current directory or a specified directory. It is intended for testing
and simple file sharing purposes.

Dependencies:
    pip install pyftpdlib

Usage:
    python3 ftp_server.py [options]

Options:
    -h, --help   Show this help message and exit
    --port PORT  Port to listen on (default: 2121)
    --dir DIR    Directory to serve (default: current directory)

Examples:
    # Start server on default port 2121 serving current directory
    python3 ftp_server.py

    # Start server on port 8021 serving /tmp
    python3 ftp_server.py --port 8021 --dir /tmp

Connecting:
    # Connect using command line ftp client
    ftp localhost 2121

    # Connect using curl
    curl ftp://localhost:2121/filename.txt
"""

import os
import sys
import argparse

try:
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib.servers import FTPServer
except ImportError:
    print("Error: pyftpdlib is not installed.")
    print("Please install it using: pip install pyftpdlib")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Simple FTP Server")
    parser.add_argument('--port', type=int, default=2121, help="Port to listen on (default: 2121)")
    parser.add_argument('--dir', type=str, default=os.getcwd(), help="Directory to serve (default: current directory)")
    args = parser.parse_args()

    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Only adding anonymous user as requested for a simple implementation
    # allowing read/write access to current directory
    # The permissions are:
    # e - change directory (CWD, CDUP)
    # l - list files (LIST, NLST, STAT, MLSD, MLST, SIZE)
    # r - retrieve file from the server (RETR)
    # w - store a file to the server (STOR, STOU)
    authorizer.add_anonymous(args.dir, perm='elrw')

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Instantiate FTP server class and listen on 0.0.0.0:<port>
    address = ('0.0.0.0', args.port)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    print(f"Starting FTP server on {address[0]}:{address[1]}")
    print(f"Serving directory: {args.dir}")
    print(f"To connect, use: ftp localhost {args.port}")

    # start ftp server
    try:
        server.serve_forever(handle_exit=False)
    except KeyboardInterrupt:
        print("\nStopping FTP server...")
        server.close_all()

if __name__ == '__main__':
    main()
