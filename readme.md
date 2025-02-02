## Project Setup

### Pre-requisites

This project can run on unix machines, it was created on linux.  The following dependencies are needed:
* Docker
* docker-compose

If you want to run tests locally, outside of the container, you will need:
* Python 3.12.3
* Pipenv
* Allure

### Running Tests in a container

The framework has been containerised.  We also employ several other containers, these are:
* Selenium Grid (for orchestrating browser instance)
* Chrome node(s) (By default, a single chrome node, to allow chrome browser tests to run)
* Firefox node(s) (As above)
* Allure Reporting
    * The allure docker service to handle generating reports
    * The allure UI docker service to handle viewing reports

To run all the tests, use this command:
`docker compose up`

As the container will run all tests by default, if you just want to run a subset of test, such as frontend only, or backend, you can use these commands when starting the containers:
`docker compose run test-framework frontend`

`docker compose run test-framework backend`

Due to the way the framework/container is structured, we can specify an entry point when the container starts, using the commands above, influences what runs from the `run_tests.sh`

This is what the `run_tests.sh` file looks like:

```bash
# Execute different actions based on the argument
case "$COMMAND" in
    frontend)
        echo "Running frontend tests across all browsers..."
        exec pytest -n 2 --browser=all-docker -m frontend_tests --html=report.html --self-contained-html --alluredir=allure-results
        ;;
    backend)
        echo "Running backend tests..."
        exec pytest -n 2 -m backend_tests --html=report.html --self-contained-html --alluredir=allure-results
        exec pytest -n 1 -m validate_ratelimit --html=report.html --self-contained-html --alluredir=allure-results
        ;;
    all)
        echo "Running frontend tests across all browsers..."
        exec pytest -n 2 --browser=all-docker -m frontend_tests --html=report.html --self-contained-html --alluredir=allure-results
        echo "Running backend tests..."
        exec pytest -n 2 -m backend_tests --html=report.html --self-contained-html --alluredir=allure-results
        exec pytest -n 1 -m validate_ratelimit --html=report.html --self-contained-html --alluredir=allure-results
        ;;
    *)
        echo "Unknown command: $COMMAND"
        exit 1
        ;;
esac
```

We can store our pytest commands in the file, and add in different combinations for different runs, when implementing the container infrastructure within a CI/CD pipeline, we can point the compose command to the run type in this file, and this will run the correct tests for the pipeline.

If you want to rebuild the framework container at any point, run this:
`docker compose up --build`

### Viewing Reports when running in a container
During a test run, and after a test run, you can view the results by going to this link:
http://localhost:5252/allure-docker-service-ui/projects/default/reports/latest

This takes you to Allure, in here you can view the logs/stdout for each test.  Frontend tests will display a screenshot upon failure, and there is also a helper in the framework to take screenshots and attach them to the report in an adhoc manner for a richer reporting experience.

### Scaling the infrastructure

When running inside the container, the tests run in parallel using `pytest-xdist`, I've kept the parallel jobs low, 2 tests at a time will run.  Selenium Grid will run one test on the Chrome node and another on the Firefox node at any one time.

We can up the number of browser nodes in the `docker-compose` command, like this:

```
docker compose up -d --scale chrome=3 --scale firefox=3
```

Adjust the `-n` parameter in the pytest run commands accordingly:
`pytest -n 2 --browser=all-docker -m frontend_tests --html=report.html --self-contained-html --alluredir=allure-results`

An improvement here, would be to find a way to programtically increase the `-n` parameter based on the max value of nodes added via the compose command.

### Running the tests locally

When writing test, triaging failures or debugging issues - it is easier to run the tests from the command line locally, rather than inside the container.

To do so, there are a couple of commands we can use.  For the frontend:

`pytest --browser=chrome -m basket_operations --html=report.html --self-contained-html --alluredir=allure-results`

The `--browser=chrome` parameter tells the framework you want to run the tests on Chrome.  You can also set this parameter as:
* `firefox`
* `all`

Setting it as `firefox` runs the tests on Firefox (you'll need the browser to be installed on your machine).  Setting it as `all` runs the tests across both Chrome and Firefox.  This is controlled by two functions in the `conftest.py` file at the root of the framework.

`pytest_generate_tests` function contains the parameter logic about what gets selected and when.
`setup` fixture contains the logic around what to do with the parameter and which webdriver needs to be instatiated.  In time the framework can be adjusted to allow for mobile devices to be provisioned via cloud based device providers or to connect to a local Appium server to farm tests out to mobile devices.

When running locally, results are still created for Allure, to access these (make sure you have allure installed locally), you should run this in your terminal from the root of the project directory:
`allure serve allure-results`
A standard pytest HTML report is also generated and placed in the root of the project to be viewed as well, contained the logs, stdout attributed to the tests that have been run.  No screenshots are attached to the HTML report.

## Framework Structure
### conftest.py

The Framework utilises the conftest.py file held at the root of the project directory.  I have a single conftest.py file in the framework, I've not set any nested conftest files in the respective test folders.  The reason I have done this is for maintainability.  The fixtures and hooks created in this file, are as follows:

* pytest_runtest_setup
    * This hook runs before each test (whether it is frontend or backend) and created a log file for the test, the logfile is held in the report_evidence folder of the framework.  This logfile is then available to be attached to the allure report upon test completion.  Holding log files like this locally, means that we can marry up the logfile back to 3rd party test management tools (like Xray), where we might want to send the logfiles after a test run has complete (along with any other results/screenshots/files)
* pytest_runtest_makereport
    * This runs after each test, it checks to see whether the test context has a webdriver in it, if it does - and an exception is present, its takes a screenshot of the browser running, so that the report is furnished with a screenshot at the point of failure.  This also attaches the logfile to the Allure report
* pytest_addoption
    * This allows us to set a custom parameter to be used in our pytest run command.  For us, this allows us to set what environment we want the frontend tests to run in (Chrome/Firefox/All etc)
* pytest_generate_tests
    * This dynamically orchestrates our 'setup' fixture which holds our webdriver logic, based on the parameter provided to the run command
* setup
    * This is our 'setup' fixture which passes the correct webdriver to the frontend tests.  As part of our webdriver setup, we use the webdriver_manager python package, this automatically retrieves the correct webdriver version for the version of the browser our local machine uses, and also handles getting the correct webdriver for any Chrome/Firefox nodes it encounters when running in the container.  
