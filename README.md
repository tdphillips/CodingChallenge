Simple program that accomplishes three tasks:
- Reads input data (from file or stdin)
- Prints out an employee tree
- Prints out total salary requirements


Read from stdin (input must end with ^D)

`python start.py`

Read from file (sample files are provided in the `samples` directory)

`python start.py somefile.[json|py]`

Run tests

`python tests.py`


Known issues:
- Does not handle circular relations (some chain of managers that results in A managing B and B managing A through any number of layers)
- Not completely tested