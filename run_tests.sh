#!/bin/bash

# Check if an argument was passed
if [ -z "$1" ]; then
    echo "No argument provided. Exiting."
    exit 1
fi

echo "Waiting for Selenium Grid to be ready..."
until $(curl --output /dev/null --silent --head --fail http://selenium-hub:4444/status); do
    echo "Waiting for Selenium Grid..."
    sleep 2
done

echo "Selenium Grid is up!"
COMMAND=$1

chmod -R 777 /app/allure-results

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
