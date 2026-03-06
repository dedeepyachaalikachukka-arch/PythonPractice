class Calculator:

    def add(self, numbers):
        return sum(numbers)
    
    def subtract(self, numbers):
       result = numbers[0]
       for num in numbers[1:]:
         result = result - num
       return result
    
class MathOperations:

    def perform_operations(self):
        calc = Calculator()

        n = int(input("How many numbers do you want to enter? "))

        numbers = []

        for _ in range(n):
           numbers.append(int(input("Enter number: ")))

        
        result1 = calc.add(numbers)
        result2 = calc.subtract(numbers)

        print("Addition:", result1)
        print("Subtraction:", result2)


if __name__ == "__main__":
    obj = MathOperations()
    obj.perform_operations()

        

     
