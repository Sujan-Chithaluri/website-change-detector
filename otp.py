import random 
import string 
     
def rand_pass(): 
    generate_pass = ''.join([random.choice( string.ascii_uppercase +
                                            string.ascii_lowercase +
                                            string.digits) 
                                            for n in range(10)])                     
    return generate_pass 
    
# x=str(rand_pass())
# print(x)    