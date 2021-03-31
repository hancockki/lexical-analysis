#CSCI 2320: RD and more specifically LL(1) parser
#Mohammad T. Irfan
#Grammar productions
#Expr -> Term {(+|-) Term}
#Term -> Factor {(+|-) Factor}
#Factor -> intLiteral

tokens = ["intLiteral", "+", "intLiteral", "*", "intLiteral"] #input
token_pointer = 0

def main():
    expr() #start symbol
    if token_pointer < len(tokens): #could not consume the whole input
        error("Incomplete expression. Error at index " + str(token_pointer))
    else:
        print("Valid Expression!")

#Expr -> Term {(+|-) Term}
def expr():
    global token_pointer
    term()
    while token_pointer < len(tokens) and (tokens[token_pointer]=="+" or tokens[token_pointer]=="-"):
        token_pointer += 1
        term()

#Term -> Factor {(+|-) Factor}
def term():
    global token_pointer
    factor()
    while token_pointer < len(tokens) and (tokens[token_pointer] == "*" or tokens[token_pointer] == "/"):
        token_pointer += 1
        factor()

#Factor -> intLiteral
def factor():
    global token_pointer
    if token_pointer < len(tokens) and tokens[token_pointer] == "intLiteral":
        token_pointer += 1
    else: #operand (intLiteral) missing
        error("Missing intLiteral at index " + str(token_pointer))
    
def error(msg):
    print(msg)
    exit()

if __name__ == "__main__":
    main()
