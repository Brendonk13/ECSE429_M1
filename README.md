
# Exploratory testing of 'todo manager API' - Unit Test Suite

Group: AutoProj 25

Please note that our unit tests are run in Python, using the nose requests and unit tests libraries.

## Setup
> pip install -r requirements.txt

## Ensure 'todo manager API' is running on localhost:4567
> java -jar runTodoManagerRestAPI-1.5.5.jar

## Run Unit Test Suite in python
> Note: This command must be ran from the same directory that contains the tests directory
> nosetests --verbosity=2 tests
