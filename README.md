
# Exploratory testing of 'todo manager API' - Unit Test Suite

Group: AutoProj 25
 
Please note that our unit tests are run in Python, using the nose requests and unit tests libraries.

## Setup
> pip install -r requirements.txt \
> pip install nose requests

## Ensure 'todo manager API' is running on localhost:4567
> java -jar runTodoManagerRestAPI-1.5.5.jar

## Run Unit Test Suite in python
> nosetests -v --with-randomly to run them in random order \
>nosetests -v to run them in order
