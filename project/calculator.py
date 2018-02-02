from collections import namedtuple

Data=namedtuple('Data',['type','val'])
class Buffer(object):
    def __init__(self,data):
        self.data=data
        self.offset=0
    
    def peek(self):
        if self.offset>=len(self.data):
            return None
        return self.data[self.offset]
    def advance(self):
        if self.offset>=len(self.data):
            return
        else:
            self.offset+=1

class Token(object):
    def consume(self):
        pass

class IntToken(Token):
    def consume(self,buffer):
        accum=''
        while True:
            ch=buffer.peek()
            if ch is None or ch in '+-':
                break
            accum+=ch
            buffer.advance()
        if accum !='':
            return Data('int',int(accum))
        else:
            return None
class OperatorToken(Token):
    def consume(self,buffer):
        ch=buffer.peek()
        if ch is None:
            return None
        buffer.advance()
        return Data('ope',ch)
def tokenize(str):
    buffer=Buffer(str)
    tk_int=IntToken()
    tk_op=OperatorToken()
    tokens=[]
    while buffer.peek():
        token=None
        for tk in (tk_int,tk_op):
            token = tk.consume(buffer)
            if token:
                tokens.append(token)
                break
        if not token:
            raise ValuError('Error in syntax')
    return tokens
class Node(object):
    pass
class BinaryOpNode(Node):
    def __init__(self,kind):
        self.kind=kind
        self.left=None
        self.right=None
class IntNode(Node):
    def __init__(self,value):
        self.value=value
def parse(tokens):
    if tokens[0].type != 'int':
        raise ValueError('Must start with an int')
    node = IntNode(tokens[0].val)
    nbo = None
    last = tokens[0].type
    for token in tokens[1:]:
        if token.type == last:
            raise ValueError('Error in syntax')
        last = token.type

        if token.type == 'ope':
            nbo = BinaryOpNode(token.val)
            nbo.left = node
        
        if token.type == 'int':
            nbo.right=IntNode(token.val)
            node =nbo
    return node

def calculate(nbo):
    if isinstance(nbo.left,BinaryOpNode):
        leftval = calculate(nbo.left)
    else:
        leftval = nbo.left.value

    if nbo.kind == '-':
        return leftval+nbo.right.value
    elif nbo.kind=='+':
        return leftval+nbo.right.value
    else:
        raise ValueError('Wrong operator')

def evaluate(node):
    if isinstance(node,IntNode):
        return node.value
    else:
        return calculate(node)

if __name__=='__main__':
    input=input('input:')
    tokens = tokenize(input)
    node = parse(tokens)
    print('result:'+str(evaluate(node)))
