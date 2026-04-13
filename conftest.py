import os
from pathlib import Path
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


def pytest_configure(config):
    """Add the managed chromedriver directory to PATH before any tests run."""
    driver_path = ChromeDriverManager().install()
    driver_dir = str(Path(driver_path).parent)
    os.environ["PATH"] = driver_dir + os.pathsep + os.environ.get("PATH", "")


def pytest_setup_options():
    """Run Chrome headless for CI-friendly testing."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return options
