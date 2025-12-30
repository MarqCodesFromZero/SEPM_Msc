<h1 align = "center">Linters for Python Code Quality</h1>

This repository includes exercises, which were part of Module 6 ("Software Engineering Project Management") in Unit 10 (Using Linters to Achieve Python Code Quality) for my MSc in Computer Science at the University of Essex.

## 1. Step

Copy the following Python code into a file named code_with_lint.py:

```
import io
from math import *

from time import time

some_global_var = 'GLOBAL VAR NAMES SHOULD BE IN ALL_CAPS_WITH_UNDERSCOES'

def multiply(x, y):
    """
    This returns the result of a multiplation of the inputs
    """
    some_global_var = 'this is actually a local variable...'
    result = x* y
    return result
    if result == 777:
        print("jackpot!")

def is_sum_lucky(x, y):
    """This returns a string describing whether or not the sum of input is lucky
    This function first makes sure the inputs are valid and then calculates the
    sum. Then, it will determine a message to return based on whether or not
    that sum should be considered "lucky"
    """
    if x != None:
        if y is not None:
            result = x+y;
            if result == 7:
                return 'a lucky number!'
            else:
                return( 'an unlucky number!')

            return ('just a normal number')

class SomeClass:

    def __init__(self, some_arg,  some_other_arg, verbose = False):
        self.some_other_arg  =  some_other_arg
        self.some_arg        =  some_arg
        list_comprehension = [((100/value)*pi) for value in some_arg if value != 0]
        time = time()
        from datetime import datetime
        date_and_time = datetime.now()
        return
```

## 2. Step

Run the code against a variety of linters to test the code quality:

- pylint code_with_lint.py
- pyflakes code_with_lint.py
- pycodestyle code_with_lint.py
- pydocstyle code_with_lint.py

## Results:


- ✅ pylint code_with_lint.py: Click here to see the [output]().

- ✅ pyflakes code_with_lint.py: Click here to see the [output]().
  
- ✅ pycodestyle code_with_lint.py: Click here to see the [output]().
  
- ✅ pydocstyle code_with_lint.py: Click here to see the [output]().

## 3. Step
Compare the effectiveness of each tool in defining and identifying code quality. What can you conclude about the effectiveness of each approach?

## Answer:
Each linter—pylint, pyflakes, pycodestyle, and pydocstyle—serves a specific purpose in code quality analysis, and their effectiveness varies depending on the focus.

Pylint is the most comprehensive tool, checking everything from PEP 8 compliance, logical errors, to code design. It is very effective at catching a wide range of issues, from minor style inconsistencies to deeper architectural problems. However, it can be overly strict and may produce too many warnings, making it harder to use for quick scans without proper configuration.

Pyflakes is much lighter, focusing primarily on catching logical errors such as undefined variables or unused imports. It’s quick and efficient for identifying potential runtime errors but doesn’t enforce coding style or catch design issues.

Pycodestyle strictly enforces PEP 8, ensuring that the code follows Python’s official style guidelines. While it’s excellent for improving code readability and consistency, it doesn’t catch logical errors or runtime issues, so it’s best paired with other tools.

Pydocstyle focuses on ensuring that the code’s documentation is complete and adheres to PEP 257 standards. It is highly effective for making sure docstrings are present and formatted correctly, improving code maintainability. However, it only addresses documentation and does not check for style or logical errors.

In conclusion, pylint offers the most thorough analysis but can be overwhelming, while pyflakes is quick for error detection. Pycodestyle ensures style consistency, and pydocstyle focuses on documentation quality. Together, they cover all aspects of code quality effectively.