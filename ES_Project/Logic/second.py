import aima1.logic as l
from aima1.utils import *


rules=[
    expr("Different(x,y) ==> Different(y,x)"),
    expr("Color(x) & Color(y) & Different(x,y) ==> ColorDifferent(x,y)"),
    expr('ColorDifferent(x,y) ==> ColorDifferent(y,x)'),
    expr("ColorDifferent(c1,c2) & ColorDifferent(c1,c3)& ColorDifferent(c1,c5) & ColorDifferent(c1,c6) & ColorDifferent(c2,c4) & ColorDifferent(c2,c5) & ColorDifferent(c2,c3) & ColorDifferent(c2,c6) & ColorDifferent(c3,c4) & ColorDifferent(c3,c6) & ColorDifferent(c5,c6) ==> Map(c1,c2,c3,c4,c5,c6)")
]

facts=[
    expr("ColorDifferent(Blue,Black)"),
    expr("ColorDifferent(Blue,White)"),
    expr("ColorDifferent(Blue,Green)"),
    expr("ColorDifferent(Green,White)"),
    expr("ColorDifferent(Green,Black)"),
    expr("ColorDifferent(White,Black)"),
]

kb = l.FolKB(rules+facts)

print(list(l.fol_fc_ask(kb,expr("ColorDifferent(x,y)"))))