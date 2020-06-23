import os
import  django
import sys
print(__file__)
print(os.path.abspath(__file__))

print(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)
print(sys.path)
