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

We can up the number of browser nodes in the `docker-compose` file here:

```
compose file
```

Adjust the `-n` parameter in the pytest run commands accordingly:
`pytest -n 2 --browser=all-docker -m frontend_tests --html=report.html --self-contained-html --alluredir=allure-results`


pytest --browser=chrome -m basket_operations --html=report.html --self-contained-html --alluredir=allure-results

