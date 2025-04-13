def simple_calculator(operation, num1, num2):
    if operation not in ["add", "subtract", "multiply", "divide"]:
        return "Invalid operation. Please choose from 'add', 'subtract', 'multiply', 'divide'."
    
    try:
        if operation == "add":
            return num1 + num2
        elif operation == "subtract":
            return num1 - num2
        elif operation == "multiply":
            return num1 * num2
        elif operation == "divide":
            if num2 == 0:
                return "Error: Division by zero is not allowed."
            return num1 / num2
    except TypeError:
        return "Invalid number input. Please provide valid numbers."