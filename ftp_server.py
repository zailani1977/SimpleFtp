import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def main():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    # Ideally, passwords should not be hardcoded, but for this simple example it's fine.
    # The permissions are:
    # e - change directory (CWD, CDUP)
    # l - list files (LIST, NLST, STAT, MLSD, MLST, SIZE)
    # r - retrieve file from the server (RETR)
    # a - append data to an existing file (APPE)
    # d - delete file or directory (DELE, RMD)
    # f - rename file or directory (RNFR, RNTO)
    # m - create directory (MKD)
    # w - store a file to the server (STOR, STOU)
    # M - change mode/permission (SITE CHMOD)
    # T - change modification time (SITE MFMT)

    # Only adding anonymous user as requested for a simple implementation
    # allowing read-only access to current directory
    authorizer.add_anonymous(os.getcwd(), perm='elr')

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('0.0.0.0', 2121)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    print(f"Starting FTP server on {address[0]}:{address[1]}")

    # start ftp server
    server.serve_forever()

if __name__ == '__main__':
    main()
