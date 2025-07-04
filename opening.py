import subprocess
import sys

def install_selenium():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])  # Upgrade pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])  # Install Selenium
        print("\n✅ Selenium installed successfully!")
    except subprocess.CalledProcessError:
        print("\n❌ Installation failed. Please check your Python and pip setup.")

if __name__ == "__main__":
    install_selenium()
