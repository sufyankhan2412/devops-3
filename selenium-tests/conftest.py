import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

@pytest.fixture(scope="session")
def driver_setup():
    """Setup Chrome driver for testing"""
    chrome_options = Options()
    
    # Docker-specific Chrome options
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    
    # Get Selenium Hub URL from environment
    selenium_hub_url = os.getenv('SELENIUM_HUB_URL', 'http://localhost:4444')
    
    # Create remote webdriver
    driver = webdriver.Remote(
        command_executor=f"{selenium_hub_url}/wd/hub",
        options=chrome_options
    )
    
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()

@pytest.fixture(scope="session")
def base_url():
    """Get base URL from environment"""
    return os.getenv('APP_URL', 'http://localhost:3000')

@pytest.fixture
def wait(driver_setup):
    """WebDriverWait fixture"""
    return WebDriverWait(driver_setup, 10)