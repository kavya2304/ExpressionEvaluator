#!/usr/bin/env python
# coding: utf-8

# In[82]:


import math
import re
import sys
token_expressions = [
    # Keywords
    ('PRINT', r'print'),

    # Operators
    ('AdditionAssignment',r'\+='),
    ("SubtractionAssignment",r'\-='),
    ("MultiplicationAssignment",r'\*='),
    ("ModulusAssignment",r"\%="),
    ("DivisionAssignment",r'\/='),
    ("EORAssignment",r"\^="),

    ("AND",r"\&\&"),
    ("OR",r"\|\|"),



    ("Equality",r"\=="),
    ("LessEquality",r'\<='),
    ("Less",r'\<'),
    ("GreaterEquality",r'\>='),
    ("Greater",r'\>'),
    ("NotEquality",r'\!='),
    ("NON",r"\!"),

    ('PLUS', r'\+'),

    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'/'),
    ('MODULO', r'%'),
    ('POWER', r'\^'),
    ('ASSIGN', r'='),
    ('INCREMENT', r'\++'),
    ('DECREMENT', r'--'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('COMMA',r'\,'),
    ('COMMENT',r'\#'),
    ('COMMENTST',r'//*'),
    ('COMMENTEN',r'\*/'),


    # Constants
    ('NUMBER', r'-?\d+(\.\d+)?'),
    ('MINUS', r'-'),
    # Variables
    ('VARIABLE', r'[a-zA-Z_][a-zA-Z0-9_]*'),

    # Ignore whitespace and newlines
#     ('IGNORE', r'\s+'),
    ('IGNORE', r'(?!\n)\s+'),
    ('NL',r'\n+'),

]

token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_expressions)

def lexer(program):
    tokens = []
    for match in re.finditer(token_regex, program):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        if token_type != 'IGNORE':
            if token_type == 'PLUS' and tokens[-1]['type'] == 'PLUS':
                tokens[-1] = {"type": 'INCREMENT', "value": '++'}
            elif token_type == 'MINUS' and tokens[-1]['type'] == 'MINUS':
                tokens[-1] = {"type": 'DECREMENT', "value": '--'}
            elif token_type =='MULTIPLY' and tokens[-1]['type']=='DIVIDE':
                tokens[-1]={"type": 'COMMENTST',"value":'/*'}
            elif token_type =='DIVIDE' and tokens[-1]['type']=='MULTIPLY':
                tokens[-1]={"type": 'COMMENTEN',"value":'*/'}
            else:
                tokens.append({"type": token_type, "value": token_value})
    return tokens


# In[ ]:





# In[83]:


class ParseError(Exception):
    pass

def parse(tokens):
    global current
    current = 0

    def consume(token_type):
        global current
        if current < len(tokens) and tokens[current]["type"] == token_type:
            current += 1
            return True
        return False

    def expression():
#         global current
        if consume("NUMBER"):
            expr = {"type": "NumberLiteral", "value": float(tokens[current - 1]["value"])}
            return expr
        elif consume("VARIABLE"):
            return {"type": "Variable", "value": tokens[current - 1]["value"]}
        elif consume("NON"):
            expr = expression()
            return {"type": "UnaryExpression", "operator": "!", "argument": expr}
        elif consume("LPAREN"):
