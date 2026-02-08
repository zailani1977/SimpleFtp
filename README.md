# Simple FTP Server

A simple Python FTP server implementation using `pyftpdlib`. This project provides a basic FTP server script and a test script to verify its functionality.

## Features

- **Simple Implementation**: Easy to understand and modify.
- **Anonymous Access**: Configured for anonymous read-only access by default.
- **Customizable**: Supports command-line arguments for port and directory.
- **Robustness**: Handles graceful shutdown on `Ctrl-C` and checks for dependencies.

## Dependencies

This project requires the `pyftpdlib` library.

```bash
pip install pyftpdlib
```

## Usage

### Starting the Server

To start the server with default settings (port 2121, serving current directory):

```bash
python3 ftp_server.py
```

### Options

- `-h`, `--help`: Show help message and exit.
- `--port PORT`: Specify the port to listen on (default: 2121).
- `--dir DIR`: Specify the directory to serve (default: current directory).

**Example:**

Serve the `/tmp` directory on port 8021:

```bash
python3 ftp_server.py --port 8021 --dir /tmp
```

### Connecting

You can connect to the server using any standard FTP client or `curl`.

**Using command line ftp client:**
```bash
ftp localhost 2121
```

**Using curl:**
```bash
curl ftp://localhost:2121/filename.txt
```

## Testing

A test script is provided to verify the server's functionality using `curl`.

```bash
python3 test_ftp_server_curl.py
```

This script will:
1. Create a temporary test file.
2. Start the FTP server in the background.
3. Download the file using `curl`.
4. Verify the downloaded content matches the original.
5. Clean up the test file and stop the server.
