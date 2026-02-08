import subprocess
import time
import os
import sys

FTP_SERVER_SCRIPT = 'ftp_server.py'
TEST_FILE = 'test_payload.txt'
TEST_CONTENT = 'This is a test payload for FTP server.'
PORT = 2121
FTP_URL = f'ftp://localhost:{PORT}/{TEST_FILE}'

def main():
    # Create a test file
    print(f"Creating test file: {TEST_FILE}")
    with open(TEST_FILE, 'w') as f:
        f.write(TEST_CONTENT)

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

        # Use curl to fetch the file
        print(f"Fetching file using curl: {FTP_URL}")
        # curl -s (silent) but show errors (-S)
        result = subprocess.run(
            ['curl', '-s', '-S', FTP_URL],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Error: curl failed with return code {result.returncode}")
            print(f"Stderr: {result.stderr}")
            sys.exit(1)

        fetched_content = result.stdout
        print(f"Fetched content: {fetched_content}")

        if fetched_content == TEST_CONTENT:
            print("PASS: Content matches.")
        else:
            print("FAIL: Content mismatch.")
            print(f"Expected: {TEST_CONTENT}")
            print(f"Got: {fetched_content}")
            sys.exit(1)

    finally:
        # Cleanup
        print("Cleaning up...")
        if server_process.poll() is None:
            server_process.terminate()
            server_process.wait()

        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

if __name__ == '__main__':
    main()