#             print('-----')
            expr = expression_statement()
            if consume("RPAREN"):
                return expr
            else:
                expr=expression_statement()
                return expr 
     
    
    def bar():
        left=expression()
        while consume("AdditionAssignment") or consume("SubtractionAssignment") or consume("MultiplicationAssignment") or consume("ModulusAssignment") or consume("DivisionAssignment") or consume("EORAssignment") :
            operator = tokens[current - 1]["type"]
            right = power()
            if right==None:
                raise ParseError
            if not isinstance(left, dict) or left["type"] not in ["OperatorExpression"]:
                left = {"type": "OperatorExpression", "left": left, "operator": operator, "right": right}
            else:
                left["right"] = {"type": "OperatorExpression", "left": left["right"], "operator": operator, "right": right}
                
        return left
    

    def power():
        expr = bar()
        if consume("POWER"):
            return {"type": "PowerExpression", "left": expr, "right": power()}
        return expr
    
    def term():
        left = power()
        while consume("MULTIPLY") or consume("DIVIDE") or consume("MODULO"):
            operator = tokens[current - 1]["type"]
            right = power()
            if right==None:
                raise ParseError
            if not isinstance(left, dict) or left["type"] not in ["BinaryExpression", "PowerExpression"]:
                left = {"type": "BinaryExpression", "left": left, "operator": operator, "right": right}
            else:
                left["right"] = {"type": "BinaryExpression", "left": left["right"], "operator": operator, "right": right}
        return left

    def expression_statement1():
        left = term()
        while consume("PLUS") or consume("MINUS"):
            operator = tokens[current - 1]["type"]
            right = term()
            left = {"type": "BinaryExpression", "left": left, "operator": operator, "right": right}
        return left #{"type": "ExpressionStatement", "expression": left}
    
    def rela():
        left=expression_statement1()
        while consume("Equality") or consume("NotEquality") or consume("Greater") or consume("GreaterEquality") or consume("Less") or consume("LessEquality"):
            operator = tokens[current - 1]["type"]
            right = power()
            if right==None:
                raise ParseError
            if not isinstance(left, dict) or left["type"] not in ["OperatorExpression"]:
                left = {"type": "OperatorExpression", "left": left, "operator": operator, "right": right}
            else:
                left["right"] = {"type": "OperatorExpression", "left": left["right"], "operator": operator, "right": right}
                
        return left
    
    def booland():
        left=rela()
        while consume("AND"):
            operator = tokens[current - 1]["type"]
            right = power()
            if right==None:
                raise ParseError
            if not isinstance(left, dict) or left["type"] not in ["OperatorExpression"]:
                left = {"type": "OperatorExpression", "left": left, "operator": operator, "right": right}
            else:
                left["right"] = {"type": "OperatorExpression", "left": left["right"], "operator": operator, "right": right}
                
        return left
        
    
    def boolor():
        left=booland()
        while consume("OR"):
            operator = tokens[current - 1]["type"]
            right = power()
            if right==None:
                raise ParseError
            if not isinstance(left, dict) or left["type"] not in ["OperatorExpression"]:
                left = {"type": "OperatorExpression", "left": left, "operator": operator, "right": right}
            else:
                left["right"] = {"type": "OperatorExpression", "left": left["right"], "operator": operator, "right": right}
                
        return left #{"type": "ExpressionStatement", "expression": left}
    
    def expression_statement():
        left= boolor()
        return {"type": "ExpressionStatement", "expression": left}        
    
    def assignment_statement():
        global current
        if consume("VARIABLE"):
            variable_name = tokens[current - 1]["value"]
            if consume("ASSIGN"):
                values={}
                values.update(expression_statement())
                return {"type": "AssignmentStatement", "variable": variable_name, "value": values}
            elif consume("AdditionAssignment"):
                values = {}
                values.update(expression_statement())
                return {"type": "AdditionAssignment", "variable": variable_name,"value":values}
            elif consume("SubtractionAssignment"):
                values = {}
                values.update(expression_statement())
                return {"type": "SubtractionAssignment", "variable": variable_name,"value":values}
            elif consume("MultiplicationAssignment"):
                values = {}
                values.update(expression_statement())
                return {"type": "MultiplicationAssignment", "variable": variable_name,"value":values}
            elif consume("ModulusAssignment"):
                values = {}
                values.update(expression_statement())
                return {"type": "ModulusAssignment", "variable": variable_name,"value":values}
            elif consume("DivisionAssignment"):
                values = {}
                values.update(expression_statement())
                return {"type": "DivisionAssignment", "variable": variable_name,"value":values}
            elif consume("EORAssignment"):
                values = {}
                values.update(expression_statement())
                return {"type": "EORAssignment", "variable": variable_name,"value":values}
            elif consume("INCREMENT"):
                return {"type": "IncrementStatement", "variable": variable_name}
            elif consume("DECREMENT"):
                return {"type": "DecrementStatement", "variable": variable_name}

    def statement():
        global current
        if tokens[current]["type"] == "PRINT":
            current += 1
            expressions = []
            expressions.append(expression_statement())
            while consume("COMMA"):
                expressions.append(expression_statement())
            return {"type": "PrintStatement", "value": expressions}

        elif tokens[current]["type"] == "VARIABLE":
            return assignment_statement()  

        elif tokens[current]["type"]=="NUMBER":
            return term()
        
        elif tokens[current]["type"]=="COMMENT":
            while tokens[current]["type"]!="NL":
                current = current + 1
            return False          
        
        elif tokens[current]["type"]=='NL':
            return False
        
        elif tokens[current]["type"]=='COMMENTST':
            while tokens[current]["type"]!="COMMENTEN":
                current=current+1
            return False

    program = {"type": "Program", "body": []}
    while current < len(tokens):
        stmt = statement()
        if stmt:
            program["body"].append(stmt)
        else:
            current += 1

    return program


# In[ ]:





# In[84]:


