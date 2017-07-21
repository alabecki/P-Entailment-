
from sympy import Symbol
from sympy.abc import*
from sympy.logic.boolalg import to_cnf
from sympy.logic.boolalg import Not, And, Or
from sympy.logic.inference import satisfiable, valid
from mpmath import*
from itertools import product
import sys
import os
from copy import deepcopy
from shutil import copyfile
from itertools import*
import re

from p_classes import*


def base():
	do = ""
	res = []
	while len(res) == 0:
		print("\n")
		print("What would you like to do? \n")
		do = input("1: Open a file, 2: Exit program\n")
		if(do == "2"):
			sys.exit()
		if(do == "1"):
			print("Please input the name of a text-file containing a set of rules ")
			print("(or press 'r' to return) \n")
			name = input()
			if name != "r":
				res = get_file(name)
				if res == []:
					continue
				#print(type(res))
				return res

		else:
			print("I'm sorry, could you repeat your command? \n")
	return res


def get_file(name):
	while True:
		if name.endswith(".txt") == False:
			name = name + ".txt"
		if(os.path.exists(name)):
			_file = open(name, "r+")
			print("\n")
			print("Name of file: %s " % (name))
			res = [_file, name]
			return res
		else:
			print("The file you selected does not exist, please try again")
			print("(Or press 'r' to return) \n ")
			name = input()
			if name == 'r':
				res = []
				return res

# Scans the rule file for atomic formulas (letters). This is needed to construct the worlds
def obtain_atomic_formulas(file):
	propositions = set()
	for line in file:
		_line = line.strip()
		_line = re.sub(r'\s+', '', _line)
		_line = _line.split("$")
		_line = _line[0]
		if _line.startswith("(") or _line.startswith("!"):
			_line = _line.replace("FALSE", "")
			_line = _line.replace("TRUE", "")
			_line = _line.replace("~", "")
			_line = _line.replace("&", ",")
			_line = _line.replace("|", ",")
			_line = _line.replace("(", "")
			_line = _line.replace(")", "")
			_line = _line.replace("->", ",")
			_line = _line.replace("!", "")
			new_props = _line.split(",")
			new_props = list(filter(None, new_props))
			for prop in new_props:
				if prop == "":
					continue 
				new = Symbol(prop)
				propositions.add(new)
			#propositions.add(_new)
	return propositions



# Parses each line of the rule file to create a dictionary of rules, distinguishing the item, body and head. The key is the name of the rule
# while the value is the Rule object itself
def construct_rules_dict(file):
	lines = []
	for line in file:
		line = line.strip()
		if line.startswith("("):
			line = re.sub(r'\s+', '', line)
			lines.append(line.strip())
	steps = []
	for line in lines:
		steps.append(re.split("->|\$", line))
	for step in steps:
		step[0] = step[0][1:]

		step[1] = step[1][:-1]
	rules = {}
	count = 0
	for line in steps:
		name = "r" + str(count)
		if len(line) == 2:
			item = line[0] + " -> " + line[1]
			new = Rule(name, item, line[0], line[1])
		if len(line) == 3:
			item = line[0] + " -> " + line[1] +  " $ " + line[2]
			if negated == True:
				item = "~" + item
			new = Rule(name, item, line[0], line[1], float(line[2]))
		rules.update({name: new})
		count += 1
	return rules

def add_rule(rule, rules):
	rule = rule.strip()
	rule = re.sub(r'\s+', '', rule)
	step = (re.split("->|\$", rule))
	#print("Step 0 %s " % (step[0]))
	#print("Step 1 %s " % (step[1]))
	step[0] = step[0][1:]
	step[1] = step[1][:-1]
	count = len(rules)
	name = "r" + str(count)
	if len(step) == 1:
		item = " " + " -> " + step[0]
		new = Rule(name, item, " " , step[0])
	if len(step) == 2:
		item = step[0] + " -> " + step[1]
		new = Rule(name, item, step[0], step[1])
	if len(step) == 3:
		item = step[0] + " -> " + step[1] +  " $ " + step[2]
		new = Rule(name, item, step[0], step[1], float(step[2]))
	rules.update({name: new})


