#CSCI 2320: Basic skeleton of an RD parser. This will not run properly.
#Mohammad T. Irfan
#Grammar productions
#Expr -> Term {(+|-) Term}
#Term -> Factor {(+|-) Factor}
#Factor -> intLiteral

tokens = ["intLiteral", "+", "intLiteral", "*", "intLiteral"] #input
token_pointer = 0

def main():
    expr() #start symbol

#Expr -> Term {(+|-) Term}
def expr():
    term()
    while tokens[token_pointer]=="+" or tokens[token_pointer]=="-":
        token_pointer += 1
        term()

#Term -> Factor {(+|-) Factor}
def term():
    factor()
    while tokens[token_pointer] == "*" or tokens[token_pointer] == "/":
        token_pointer += 1
        factor()

#Factor -> intLiteral
def factor():
    if tokens[token_pointer] == "intLiteral":
        token_pointer += 1
