import numpy as np
import matplotlib.pylab as plt

def EqualAngle(Pl):
    """
    returns mapped plunge into equal angle projection
    """
    return 90.*np.tan(np.radians(90.-Pl)/(2.)) # convert to radians!

def EqualArea(Pl): ### Pl is an angle in degrees
    """
    returns mapped plunge into equal area projection
    """
    return np.sqrt(2.)*90.*np.sin(np.radians(90.-Pl)/(2.))

def dir2cart(Dir):
    if len(Dir)>2:
        R=Dir[2]
    else:
        R=1.
    Az,Pl=np.radians(Dir[0]),np.radians(Dir[1])
    return [R*np.cos(Az)*np.cos(Pl),R*np.sin(Az)*np.cos(Pl),R*np.sin(Pl)]
 
def cart2dir(X):
    R=np.sqrt(X[0]**2+X[1]**2+X[2]**2) # calculate resultant vector length
    Az=np.degrees(np.arctan2(X[1],X[0]))%360. # calculate declination taking care of correct quadrants (arctan2) and making modulo 360.
    Pl=np.degrees(np.arcsin(X[2]/R)) # calculate inclination (converting to degrees) #
    return [Az,Pl,R]

