import argparse
from pathlib import Path
from datetime import datetime

class Calculator:
    def __init__(self,a,b):
        self.a = a
        self.b = b

        self.sean = 2.45

    def get_sum(self):
        return  self.a + self.b
    
    def get_minus(self):
        return  (self.a - self.b) 
    
    def get_divison(self):
        return  (self.a / self.b) 
    
    def get_product(self):
        return  (self.a / self.b) 

    def sean_index(self):
        ans = (self.a + self.b)*self.sean +100
        return ans
    

if __name__ == "__main__":
    myCalc = Calculator(a=247, b=12)
    
    out = Path("/data/my_calc.txt")

    with out.open("a") as f:
        f.write(f"The answer is {(myCalc.get_divison())}  at {datetime.now()} \n")
 