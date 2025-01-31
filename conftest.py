import logging
import os
import traceback
import pytest
import allure
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager


def pytest_runtest_setup(item):
    """
    Setup function to create a log file for each test case.
    """
    # Create a directory for reports if it doesn't exist
    log_dir = "report_evidence"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a log file for this test based on its name and a timestamp
    test_name = item.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"{test_name}_{timestamp}.log")
    
    # Store the log file path on the item so it can be used later in makereport
    item.log_file = log_file

    # Set up the logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove existing handlers to avoid duplicate logs
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create a file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Create and set a formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to process test outcomes and attach screenshots & logs to Allure.
    Attaches both error details (if any) and the logs from the log file.
    """
    outcome = yield  # Yield to let pytest run the test and generate a report
    rep = outcome.get_result()  # rep is the TestReport object

    # Read the log file contents (if available)
    file_logs = ""
    if hasattr(item, "log_file") and os.path.exists(item.log_file):
        with open(item.log_file, "r") as f:
            file_logs = f.read()

    # Prepare a list for log messages to attach via Allure
    log_messages = []
    test_name = item.name

    if rep.when == "call":
        if rep.failed:
            log_messages.append(f"Test FAILED: {test_name}")

            # Capture exception details if available.
            if call.excinfo is not None:
                exception_type = call.excinfo.typename
                exception_message = str(call.excinfo.value)
                tb_str = "".join(traceback.format_exception(
                    call.excinfo.type, call.excinfo.value, call.excinfo.tb))
                log_messages.extend([
                    f"Exception Type: {exception_type}",
                    f"Exception Message: {exception_message}",
                    "Traceback:",
                    tb_str,
                ])
            if hasattr(rep, "duration"):
                log_messages.append(f"Test Duration: {rep.duration:.2f}s")

            # Attach a screenshot if a driver fixture is available.
            # (Adjust "setup" to your driver fixture name if needed.)
            if "setup" in item.funcargs:
                driver = item.funcargs["setup"]
                try:
                    screenshot_png = driver.get_screenshot_as_png()
                    allure.attach(
                        screenshot_png,
                        name="Screenshot",
                        attachment_type=allure.attachment_type.PNG,
                    )
                    log_messages.append("Screenshot captured and attached to Allure report.")
                except Exception as screenshot_exception:
                    err_msg = f"Failed to capture screenshot: {screenshot_exception}"
                    log_messages.append(err_msg)
                    allure.attach(
                        err_msg,
                        name="Screenshot Error",
                        attachment_type=allure.attachment_type.TEXT,
                    )
            # Attach the error logs (if any) as an Allure attachment.
            allure.attach(
                "\n".join(log_messages),
                name="Error Logs",
                attachment_type=allure.attachment_type.TEXT,
            )
        else:
            # Test passed
            pass_message = f"Test PASSED: {test_name}"
            allure.attach(
                pass_message,
                name="Pass Logs",
                attachment_type=allure.attachment_type.TEXT,
            )


def pytest_addoption(parser):
    """
    Add command line options to pytest
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="browser to run tests on (chrome/firefox/all)",
    )


@pytest.fixture
def setup(request):
    """
    Webdriver fixture to run tests on Chrome or Firefox
    """
    browser = request.config.getoption("--browser")
    drivers = []

    if browser.lower() in ["chrome", "all"]:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        drivers.append(
            webdriver.Chrome(service=ChromeService(), options=chrome_options)
        )

    if browser.lower() in ["firefox", "all"]:
        firefox_options = FirefoxOptions()
        # firefox_options.add_argument("--headless")

        drivers.append(
            webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=firefox_options,
            )
        )

    if not drivers:
        raise ValueError("Invalid browser specified. Use chrome, firefox, or all")

    yield drivers[0] if len(drivers) == 1 else drivers

    for driver in drivers:
        driver.quit()
