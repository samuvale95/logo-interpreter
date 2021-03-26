Logo Parser and Interpreter
===
### What is Logo programming language?
Here is a definition from wikipedia:

>A general-purpose language, Logo is widely known for its use of turtle graphics, in which commands for movement and drawing produced line or vector graphics, either on screen or with a small robot termed a turtle. The language was conceived to teach concepts of programming related to Lisp and only later to enable what Papert called "body-syntonic", where students could understand, predict, and reason about the turtle's motion by imagining what they would do if they were the turtle.

### What is the aim of this project?
The aim of the project was create a real parser and interpreter of a programming language, in this particular case what I made was a transpiler. A transpiler is a piece of code that take another source code in input and the output is an equivalente source code in the same language or a different programming language.
In this case I parse a Logo code and translate that in a equivalent Python code and run a code over a Python interpreter.

### How the project work?
The project is made by 2 component:

- [`parse.py`](https://github.com/samuvale95/logo-interpreter/blob/main/src/parser.py), this code read a Logo grammar from a *.txt* file and create the parsed tree that will be use to interpreter to translate Logo command into Python command.  
- [`interpreter.py`](https://github.com/samuvale95/logo-interpreter/blob/main/src/interpreter.py), this code define all possibile Logo operation and convert that into Python code. To execute Logo graphic operation I use [turtle](https://docs.python.org/3/library/turtle.html) library that allow to execute Logo graphic operation to the screen.

For all project in the docs folder there is complete documentation for all code.

### How to use it?
One of the main components project is the [Liblet](https://github.com/let-unimi/liblet) library, develop by prof. [Massimo Santini](https://github.com/mapio) for his course. For a correct execution and installation of this project refer to [Liblet documentation](https://liblet.readthedocs.io/en/latest/index.html).

1. Clone this repository
2. run `pip install -r requirements.txt`
3. run `test.py` to check if all code work correctly.
