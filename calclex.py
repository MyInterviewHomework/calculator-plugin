#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

#---------------------------- ------------------------------------------------------------
# calclex.py
#
# Tokenizer for simple integer expressions including addition, subtraction and parenthesis
## ---------------------------------------------------------------------------------------

import ply.lex as lex

class CalcLex:
	"""This class implements the lexer for integer expression like 41+(3-2).
	CalcLex it used in conjunction with CalcYacc
	
	:Example:
		
	obj = CalcLex(**kwargs)
	"""
	# List of token names.
	tokens = (
	   'NUMBER',
	   'PLUS',
	   'MINUS',
	#   'TIMES',
	   'LPAREN',
	   'RPAREN',
	)
	
	# Regular expression rules for simple tokens
	t_PLUS    = r'\+'
	t_MINUS   = r'-'
	#t_TIMES   = r'\*'
	t_LPAREN  = r'\('
	t_RPAREN  = r'\)'
	
	# A string containing ignored characters (spaces and tabs)
	t_ignore  = ' \t'
	
	def __init__(self):
	    """The constructor of class CalcLex. 
		.. note:: Not argument is required.
	    """
	    self.error = False
	    self.lexer = None

	# A regular expression rule with some action code
	def t_NUMBER(self,t):
	    r'\d+'
	    t.value = int(t.value)    
	    return t
	
	# Error handling rule
	def t_error(self,t):
	    raise SyntaxError("Illegal character '%s'. Try again ..." % t.value[0])
	    #print("Illegal character '%s'" % t.value[0])
	    #t.lexer.skip(1)
	    #self.error = True
	
	# Build the lexer
	def build(self,**kwargs):
	    """Build the lexer. 
	    :param **kwargs : Any param
			    
	    :Example:
		
	    obj.build(**kwargs)
	    """
	    self.lexer = lex.lex(module=self, **kwargs)
	    return self.lexer

