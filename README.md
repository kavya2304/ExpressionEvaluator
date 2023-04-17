Project 2: Calculator Language
===============================================================
▶team name and Stevens login

KavyaSri Thalluri     kthallur@stevens.edu
Wenkai Xiao           wxiao7@stvens.edu

=================================================================
▶the URL of team public GitHub repo

https://github.com/kavya2304/ExpressionEvaluator

=================================================================
▶an estimate of how many hours you spent on the project

KavyaSri Thalluri：I spent 2 days nearly 20 hours for writing the basic functions and baseline of the program. For extensions I took another 10-15 hours , and for debugging other 10 hours so totally 40-50 hours I spent on this project. 

Wenkai Xiao:
I spent about 40 hours in the first week to finish the first version of bc, including the basic functions and 4 tests, but the code I wrote just without errors and bug hints never worked.

After the second week of class I realized that my code was quite different from the sample code and used regular expressions in the token section that made no sense for this project.

Thanks to Kavya's help, the next week I implemented an extension to what she had written, discussed with her and fixed some bugs, which took me about 30 hours, so the program took me about 70 hours in total.
========================================================================
▶a description of how you tested your code

I used doctests to test the code. In my test file, add document strings and doctests for the lexer, parse and evaluate functions：

 ```python
 def lexer(program):
    """
    The lexer function takes a program as input and tokenizes it based on the token expressions.
    
    >>> lexer("x = 1")
    [{'type': 'VARIABLE', 'value': 'x'}, {'type': 'ASSIGN', 'value': '='}, {'type': 'NUMBER', 'value': '1'}]
    """
    # Function implementation...

def parse(tokens):
    """
    The parse function takes a list of tokens as input and generates an Abstract Syntax Tree (AST) for the program.
    
    >>> parse([{'type': 'VARIABLE', 'value': 'x'}, {'type': 'ASSIGN', 'value': '='}, {'type': 'NUMBER', 'value': '1'}])
    {'type': 'Program', 'body': [{'type': 'AssignmentStatement', 'variable': 'x', 'value': {'type': 'ExpressionStatement', 'expression': {'type': 'NumberLiteral', 'value': 1.0}}}]
    """
    # Function implementation...

def evaluate(ast, variables=None):
    """
    The evaluate function takes an AST and an optional variables dictionary as input, evaluates the AST and updates the variables dictionary with the results.

    >>> variables = {}
    >>> evaluate({'type': 'Program', 'body': [{'type': 'AssignmentStatement', 'variable': 'x', 'value': {'type': 'ExpressionStatement', 'expression': {'type': 'NumberLiteral', 'value': 1.0}}}]}, variables)
    []
    >>> variables
    {'x': 1.0}
    """
    # Function implementation...
 ```

Next, I import the doctest module into my code and add the doctest test to the if __name__ == "__main__": section. Add the following code to the end of our code:

```python
import doctest

if __name__ == "__main__":
    doctest_result = doctest.testmod()
    if doctest_result.failed == 0:
        print("test pass")
    else:
        print("test failed")
```

This is only the test of the main function, for more functional tests, we first need to count approximately how many specific functions need to be tested, doctests list as follows:

lexer tests - at least 3
Test simple code with different types of tokens
Test code with various operators
tests with comments and multi-line code

parse tests - at least 6
Test simple expressions (e.g., numbers, variables, parentheses)
Test complex expressions (including multiple operators and parentheses)
Test simple assignment statements
Test complex assignment statements (including self-incrementing, self-subtracting, etc.)
Testing print statements
Testing code with comments and multiple lines of code

evaluate tests - at least 6
Testing simple expressions
Test complex expressions
Test evaluation of assignment statements
Test the value of assignment operators such as self-incrementing, self-subtracting, etc.
Testing the output of print statements
Test for exceptions (e.g., division by zero)

is_valid test - at least 3
Test for valid parentheses combinations
Test for invalid bracket combinations
Test for valid and invalid combinations containing non-bracketed characters

The following are examples of doctests for the evaluate divided by zero exception case

