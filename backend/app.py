import os
import subprocess
import platform
import sys


def activate_virtual_env():
    """Activate the virtual environment based on the OS."""
    print("Activating the virtual environment...")
    if platform.system() == "Windows":
        activate_script = os.path.join("env", "Scripts", "activate.bat")
    else:
        activate_script = os.path.join("env", "bin", "activate")

    if not os.path.exists(activate_script):
        raise FileNotFoundError("Virtual environment not found. Please create it first.")

    return activate_script


def install_dependencies():
    """Install Python dependencies."""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


def check_env_file():
    """Ensure the `.env` file exists."""
    print("Checking for .env file...")
    if not os.path.exists(".env"):
        raise FileNotFoundError(".env file not found. Please generate it before starting the server.")


def start_server():
    """Start the backend server."""
    print("Starting the backend server...")
    subprocess.run([sys.executable, "noovox/server.py"], check=True)


def main():
    try:
        print("Starting Noovox Backend Setup...")
        # Step 1: Activate virtual environment
        activate_script = activate_virtual_env()
        print(f"Virtual environment activation command: {activate_script}")
        if platform.system() == "Windows":
            subprocess.run(activate_script, shell=True)
        else:
            subprocess.run(["source", activate_script], shell=True, executable="/bin/bash")

        # # Step 1: Check .env file
        check_env_file()

        # Step 2: Start the server
        start_server()

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Subprocess failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
