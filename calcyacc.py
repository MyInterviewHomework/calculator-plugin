#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

"""
#----------------------------------------------------------------------------------------------
# calcyass.py
#
# Yass calculator for simple integer expressions including addition, subtraction and parenthesis
## ---------------------------------------------------------------------------------------------
"""

import ply.yacc as yacc

# Get the token map from the lexer.
import calclex

tokens = calclex.CalcLex.tokens


# Declaration of the grammar and specification as follows #

# expression : expression + factor
#            | expression - factor
#            | factor
# 
# factor     : NUMBER
#            | ( expression )

def p_expression_plus(p):
    'expression : expression PLUS factor'
    p[0] = p[1] + p[3] 

def p_expression_minus(p):
    'expression : expression MINUS factor'
    p[0] = p[1] - p[3]

def p_expression_factor(p):
    'expression : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    raise SyntaxError("Oops! That was not a valid expression. Try again ...")

parser = yacc.yacc()


class CalcYacc:
	"""This class implements the grammar for integer expression like 41+(3-2)
	The expression is provides to the class objct using the method 
	.. seealso:: calcul() 
    """
	def __init__(self,**kwargs):
	    """The constructor of class CalcYacc. 
		:param **kwargs : Any param
			    
		:Example:
		
		obj = CalcYacc(**kwargs)
		
		.. warning:: Arguments are not yet implemented !		
		"""
	    self.result = None
	    self.calclexer = calclex.CalcLex()
	    self.calclexer.build(**kwargs)

	def calcul(self,data):
	   """Parse and compute the value of the given integer expression. 
	   :param expr : The expression to parse
	   :type expr: string defining an integer operation
	   :return: The integer value of the expr
	   :rtype: int
	   
	   :Example:
	   
	   >>>obj.calcul(expression)
	   """
	   self.result = parser.parse(str(data)) 
	   return self.result

if __name__ == "__main__":
    calc = CalcYacc()
    while True:
    	try:
		expr = str(input("Calculator > "))
    		res = calc.calcul(expr)
    		print res
    	except KeyboardInterrupt:
    		print "Exiting calculator"
    		break
    	except SyntaxError,e: 
    		print e