```python
def evaluate(expression):
    """
    Evaluates a given expression and returns the result.

    >>> evaluate("5 / 0")
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero
    """
    # our function implementation here
```
Run the bc.py file in the terminal with the following command:

```python
python -m doctest bc.py -v
```

we get the result：

```python
Trying:
    evaluate("5 / 0")
Expecting:
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero
ok
1 items had no tests:
    your_script_name
1 items passed all tests:
   1 tests in your_script_name.evaluate
1 tests in 2 items.
1 passed and 0 failed.
Test passed.
```
========================================================================
>Any bugs or issues you could not resolve
For most of the time I faced an issue with the braces, when I give a big expression inside braces in the print statement.
If I give it without braces it works ,otherwise it is giving me error. After implementing all the extensions, I saw it was fixed itself, I realized it is an issue with the precedence.
But that to me seems like a bug I couldnt resolve myself.

========================================================================
>An example of a difficult issue or bug and how you resolved
An example which involved the power and multiplication took lot of time fo me to fix as I made a mistake in generation of expression statement. It took lot of time to debug it but finally fixed it.
Power should evaluate first and multiply should be next , which is going wrong in my code first and then I fixed it.

========================================================================

▶a list of the four extensions you’ve chosen to implement

**1.Op-equals**

The part of our code that implements the Op-equals functionality is divided into two phases: lexical analysis (lexer) and syntactic parsing (parse).

In the lexical analysis phase (lexer), our code that implements the Op-equals functionality focuses on defining a series of Op-equals operators in the token_expressions list, as follows:

```python
# Operators
('AdditionAssignment',r'\+='), And so on in the same way

```
The Op-equals operators AdditionAssignment, SubtractionAssignment, MultiplicationAssignment, ModulusAssignment, DivisionAssignment and EORAssignment are defined here. Op-equals operators such as SubtractionAssignment, MultiplicationAssignment, ModulusAssignment, DivisionAssignment and EORAssignment.

In the syntax parsing stage (parse), our code to implement Op-equals functionality handles a series of Op-equals operators mainly in the assignment_statement function:

```python
    ...
        # Op-equals part
        elif consume("AdditionAssignment"):
            values = {}
            values.update(expression_statement())
            return {"type": "AdditionAssignment", "variable": variable_name,"value":values} //in the same way for others
```
Finally, in the evaluate function, our code that implements the Op-equals function performs the appropriate action depending on the type of the AST node:

```python
def eval_statement(stmt, variables):
    ...
    # Op-equals part
    elif stmt['type']=="AdditionAssignment":
        variables[stmt["variable"]] = variables.get(stmt["variable"], 0) + eval_expression(stmt["value"]) // in the same way for others
```

Example: for below input 
source_code = """
x=5
x +=2
y=6
y-=3
z=6
z*=2
a=8
a/=2
b=0
b &&= !0
print x,y,z,a,b
"""
output: 7.0 3.0 12.0 4.0 0

**2.Relational operations**

First, tokens of relational operations are generated by.

Next, the relational operation expression is processed in the term() function, and an expression of type OperatorExpression is constructed by consuming the relevant tokens, storing the left operand, operator and right operand in the expression object.

Finally, the relational operation expression is evaluated in the eval_expression() function. By comparing the left operand and the right operand, the Boolean result is converted to an integer value (0 or 1) based on the operator

In the token_expressions list, the relational operation matching rules are defined (lines 45 to 51).

```python
("Equality",r"\==") // same way for others
```
In the term() function, the relational operation expressions are handled (lines 123 to 131).

```python
while consume("Equality") :
    operator = tokens[current - 1]["type"]
    right = power()
    if not isinstance(left, dict) or left["type"] not in ["OperatorExpression"]:
        left = {"type": "OperatorExpression", "left": left, "operator": operator, "right": right}
    else:
        left["right"] = {"type": "OperatorExpression", "left": left["right"], "operator": operator, "right": right} // same way for others
```
In the eval_expression() function, the relational expression is evaluated 

