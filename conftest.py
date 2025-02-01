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
from webdriver_manager.chrome import ChromeDriverManager


def pytest_runtest_setup(item):
    """
    Pytest hook that runs before each test.
    Creates a unique log file for each test, sets up logging for that test,
    and stores the log file path in `item.log_file` for later use.  I'd use the log files
    when attaching report evidence to tests in Xray
    """
    log_dir = "report_evidence"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    test_name = item.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"{test_name}_{timestamp}.log")

    # Attach log file path to the test item for later reference in makereport
    item.log_file = log_file

    # Set up a new logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Remove old handlers to prevent duplicate logging, housekeeping here
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create file handler to write to our unique log file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Format for log messages
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Register the file handler
    logger.addHandler(file_handler)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that runs after the test is executed.
    Attaches logs, error details, and a screenshot (if available) to Allure
    when the test fails, and logs misc details like test duration.
    """
    # Let pytest first execute the test and generate the result
    outcome = yield
    rep = outcome.get_result()

    # Attempt to read and store file logs if they exist
    file_logs = ""
    if hasattr(item, "log_file") and os.path.exists(item.log_file):
        with open(item.log_file, "r") as f:
            file_logs = f.read()

    # Prepare messages to attach (I can expand this to include more details as the framework grows)
    log_messages = []
    test_name = item.name

    if rep.when == "call":
        if rep.failed:
            log_messages.append(f"Test FAILED: {test_name}")

            if call.excinfo is not None:
                exception_type = call.excinfo.typename
                exception_message = str(call.excinfo.value)
                tb_str = "".join(
                    traceback.format_exception(
                        call.excinfo.type, call.excinfo.value, call.excinfo.tb
                    )
                )
                log_messages.extend(
                    [
                        f"Exception Type: {exception_type}",
                        f"Exception Message: {exception_message}",
                        "Traceback:",
                        tb_str,
                    ]
                )
            if hasattr(rep, "duration"):
                log_messages.append(f"Test Duration: {rep.duration:.2f}s")

            # If we have a fixture named "setup", assume it returns a WebDriver
            # Backend tests will skip this
            if "setup" in item.funcargs:
                driver = item.funcargs["setup"]
                try:
                    screenshot_png = driver.get_screenshot_as_png()
                    allure.attach(
                        screenshot_png,
                        name="Screenshot",
                        attachment_type=allure.attachment_type.PNG,
                    )
                    log_messages.append(
                        "Screenshot captured and attached to Allure report."
                    )
                except Exception as screenshot_exception:
                    err_msg = f"Failed to capture screenshot: {screenshot_exception}"
                    log_messages.append(err_msg)

        elif rep.passed:
            # If test passed, you can optionally log something or attach logs
            log_messages.append(f"Test PASSED: {test_name}")

    # If we have any logs to attach, do so
    if log_messages or file_logs:
        combined_logs = "\n".join(log_messages) + "\n" + file_logs
        allure.attach(
            combined_logs,
            name="Test Logs",
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
    Fixture to initialize one or multiple WebDriver instances depending on
    the pytest command-line option --browser. (chrome, firefox, or all)
    Yields a single driver if only one browser was specified,
    otherwise yields a list of drivers.
    """
    browser_option = request.config.getoption("--browser", default="chrome").lower()
    drivers = []

    # If user chose chrome or all, set up Chrome driver
    if browser_option in ["chrome", "all"]:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        drivers.append(
            webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=chrome_options,
            )
        )

    # If user chose firefox or all, set up Firefox driver
    if browser_option in ["firefox", "all"]:
        firefox_options = FirefoxOptions()
        # firefox_options.add_argument("--headless")
        drivers.append(
            webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=firefox_options,
            )
        )

    # Raise an error if no valid driver was added
    if not drivers:
        raise ValueError("Invalid browser specified. Use chrome, firefox, or all")

    # Yield a single driver if there's exactly one, otherwise yield all (typically should only be 1)
    yield drivers[0] if len(drivers) == 1 else drivers

    # Teardown: quit every driver
    for driver in drivers:
        driver.quit()
