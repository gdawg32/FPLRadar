import Visual as vs
import mapping as mp

#Input
a = 'Salah'
b = 'Havertz'

#Get FPL IDs
p1 = mp.get_fpl_id(a)
p2 = mp.get_fpl_id(b)

if p1 and p2:
    print("Found a match!")
    vs.visualise(p1, p2)
else:
    print("No match found.")