'''
encoding = 'utf-8'

#use subprocess to make command line calls 
p = sub.Popen(['ls', target],stdout=sub.PIPE,stderr=sub.PIPE)

#obtain output and error
output,error = p.communicate()

#decode output into string
output = output.decode(encoding).rstrip('\n')
error = error.decode(encoding).rstrip('\n')

#determine whether output file exist
file_exist = False
if output == target:
    file_exist = True
'''

''' lookahead function

#make iterable 'symbols' into an iterator
self.it = iter(self.symbols)
#get the first element
last = next(self.it)

for cur in it: #starting from second element
   yield last,True
   last = cur
#report last value
yield last,False

'''
