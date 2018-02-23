
from probability import *

P = ProbDist('Flip');
P['H'], P['T'] = 0.25, 0.75;
print (P['H'])

print (burglary)
print (burglary.variable_node('Alarm').cpt)
print (burglary.variable_node('JohnCalls').cpt)


print (enumeration_ask('Burglary', {}, burglary)[True])
print (enumeration_ask('Earthquake', {}, burglary)[True])
print (enumeration_ask('Alarm', {}, burglary)[True])
print (enumeration_ask('JohnCalls', {}, burglary)[True])
print (enumeration_ask('MaryCalls', {}, burglary)[True])

