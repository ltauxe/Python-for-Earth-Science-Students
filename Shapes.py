class Circle:
    """
    This is an example of a class called Circle
    """
    import numpy as np # get some math power
    # define some attributes of the Circle class
    pi=np.pi # pi is now an attribute of this class too.  
    # initialize the class   with the attribute r
    def __init__(self,r):
        self.r=r # define a variable, r
    # define some more attributes
    def area(self): 
        return (1./2.)*self.pi*self.r**2
    def circumference(self):
        return 2.*self.pi*self.r
        