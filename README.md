# Basic Credit Card Processing


This application is rudimentary credit card processor.
The program can add new credit card accounts, process charges and credits
against them, and display summary information.


## Requirements

Python >= 3.5

## Usage

### Running the application


The application accepts input from two types of sources:

 - a filename passed in command line arguments
 - STDIN

Run the application with either of the following commands:


```
python3 app.py input.txt 
```

```
python3 app.py < input.txt
```

### Running tests


The simplest way to run unit tests is to use Python's stdlib
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
pip install nose coverage
nosetests --with-coverage
```

## Design Overview

The application features a central Processor class that contains the logic to perform the actions laid out in the project description requirements. This includes the input commands described: "Add", "Charge", and "Credit", but additionally the class possesses methods for reading, and parsing input, as well as writing the output summary after all input has been processed. 

The credit card processor is modular by design. The functionality has been abstracted into small methods that each perform an action that can quickly be grasped by the method definition, and the docstrings provided. This design makes the application very readable, as well as maintainable. Additionally, because the Processor class includes all the logic required to accept input and process the output, it creates the opportunity for Processor objects to be instantiated as workers to scale for larger datasets.

Processor objects are instantiated with a dictionary or hash-table for storing the account data for individuals as accounts are added, charged, and credited.

```
{
"Tom": {"card_number": "4111111111111111", "balance": 1000, "limit": 2000},
"Lisa": {"card_number": "4111111111111111", "balance": 1000, "limit": 2000}
}
```

In this contrived example account lookups are performed by using the person’s first name as the primary key. This design clearly is over-simplified for a real-world solution where many accounts could be owned by people with the same first name, in which case, a unique identifier such as the card number or a surrogate key should be used.

Processor can read input from a file via command-line arguments or STDIN. Input is parsed into separate events that contain the type of action to perform and the account to perform them on. Input is read and the events are parsed and then forwarded to the Processor methods designed to handle each action. Parameters for each method are extracted by unpacking the variables in each space delimited event, and then passed to the appropriate method via the event type. This design allows all the actions to be called through the same interface rather than having to check the type of each event before sending to the appropriate method. 

The Processor class also contains some helper methods designed to encapsulate the logic necessary to format the data as it is processed. parse_dollars converts dollar amounts into Decimal types so that mathematical operations can be performed. check_amount ensures that amounts are of type Decimal, and raises an error if they are not. get_account_details abstracts the logic for looking up an account which makes it reusable for all actions that require an account lookup. Finally, generate_summary sorts the output by name and formats the summary.

The main application is a simple block that instantiates a Processor, and cycles through the events parsed by it, but the business logic is primarily handled by the Processor class itself. 

In addition to the output summary written after all the data has been processed, there is an included logging utility that outputs info about the actions being performed as the processor performs the work. This is a helpful visualization, useful for debugging, and also creates the opportunity for monitoring, error tracking, and analysis.

Unit tests are included to accompany the application. The tests are organized to focus on the Processor actions and helper methods. Although the project description notes that all input will be valid, a series of tests have been designed to ensure that proper exceptions are raised in the event of an invalid type getting passed. Additionally, the methods are tested to ensure they are returning the expected outcome, and actions performed on non-existent accounts will raise key lookup errors.

## Python

For this application, I chose to use Python. Python is powerful, flexible and open-source. It has a very simple syntax, which makes it easy to read, and to maintain. Python is fast, and highly scalable for massive web applications; for example much of Google's infrastructure is built on top of it.

Python features an extensive standard library, offering a wide range of facilities, enabling me to write all the logic for this credit card processor without the use of any third-party dependencies. Furthermore, the Python interpreter, makes the development process fast, and allowed me to quickly sketch out functionality, and iterate on my design decisions. I specifically took this as an opportunity to use the latest version of Python (3.5) for this project. Regardless of the slow adoption in the community, I embrace the advantages introduced in Python 3+, and I am excited for the potential of integrating new features such as concurrency with asyncio, and type annotations. Additionally, without having any external dependencies, there was no fear for compatibility issues.