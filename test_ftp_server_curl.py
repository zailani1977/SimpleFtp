"""
Test script for FTP Server using curl.

This script automates the testing of `ftp_server.py`. It starts the FTP server
as a subprocess, creates a temporary test file, and uses `curl` to fetch the file
from the server. It also tests file upload functionality.

Dependencies:
    curl (command line tool)
    ftp_server.py (in the same directory)

Usage:
    python3 test_ftp_server_curl.py
"""

import subprocess
import time
import os
import sys

FTP_SERVER_SCRIPT = 'ftp_server.py'
PORT = 2121

# Download test constants
DOWNLOAD_TEST_FILE = 'test_download.txt'
DOWNLOAD_TEST_CONTENT = 'This is a test payload for FTP download.'
DOWNLOAD_URL = f'ftp://localhost:{PORT}/{DOWNLOAD_TEST_FILE}'

# Upload test constants
UPLOAD_SOURCE_FILE = 'test_upload_source.txt'
UPLOAD_DEST_FILE = 'test_upload_dest.txt'
UPLOAD_TEST_CONTENT = 'This is a test payload for FTP upload.'
UPLOAD_URL = f'ftp://localhost:{PORT}/{UPLOAD_DEST_FILE}'

def main():
    # Setup files for tests
    print(f"Creating download test file: {DOWNLOAD_TEST_FILE}")
    with open(DOWNLOAD_TEST_FILE, 'w') as f:
        f.write(DOWNLOAD_TEST_CONTENT)

    print(f"Creating upload source file: {UPLOAD_SOURCE_FILE}")
    with open(UPLOAD_SOURCE_FILE, 'w') as f:
        f.write(UPLOAD_TEST_CONTENT)

    # Ensure destination file does not exist
    if os.path.exists(UPLOAD_DEST_FILE):
        os.remove(UPLOAD_DEST_FILE)

    # Start the FTP server
    print(f"Starting FTP server: {FTP_SERVER_SCRIPT}")
    # Redirect stdout/stderr to devnull to avoid cluttering test output
    server_process = subprocess.Popen(
        [sys.executable, FTP_SERVER_SCRIPT],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Give the server a moment to start
    time.sleep(2)

    try:
        if server_process.poll() is not None:
            print("Error: FTP server failed to start.")
            sys.exit(1)

        # --- Test Download ---
        print("\n--- Testing Download ---")
        print(f"Fetching file using curl: {DOWNLOAD_URL}")
        # curl -s (silent) but show errors (-S)
        result = subprocess.run(
            ['curl', '-s', '-S', DOWNLOAD_URL],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Error: curl download failed with return code {result.returncode}")
            print(f"Stderr: {result.stderr}")
            sys.exit(1)

        fetched_content = result.stdout
        print(f"Fetched content: {fetched_content}")

        if fetched_content == DOWNLOAD_TEST_CONTENT:
            print("PASS: Download content matches.")
        else:
            print("FAIL: Download content mismatch.")
            print(f"Expected: {DOWNLOAD_TEST_CONTENT}")
            print(f"Got: {fetched_content}")
            sys.exit(1)

        # --- Test Upload ---
        print("\n--- Testing Upload ---")
        print(f"Uploading file using curl: {UPLOAD_SOURCE_FILE} -> {UPLOAD_URL}")
        result = subprocess.run(
            ['curl', '-s', '-S', '-T', UPLOAD_SOURCE_FILE, UPLOAD_URL],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Error: curl upload failed with return code {result.returncode}")
            print(f"Stderr: {result.stderr}")
            sys.exit(1)

        # Verify the file exists locally (since server is serving current dir)
        if not os.path.exists(UPLOAD_DEST_FILE):
            print(f"FAIL: Uploaded file {UPLOAD_DEST_FILE} not found on server (local dir).")
            sys.exit(1)

        with open(UPLOAD_DEST_FILE, 'r') as f:
            uploaded_content = f.read()

        print(f"Uploaded content on server: {uploaded_content}")

        if uploaded_content == UPLOAD_TEST_CONTENT:
             print("PASS: Upload content matches.")
        else:
            print("FAIL: Upload content mismatch.")
            print(f"Expected: {UPLOAD_TEST_CONTENT}")
            print(f"Got: {uploaded_content}")
            sys.exit(1)

    finally:
        # Cleanup
        print("\nCleaning up...")
        if server_process.poll() is None:
            server_process.terminate()
            server_process.wait()

        for f in [DOWNLOAD_TEST_FILE, UPLOAD_SOURCE_FILE, UPLOAD_DEST_FILE]:
            if os.path.exists(f):
                os.remove(f)

if __name__ == '__main__':
    main()
