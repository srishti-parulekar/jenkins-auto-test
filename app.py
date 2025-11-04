class SmartCalc:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, a, b):
        return a ** b
    
    def sqrt(self, a):
        if a < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return a ** 0.5
if __name__ == "__main__":
    calc = SmartCalc()
    print("SmartCalc Service Running!")
    print(f"2 + 3 = {calc.add(2, 3)}")
    print(f"5 - 2 = {calc.subtract(5, 2)}")
