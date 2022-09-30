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
        self.parse = yacc.yacc(module = self,debug=True)
        self.ports = {}
    def run(self,text):
        return self.parse.parse(text, lexer=self.lexer)

    def p_module_nparal(self,p):
        " module : MODULE ID mheadls ENDMODULE"
    #def p_mheadls_parasports(self,p):
    #    " mheadls : parals portls"
    #    pass
    def p_mheadls_ports(self,p):
        " mheadls : portls"    
        pass
    # port declaration
    # io_dir [net_type] [signed] [range] list_port_identifiers
    # io_dir : input/output
    # net_type : reg/wire/logic
    # signed ： signe/unsigned
    def p_portls(self,p):
        "portls : LPAREN ports RPAREN"
        p[0] = p[2]
    # The port lst have no input/output
    def p_ports(self,p):
        """ports : ports COMMA portcom
                 | portcom """
        if(len(p) == 4):
            if(isinstance(p[3],list)):
                for i in p[3][1]:
                    self.ports[i] = p[3][0]
            else:
                self.ports[p[3]] = ["","","",""]
        else:
            if(isinstance(p[1],list)):
                for i in p[1][1]:
                    self.ports[i] = p[1][0]
            else:
                self.ports[p[1]] = ["","","",""]



    def p_porthead(self,p):
        " porthead : iorange ID"
        p[0] = [p[1],[p[2]]]
        
    portcom_start = "io"
    def p_portcom(self,p):
        """ portcom : portcom COMMA ID
                    | porthead"""
        print(p[:],p[-3])
        if(len(p) == 2):
            p[0] = p[1]
        else:
            p[1][1].append(p[3])
            p[0] =  [p[1][0] , p[1][1]]
    
    def p_io(self,p):
        """ io : INPUT
               | OUTPUT"""
        p[0] = p[1]
    def p_nett(self,p):
        """ nett : WIRE
                 | REG
                 | LOGIC"""
        pass
    def p_ionett(self,p):
        """ ionett : io nett
                  | io"""
        p[0] = p[1]
    def p_signed(self,p):
        """ signed : SIGNED
                 | UNSIGNED"""
        p[0] = p[1]
    
    def p_iosign(self,p):
        """ iosign : ionett signed
                   | ionett"""
        if(len(p)==2):
            p[0] = [p[1],""]
        else:
            p[0] = [p[1],p[2]]
    def p_range(self,p):
        " range : LBRAC expr COLON expr RBRAC "
        p[0] = [p[2],p[4]]
    
    def p_iorange(self,p):
        """ iorange : iosign range
                    | iosign"""
        if(len(p) == 3):
            p[1].extend(p[2])
            p[0] = p[1]
        else:
            p[1].extend([None,None])
            p[0] = p[1]
        
    def p_expr(self,p):
        "expr : NUMBER"
        p[0] = p[1]
    

    def p_error(self,p):
        #print(p.type)
        self.parse.errok()
        pass
    
m = Parse()
data = """module
 ID(
     output [12:0]aqw,ert,
     output[2:3] b,r,t,w,qqs,ds)
 endmodule
"""
(m.run(data))
print(m.ports)
