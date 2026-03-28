# added __init__.py file to mark this directory as a package 

# File is executed once, the first time any module from 
# this package is imported. Printing message to illustrate.

print('Initializing src package')


# define modules visible using import * 
__all__ = ['game']


# import these modules into the package's namespace 
from .game import Game 