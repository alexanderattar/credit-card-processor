# Basic Credit Card Processing
-----

This application is rudimentry credit card processor.
The program can add new credit card accounts, process charges and credits
against them, and display summary information.
rt

## Requirements

Python >= 3.5

## Usage

### Running the appication


The application accepts input from two types of sources:

 - a filename passed in command line arguments
 - STDIN

Run the application with either of the following commands:


```
python3 app.py input.txt 
```

```
python3 < input.txt
```

### Running tests


The simplest way to run unit test is to use Python's stdlib
[unittest test discovery](https://docs.python.org/3/library/unittest.html#test-discovery)

```
python3 -m unittest discover tests
```

Alternatively, you can run the tests by referencing the test file directly

```
python3 tests/test.py 
```

For more advanced usage (like running tests with code coverage)
install the additional 3rd party library nose.

```
$ pip install nose coverage
$ nosetests --with-coverage
```

## Design Overview

- An overview of your design decisions
- Why you picked the programming language you used
- How to run your code and tests, including how to install any dependencies
your code may have.


