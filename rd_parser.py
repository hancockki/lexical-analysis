"""
CSCI 2320
Programming Assignment 2: Syntactic Analysis

For this assignment, our goal was to create a 
recursive descent parser for the CLite programming
language. 
The input is a stream of tokens and lexemes, and the output
is either a success message (meaning the tokens represent a 
syntactically correct program) or a failure message (tokens do
not represent a syntactically correct program).

The program takes in a single command-line argument corresponding
to the input file of token and lexemes.

To implement this, we use a top-down recursive approach, where 
a method is defined for each nonterminal symbol that does not
have a corresponding token. We call the start symbol first, in this
case, Program(). This function then calls all of the NT symbols on the
RHS of the grammar production rule, and this continues until 
a token is reached. 

Each time we come across a new token, we increment the token counter.
If the syntactically correct token is recognized,
we continue the recursion process after incrementing.
If we reach a syntactically incorrect symbol or the token pointer is not
equal to the number of tokens after reading in all the tokens given 
(meaning some were not parsed) then an error message is printed.

Kim Hancock
Principles of Programming Languages
Bowdoin College
"""


import sys

#define globally used variables
token_input = []
token_pointer = 0
raise_error = False

# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

#define a user defined error for incorrect tokens
class ParseError(Error):
    pass

"""
Read in the file of tokens and lexemes.
Each line of the file contains a token followed
by a tab, followed by a lexeme.
This file is read in line by line, and the token 
is added to our globally defined list, token_input.

@params:
    input --> file name given on command line
"""
def get_input(input):
    with open(input, 'r') as tokens:
        for line in tokens:
            next_token = line.split()[0]
            print(next_token)
            token_input.append(next_token)

"""
Main method, driver for our recursion.
We start by getting the stream of user tokens
and then call our start symbol.
From Program(), all of the subsequent NT methods 
are called until all tokens are processed or an error
is raised.

@params:
    input --> file name given on command line
"""
def main(input):
    get_input(input)
    Program() #start symbol
    if token_pointer < len(token_input): #could not consume the whole input
        print("Incomplete expression. Error at index " + str(token_pointer) + " " + str(token_input[token_pointer]))
    else: #consumed all tokens with no errors
        print("Valid Expression!")

"""
Start symbol.
Since the first 5 tokens are the same for any program, we manually check these.
Then, after the opening bracket for the main method,
we call Declarations and Statements, the two NT symbols on the RHS of Program

When we reach the end of this method we are done parsing and return to main(),
where we check if the parsing was valid.
"""
def Program():
    global token_pointer
    if token_pointer < len(token_input) and token_input[token_pointer] == "type":
        token_pointer += 1
    else:
        return
    if token_pointer < len(token_input) and token_input[token_pointer] == "main":
        token_pointer+= 1
    else:
        return
    if token_pointer < len(token_input) and token_input[token_pointer] == "(":
        token_pointer+=1
    else:
        return
    if token_pointer < len(token_input) and token_input[token_pointer] == ")":
        token_pointer+=1
    else:
        return
    if token_pointer < len(token_input) and token_input[token_pointer] == "{":
        token_pointer += 1
        #call NT symbols on RHS of Program grammar production rule
        Declarations()
        Statements()
    else:
        return
    if token_pointer < len(token_input) and token_input[token_pointer] == "}":
        token_pointer += 1

"""
Grammar rule is that Declarations maps to
one or more iterations of Declaration. 
We use a while loop to capture this.
"""
def Declarations():
    while token_pointer < len(token_input) and token_input[token_pointer] == "type":
        Declaration()

"""
Grammar rule for declaration is type followed
by id, followed by 0 or more iterations of ,id.
"""
def Declaration():
    global token_pointer
    Type() #type must come first
    if token_pointer < len(token_input) and token_input[token_pointer] == "id":
        token_pointer += 1
    else:
        error("No id. Error at index: " + str(token_pointer))
    # we could have id followed by any number of ,id (comma separated values)
    while token_pointer < len(token_input) and token_input[token_pointer] == ",":
        token_pointer += 1
        if token_pointer < len(token_input) and token_input[token_pointer] == "id":
            token_pointer += 1
        else: 
            error("Comma not followed by id. Error at index: " + str(token_pointer))
    #declaration must end with a semicolon
    if token_input[token_pointer] == ";":
        token_pointer += 1
    else:
        error("no semicolon. Error at index: "+ str(token_pointer))

"""
Simply check if the token is type.
"""
def Type():
    global token_pointer
    if token_pointer < len(token_input) and token_input[token_pointer] == "type":
        token_pointer += 1

"""
Statements is defined as 0 or more iterations
of Statement. Keep running Statement until it returns
false.
"""
def Statements():
    while Statement():
        Statement()

""" 
The grammar rule for Statement is either
Assignment OR PrintStmt OR IfStatement OR WhileStatement
OR ReturnStatement. We try each of these until the 
syntax for one matches. If this is the case, we return True.
Otherwise, we return False.

We use try except blocks here, meaning we need to catch an error.
Since we only want to catch errors in this method, we use a bool
that is globally defined to be false, and make it true for the duration
of this method. Then, if we get parsing errors while trying one of the NT symbols,
we can catch the error and try to next NT symbol.
"""
def Statement():
    global raise_error
    raise_error = True
    try:
        Assignment()
        raise_error = False
        return True
    except ParseError:
        pass
    try:
        PrintStmt()
        raise_error = False
        return True
    except ParseError:
        pass
    try:
        IfStatement()
        raise_error = False
        return True
    except ParseError:
        pass
    try:
        WhileStatement()
        raise_error = False
        return True
    except ParseError:
        pass
    try:
        ReturnStatement()
        raise_error = False
        return True
    except ParseError:
        raise_error = False
        return False #none of them worked!

