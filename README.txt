_________________________________________________________________________
P-Entailment Solver 
_________________________________________________________________________ 
 

0. Installation

To run the program, a computer must have Python 3.x installed. The program 
was written on Python 3.6 but may run correctly on older versions. Version 
3.4 or higher, however, is recommended. The program can be opened in on the 
command-line in Windows or Linux machines. 

In the command line, go to the directory in which you have placed the 
folder containing the program and type:

	python z_main.py

(If you have Anaconda installed on your computer you need only type 
“z_main.py”)

The program makes use of the logic module from the sympy library. It is 
recommended that the user employ pip when installing Python libraries. To 
install sympy simply type:

       pip install sympy	(perhaps with a “sudo”)


If you have both Python 2.x and 3.x installed on your system, it might 
run Python 2.x by default, which will cause trouble both when trying to 
run the program and when installing modules. 

If this is the case, type the following into the command prompt: 
	
	alias python='/usr/bin/python3'   (Linex)
	
	alias python='python3'		  (Mac)

Then install sympy as follows:
	
	python3.x -m pip install sympy    (Mac)

If you have trouble installing through pip, please try using Easy Install:

	easy_install sympy		(perhaps with sudo prefixed)

This second way of installing sympy may be necessary even if you already
have python 3 active.

If none of these methods of installing sympy work see:

http://docs.sympy.org/latest/install.html

_________________________________________________________________________


1. Introduction

The program checks whether or not a formula 'a' p-entails a formula 'b' given
a set R of rules and a set C of constraints.   

p-entailment was introduced in Adams (1975). The current program makes use of
an algorithm outlined by Pearl (1990). 
  
_________________________________________________________________________

2. Rules and Constraints

Rulesets are provided by the user in the form of ‘.txt’ files. Upon starting
the program, the user will be asked if he or she would like to open a file.

Rules must be written in the following format: (b -> h), where 'b' and 'h' are
formulas of propositional logic. "&" is used for "and", "|" is used for "or", 
and "~" is used for “not”. Material implication must be expressed in terms of 
these symbols.

Atomic propositions are composed of Latin letters. I, E, S, N, C, O, and Q, 
however, should not be used because sympy reserves them for imaginary numbers.
It is recommended that the user stick with lower-case letters.  

	Example 1:	((~par | (~qu | r)) -> (qu & par)) 

Constraints are formulas preceded by an “!” 

	Example 2:	! ~c | ~f  

Worlds that do not satisify all constraints will not be taken into
consideration when evaulating preferences.

The program is flexible regarding the use of parentheses, with the following 
exceptions:

	(1) The outermost parentheses for rules must be included (for constraints they are optional)
	(2) Any parentheses required for removing ambiguity from the      
            meaning of a formula must be included 

Spacing within a line is ignored. The following rule is perfectly acceptable: 

	Example 3: (abs   & ~b &c -> p | q |re) 
 
IMPORTANT: Rules must appear on lines by themselves or the program will not 
be able to parse them correctly. Also, the first character of a rule line MUST 
be “(“.

Rules do not need to have bodies, but they do need to have heads.
	
	Example 4: (  -> p|q)

In this example, p or q ought to be the case by default, but this default might
be overturned by a rule with a body:
	
	Example 5: (r -> ~(p|q))

“TRUE” and “FALSE” can be used when defining rules: 
	
       Example 6: (pm & hs -> FALSE)
       
       Example 7: (TRUE -> p|q)
       
       Example 8: (~(p|q) -> FALSE)

Ex. 6 is the rule that, normally, pm and hs are not both true. Ex. 7 and 8 are
both notational variants of Ex.3.  
	

Some example ruleset text files are included with the program. 
  
_________________________________________________________________________

3. Entailment Checking

The program is quite simple. Once a file has been loaded the user is asked to check 
for the soundness of various inferences based on R. When checking for a |- b, the 
user will be asked to first input formula 'a' and then formula 'b'. The program
will then tell the user if the entailement holds. 
 




_________________________________________________________________________

References

Adams, E. 1975. The logic of conditionals. Dordrecht, The Netherlands: D. Reidel

Judea Pearl. 1990. System Z: a natural ordering of defaults with tractable
applications to nonmonotonic reasoning. In Proceedings of the 3rd conference
on Theoretical aspects of reasoning about knowledge (TARK '90). Morgan Kaufmann
Publishers Inc., San Francisco, CA, USA, 121-135.

.

