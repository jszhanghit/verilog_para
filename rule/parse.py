import sys
import os
import re
sys.path.append("..")
from ply import yacc
from lexer import *
class Parse():
    def __init__(self):
        self.lexer = Vlexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parse = yacc.yacc(module = self)
    
    def run(self,text):
        return self.parse.parse(text, lexer=self.lexer)

    def p_module_nparal(self,p):
        " module : MODULE ID portls ENDMODULE"
        p[0] = p[3]
    
    def p_portls(self,p):
        "portls : LPAREN ports RPAREN"
        p[0] = p[2]
    # The port lst have no input/output
    def p_ports(self,p):
        """ports : ports COMMA port
                 | port """
        print(len(p[:]))
        if(len(p) == 4):
            p[0] = p[1] + p[3]
        else:
            p[0] = p[1]
    def p_port_in(self,p):
        """port : ID"""
        p[0] = p[1]
    
m = Parse()
data = """module ID(aqw,b,r,t,w,qqs,ds)
 endmodule
"""
print(m.run(data))