```python
    if operator == "Equality":
        return int(right==left)
```
Example: for the below input
"""print 1 < 3
print 1/3 > 5* 6
"""
output: 
1
0
"""print (4 + 5) * 3 > 25 && !(8 - 2 < 5) || true
output: 1
"""

**3.Boolean operations**

Our code implements 2 Boolean operations: AND and OR and negation. Boolean operations are implemented mainly in the following places:

In the token_expressions list, the regular expression matching rules for the boolean operation are defined (line 52)
```python

("AND", r"\&\&"),//same for others
```
In the term() function, the Boolean operation expressions are handled (lines 123 to 131). Note: The snippet here is the same as the snippet implementing the relational operation, since they both belong to the binary operator.


```python
while consume("OR)
    operator = tokens[current - 1]["type"]
    right = power()
    if right==None:
        raise ParseError
    if not isinstance(left, dict) or left["type"] not in ["OperatorExpression"]:
        left = {"type": "OperatorExpression", "left": left, "operator": operator, "right": right}
    else:
        left["right"] = {"type": "OperatorExpression", "left": left["right"], "operator": operator, "right": right} 
        // Same logic follows for "and "
```

Evaluate the Boolean expression in the eval_expression() function (lines 179 through 182)
```python

elif operator == "AND":
    return int(left and right)// same logic for "and"

```

The code logic is as follows:

First, tokens for Boolean operations are identified and generated by regular expressions.
Next, the Boolean operation expression is processed in the term() function, and an expression of type OperatorExpression is constructed by consuming the relevant tokens, storing the left operand, operator and right operand in the expression object. Note that Boolean operations share the same code segment as relational operations, as they both belong to the binary operator.
Finally, in the eval_expression() function, the Boolean operation expression is evaluated. Depending on the operator, a logical AND or OR operation is performed and the result is converted to an integer value (0 or 1).

Example: print 1 && 2, 2 || 1, -5 && !1, 0 && -100
1 1 0 0

**4.Comments**

Our last extension is Comments,which includes (#, /*,*/) implemented this extension mainly in the following places.

In the Lexer where we tokenize the input if it matches the following regex

```python
    ('COMMENT',r'\#'),
    ('COMMENTST',r'//*'),
    ('COMMENTEN',r'\*/'),
```
In the Parser we identify those tokens and in parser itself we removed them, as there is no need of evaluating those lines.

The code logic is as follows:
```python
elif tokens[current]["type"]=="COMMENT":
            while tokens[current]["type"]!="NL":
                current = current + 1
            return False       //same logic follows for block comments too   
```
First we tokenize and in parser we identify the # and just traverses through everything and ignores until we see a newline character.
If we see /* ,we will will just traverse through everything and ignore until we see a */. 

Example: x = 1
/* 
x = 2
y = 3
*/
y = 4
# print 0
print x, y
output : 1.0 4.0
*/y = 4
print  y
output: 4.0

Example: source_code = 
```python
print (2^10 - 2^7 * 3^2 + 5^3 - 7^2 * 2) / ((11^2 - 2^2) * 3^2 + 13^2 * 2^2) + (3^3 * 2^2 - 5^2 * 7 + 11^2) / ((2^3 * 5 - 3^2) * 7^2 + 17^2) 
output: -0.02854801230441659
```
Input: 
```python 
print (4 + 5) * 3 > 25 && !(8 - 2 < 5) || true
print (7 % 3 == 1 || 2 * 2 == 5) && false || !(1 + 2 < 5)
print (true && false) || (true || false) && !(true && false)
print 10 / 2 + 5 * 3 >= 25 && 8 % 3 != 1 || false
print (3 * 4 < 5 + 6 || true) && false || !(8 % 2 == 0 && 9 - 4 > 4 + 1)
output:
1
0
0
1
0
```
Some more test cases:
```python
_abc_ - parse error
abc - works
1asd - parse error
abc_123_asd - works
abc______ - works
______ - parse error
print - parse error
```
========================================================================