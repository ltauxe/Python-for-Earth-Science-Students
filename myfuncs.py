## module myfuncs
def gimmepi():  
    """
    returns pi
    """
    return 3.141592653589793
def deg2rad(degrees):  
    """
    converts degrees to radians
    """
    return degrees*3.141592653589793/180.
def print_args(*args):
    """
    prints argument list
    """
    print ('You sent me these arguments: ')
    for arg in args:
        print (arg)