def add_constraints(file):
	lines = []
	for line in file:
		line.strip()
		line = re.sub(r'\s+', '', line)
		if line.startswith("!"):
			lines.append(line.strip())
		#for line in lines:
	temp1 = [line[1:] for line in lines]		#remove "!(" at the beginning of the rule
	#temp2 = [line[:-1] for line in temp1]		#remove the ")" at the end of the rule
	constraints = {}
	count = 0
	for line in temp1:
		name = "c" + str(count)
		new = Constraint(name, line)
		constraints.update({name: new})
		count += 1
	return constraints


def prepare_for_SAT(formula):
	for char in formula:
		char = Symbol(char)
	symb_form = to_cnf(formula)
	return symb_form


def rule_conditional_formula(rule):
	print("Body: %s" % (rule.body))
	print("Head: %s" % (rule.head))
	if rule.head == "FALSE":
		formula = "~(" + rule.body + ")"
		return formula
	if rule.head == "~(FALSE)":
		formula = rule.body
		print(formula)
		return formula
	if rule.body == "TRUE":
		formula = rule.head
		return formula
	if rule.body == "~(TRUE)":
		formula = "~(" + rule.head + ")"
		return formula 

	formula = "~(" + rule.body + ")|(" + rule.head + ")"
	return formula



def rule_to_conjuctive_formula(rule):
	print("Body: %s" % (rule.body))
	print("Head: %s" % (rule.head))
	if rule.head == "FALSE":
		formula = "~(" + rule.body + ")"
		return formula 
	if rule.head == "~(FALSE)":
		formula = rule.body
		print(formula)
		return formula
	if rule.body == "TRUE":
		formula = rule.head
		return formula
	if rule.body == "~(TRUE)":
		formula = "~(" + rule.head + ")"
		return formula 
	formula = "(" + rule.body + ")&(" + rule.head + ")"
	return formula


def check_tolerance(item, sub_rules, constraints):
	expression = item
	print(expression)
	for sub in sub_rules.values():
		print("Other: %s" % (sub.item))
		other = rule_conditional_formula(sub)
		print("other before: %s" % (other))
		other = prepare_for_SAT(other)
		print ("Other after: %s" % (other))
		expression = And(expression, other)
	for c in constraints.values():
		restriction = prepare_for_SAT(c.item)
		print(restriction)
		expression = And(expression, restriction)
	print("expression: %s" % (expression))
	if satisfiable(expression):
		print("true")
		return True
	else:
		print("false")
		return False

def z_partition(rules,constraints):
	decomposition = dict()
	count = 0
	remaining_rules = deepcopy(rules)
	remaining_shadow = deepcopy(rules)
	num_rules = len(rules.keys())
	trials = 0
	while len(remaining_rules.keys()) > 0 and count <= num_rules:
		print("Len rules: %s" % (len(remaining_rules.keys())))
		print("Remaining rules:")
		for k, v in remaining_rules.items():
			print(k, v.item)
		temp = []
		for r in remaining_rules.keys():
			print(r, end=" ")
		for r, rule in remaining_rules.items():
			print("Current rule: %s" % (rule.item))
			comp = deepcopy(remaining_rules)
			del comp[r]
			item = deepcopy(rule)
			item = rule_to_conjuctive_formula(item)
			print(item)
			item = prepare_for_SAT(item)
			print(item)
			if check_tolerance(item, comp, constraints) == True:
				temp.append(rule)
				print("Count: %s" % (count))
				print("rule: %s" % (rule.item))
				rules[r].Z = count 
				print("rule z: %s" % (rules[r].Z))
				for t in temp:
					print( t.item)
				del remaining_shadow[r]
		name = "d" + str(count)
		decomposition[name] = temp
		remaining_rules = deepcopy(remaining_shadow)
		if len(remaining_rules.keys()) == 0:
			break
		print("Current len remaining rules: %s" % (len(remaining_rules.keys())))
		count += 1
	if len(remaining_rules.keys()) > 0 :
		decomposition = dict()
	return decomposition


def entailment_0Z(a, b, rules, constraints):			#Need to limit consideration to worlds under consideration
	KB = deepcopy(rules)
	new = "(" + a + "->" + "~(" + b + ") )"
	print("new: %s" % (new))
	add_rule(new, KB)
	print("KB:")
	for k, v in KB.items():
		print(k, v.item)
	decomp = z_partition(KB, constraints)
	if len(decomp.keys()) == 0:
		return True
	else:
		return False

