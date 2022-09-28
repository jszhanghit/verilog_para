import sys
import os
import re
from ply import lex
class Vlexer(object):
    def build(self, **kwargs):
        self.lexer = lex.lex(object=self, **kwargs)
    keyword = ("MODULE","ENDMODULE","PARAMETER")
    reserved = {}
    for kw in keyword:
        reserved[kw.lower()] = kw
    tokens = keyword + (
        "ID",
        
        "LPAREN","RPAREN","COMMA",
        #操作符
        "ADD","SUB","MUL","DIV"
    )
    t_ignore = " \t"
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_COMMA = r","
    def t_NEWLINE(self,t):
        r"\n"
        pass

    def t_error(self,t):
        print("Illegal "+t.value)
        self.lexer.skip(1)
    
    def t_ID(self,t):
        r"[_a-zA-Z0-9]\w*"
        t.type = self.reserved.get(t.value, 'ID')
        return t
    
    t_ADD = r"\+"
    t_SUB = r"-"
    t_MUL = r"\*"
    t_DIV = r"/"

    def token(self):
        return self.lexer.token()
    def input(self, data):
        self.lexer.input(data)
