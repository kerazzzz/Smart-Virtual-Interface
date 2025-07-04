import subprocess
import sys

def install_webdriver_manager():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])  # Upgrade pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver-manager"])  # Install webdriver-manager
        print("\n✅ WebDriver Manager installed successfully!")
    except subprocess.CalledProcessError:
        print("\n❌ Installation failed. Please check your Python and pip setup.")

if __name__ == "__main__":
    install_webdriver_manager()
