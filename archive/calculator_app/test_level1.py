import unittest
from calculator_app.app import Calculator

class TestOperations(unittest.TestCase):
    # ARRANGE, ACT and  ASSERT <- General template
    
    def test_sum(self):
        #ARRANGE
        testCalc = Calculator(8,2)
        #ACT and ASSERT
        self.assertEqual(testCalc.get_sum(), 10 , 'The sum is wrong')

    def test_minus(self):
        #ARRANGE
        testCalc = Calculator(8,2)
        #ACT and ASSERT
        self.assertEqual(testCalc.get_minus, 6 , 'The minus is wrong')

    def test_division(self):
        #ARRANGE
        testCalc = Calculator(8,2)
        #ACT and ASSERT
        self.assertEqual(testCalc.get_divison, 4 , 'The divsion is wrong')
    
    def test_product(self):
        #ARRANGE
        testCalc = Calculator(8,2)
        #ACT and ASSERT
        self.assertEqual(testCalc.get_product, 16 , 'The product is wrong')


if __name__ == "__main__":
    unittest.main()