"""
PrintStmt grammar production rule is defined as print followed
by expression followed by semicolon. 
"""
def PrintStmt():
    global token_pointer
    print("Print", token_input[token_pointer])
    if token_input[token_pointer] == "print":
        token_pointer += 1
    else:
        error("Missing print. Error at index " + str(token_pointer))
    Expression()
    if token_input[token_pointer] == ";":
        token_pointer += 1
    else:
        error("Missing semicolon. Error at index " + str(token_pointer))

"""
Grammar production rule for IfStatement is if followed by (Expression) 
followed by Statement, followed by 0 or 1 iterations of else Statement
"""
def IfStatement():
    global token_pointer
    if token_input[token_pointer] == "if" and token_pointer < len(token_input):
        token_pointer += 1
    else:
        error("No if. Error at index " + str(token_pointer))
    if token_input[token_pointer] == "(" and token_pointer < len(token_input):
        token_pointer += 1
        Expression()
    else:
        error("No (. Error at index " + str(token_pointer))
    if token_input[token_pointer] == ")" and token_pointer < len(token_input):
        token_pointer += 1
    else:
        error("No ). Error at index " + str(token_pointer))
    Statement()
    if token_input[token_pointer] == "else": #check if we have an else block
        token_pointer += 1
        Statement()

"""
WhileStatement grammar production rule is defined as while followed by
(Expression) followed by Statement.
"""
def WhileStatement():
    global token_pointer
    print("While")
    if token_input[token_pointer] == "while" and token_pointer < len(token_input):
        token_pointer += 1
    else:
        error("Missing while. Error at index " + str(token_pointer))
    if token_input[token_pointer] == "(" and token_pointer < len(token_input):
        token_pointer += 1
        Expression()
    else:
        error("Missing (. Error at index " + str(token_pointer))
    if token_input[token_pointer] == ")" and token_pointer < len(token_input):
        token_pointer += 1
    else:
        error("Missing ). Error at index " + str(token_pointer))
    Statement()

"""
ReturnStatement grammar production rule is defined as return followed by
Expression followed by semicolon. 
"""
def ReturnStatement():
    global token_pointer
    if token_input[token_pointer] == "return" and token_pointer < len(token_input):
        token_pointer += 1
    Expression()
    if token_input[token_pointer] == ";" and token_pointer < len(token_input):
        token_pointer += 1
    else:
        error("Missing ; in return. Error at index " + str(token_pointer))

"""
Grammar production rule for assignment is defined as 
if followed by assignOp followed by Expression followed
by semicolon.
"""
def Assignment():
    global token_pointer
    if token_input[token_pointer] == "id":
        token_pointer += 1
    if token_input[token_pointer] == "assignOp":
        token_pointer += 1
    Expression()
    if token_input[token_pointer] == ";":
        token_pointer += 1
    else:
        error("Missing semicolon. Error at index " + str(token_pointer))

"""
Grammar production rule for Expression() is Conjunction followed by
zero or more iterations of || Conjunction
"""
def Expression():
    global token_pointer
    Conjunction()
    while token_input[token_pointer] == "||":
        token_pointer += 1
        Conjunction()

"""
Grammar production rule for Conjunction is Equality followed
by zero or more iterations of && Equality
"""
def Conjunction():
    global token_pointer
    Equality()
    while token_input[token_pointer] == "&&":
        token_pointer += 1
        Equality()

"""
Grammar production rule for Equality is Relation followed by
zero or 1 occurences of equOp Relation 
"""
def Equality():
    global token_pointer
    Relation()
    if token_input[token_pointer] == "equOp":
        token_pointer+=1
        Relation()

"""
Grammar Production rule for Relation is Addition followed by
zero or 1 occurence of relOp Addition
"""
def Relation():
    global token_pointer
    Addition()
    if token_input[token_pointer] == "relOp":
        token_pointer += 1
        Addition()

"""
Grammar Production rule for Addition is Term followed by zero or 
more iterations of addOp Term
"""
def Addition():
    global token_pointer
    Term()
    while token_input[token_pointer] == "addOp":
        token_pointer+=1
        Term()

"""
Grammar Production rule for Term is Factor followed by zero or more
iterations of multOp Factor 
"""
def Term():
    global token_pointer
    #print("Term")
    Factor()
    while token_input[token_pointer] == "multOp":
        #print("Found ", token_input[token_pointer])
        Factor()

""" 
Grammar Production rule for Factor is id OR intLiteral OR boolLiteral OR
floatLiteral OR (Expression)
"""
def Factor():
    global token_pointer
    global raise_error
    print(token_input[token_pointer])
    if token_input[token_pointer] == "id" or token_input[token_pointer] == "intLiteral" or \
    token_input[token_pointer] == "boolLiteral" or token_input[token_pointer] == "floatLiteral":
        token_pointer += 1
        return
    #check if we have opening parenthenses for (Expression)
    elif token_input[token_pointer] == "(":
        token_pointer += 1
        Expression()
    #check if we have closing parenthenses for (Expression)
    if token_input[token_pointer] == ")":
        token_pointer += 1
    else:
        error("Error in factor. Error at index " + str(token_pointer))

def error(msg):
    print(msg)
    if raise_error:
        print("raise error", token_pointer)
        raise ParseError
    exit()

if __name__ == "__main__":
    main(sys.argv[1])