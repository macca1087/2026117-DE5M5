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
    

if __name__ == "main":
    myCalc = Calculator(a=5, b=6)
    print(myCalc.get_sum())