def evaluate(ast, variables=None):
    if variables is None:
        variables = {}
    evaluated_values = []
    
    def eval_expression(expr):

        if expr["type"] == "NumberLiteral":
            return expr["value"]
        elif expr["type"]=="OperatorExpression":
            if expr["right"] == None:
                print('parse error')
            right = eval_expression(expr["right"])
            left = eval_expression(expr["left"])
            operator = expr["operator"]
            if operator == "AdditionAssignment":
                return right+left
            elif operator=="SubtractionAssignment":
                return right-left
            elif operator=="MultiplicationAssignment":
                return right*left
            elif operator=="ModulusAssignment":
                return right%left
            elif operator=="DivisionAssignment":
                return right/left
            elif operator=="EORAssignment":
                return right^left
            elif operator=="Equality":
                return int(right==left)
            elif operator=="NotEquality":
                return int(right!=left)
            elif operator=="Greater":
                return int(right<left)
            elif operator=="Less":
                return int(right>left)
            elif operator=="LessEquality":
                return int(right>=left)
            elif operator=="GreaterEquality":
                return int(right<=left)
            elif operator=="AND":
                if right and left:
                    return 1
                return 0
            elif operator=="OR":
                if right or left:
                    return 1
                return 0
            elif operator=="NON":
                return int(not right)
        elif expr["type"] == "Variable":
            return variables.get(expr["value"], 0)  # return None for undefined variable
        elif expr["type"] == "BinaryExpression":
            if expr["right"]== None:
                print('parse error')             
            right = eval_expression(expr["right"])
            if expr["left"]==None:
                if expr["operator"]=="MINUS":
                    return (-1)*right
                    
            left = eval_expression(expr["left"])
            
            operator = expr["operator"]
            if operator == "PLUS":
                return left + right
            elif operator == "MINUS":
                return left - right
            elif operator == "MULTIPLY":
                return left * right
            elif operator == "DIVIDE":
                if right==0:
                    raise ZeroDivisionError
                return left / right
            elif operator == "MODULO":
                return left % right

        elif expr["type"] == "PowerExpression":
            left = eval_expression(expr["left"])
            right = eval_expression(expr["right"])
            return left ** right
        elif expr["type"] == 'ExpressionStatement':
            return eval_expression(expr['expression'])
        
        elif expr["type"] == 'UnaryExpression':
            if expr["operator"] == '!':
                a = eval_expression(expr['argument'])
                #print('abcdefg')
                if a:
                    return 0
                else:
                    return 1
        
        

    def eval_statement(stmt, variables):
        if stmt["type"] == "PrintStatement":
            evaluated_values1 = []
            for value in stmt['value']:
                try:
                    evaluated_value = eval_expression(value)
                    evaluated_values1.append(evaluated_value)
                except ZeroDivisionError:
                    evaluated_values1.append("divide by zero")
                except Exception as e:
                    evaluated_values1.append(str(e))
            print(*evaluated_values1)

        elif stmt["type"] == "AssignmentStatement":
            if "value" in stmt:
                variables[stmt["variable"]] = eval_expression(stmt["value"])
            else:
                variables[stmt["variable"]] = variables.get(stmt["variable"], 0) + 1
        elif stmt["type"] == "DecrementStatement":
            variables[stmt["variable"]] = variables.get(stmt["variable"], 0) - 1
        elif stmt["type"] == "IncrementStatement":
            variables[stmt["variable"]] = variables.get(stmt["variable"], 0) + 1
        elif stmt['type']=="AdditionAssignment":
            variables[stmt["variable"]] = variables.get(stmt["variable"], 0) + eval_expression(stmt["value"])
        elif stmt['type']=="SubtractionAssignment":
            variables[stmt["variable"]] = variables.get(stmt["variable"], 0) - eval_expression(stmt["value"])
        elif stmt['type']=="MultiplicationAssignment":
            variables[stmt["variable"]] = variables.get(stmt["variable"], 0) * eval_expression(stmt["value"])
        elif stmt['type']=="ModulusAssignment":
            variables[stmt["variable"]] = variables.get(stmt["variable"], 0) % eval_expression(stmt["value"])
        elif stmt['type']=="DivisionAssignment":
            variables[stmt["variable"]] = variables.get(stmt["variable"], 0) / eval_expression(stmt["value"])
        elif stmt['type']=="EORAssignment":
            variables[stmt["variable"]] = int(variables.get(stmt["variable"], 0)) ** int(eval_expression(stmt["value"]))
        elif stmt["type"]=="BinaryExpression":
            val=eval_expression(stmt)
        elif stmt["type"]=="OperatorExpression":
            val=eval_expression(stmt)
                        

    for statement in ast["body"]:
        eval_statement(statement, variables)

    return evaluated_values

# #==================================================================


# In[87]:


# source_code = """
# X= 3 > 25 && (8< 5) || !0
# print X
# """
# try:
#     tokens = lexer(source_code)
#     ast = parse(tokens)
#     if ast is not None:
#         evaluate(ast)
#     else:
#         print("Parsing failed")
# except ParseError as e:
#         print('parse error')
# except ZeroDivisionError as e:
#     print('divide by zero')



# In[86]:


import sys

if __name__ == "__main__":
    input_text =sys.stdin.read()
  
    try:
        tokens = lexer(input_text)
        ast = parse(tokens)
        if ast is not None:
            evaluate(ast)
            # i=i+1
        else:
            print("Parsing failed")
    except ParseError as e:
            print('parse error')
    except ZeroDivisionError as e:
        print('divide by zero')


# In[ ]:





# In[ ]:




