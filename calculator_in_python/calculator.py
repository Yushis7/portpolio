# import tkinter as tk
# from tkinter import simpledialog

# def add(x, y):
#     return x + y

# def subtract(x, y):
#     return x - y

# def multiply(x, y):
#     return x * y

# def divide(x, y):
#     if y == 0:
#         return "오류! 0으로 나눌 수 없습니다."
#     return x / y

# def calculator():
#     root = tk.Tk()
#     root.withdraw()  # Hide the root window

#     operations = {"1": add, "2": subtract, "3": multiply, "4": divide}

#     choice = simpledialog.askstring("계산기", "연산 선택:\n1. 더하기\n2. 빼기\n3. 곱하기\n4. 나누기")

#     if choice in operations:
#         num1 = float(simpledialog.askstring("Input", "첫 번째 숫자를 입력하세요:"))
#         num2 = float(simpledialog.askstring("Input", "두 번째 숫자를 입력하세요:"))

#         result = operations[choice](num1, num2)
#         simpledialog.messagebox.showinfo("Result", f"결과: {result}")
#     else:
#         simpledialog.messagebox.showerror("Error", "잘못된 입력입니다")

# # Run the calculator
# calculator()



import tkinter as tk
from tkinter import simpledialog, messagebox

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "오류! 0으로 나눌 수 없습니다."
    return x / y

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        root.title("계산기")
        self.expression = ""
        self.text_input = tk.StringVar()

        self.display = tk.Entry(root, textvariable=self.text_input, font=('arial', 20, 'bold'), bd=30, insertwidth=4, width=14, justify='right')
        self.display.grid(row=0, column=0, columnspan=4)

        self.create_buttons()

    def create_buttons(self):
        button_texts = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('/', 4, 3)
            
        ]

        for (text, row, col) in button_texts:
            self.create_button(text, row, col)

    def create_button(self, text, row, col):
        button = tk.Button(self.root, text=text, padx=20, pady=20, font=('arial', 20, 'bold'),
                           command=lambda: self.on_button_click(text))
        button.grid(row=row, column=col)

    def on_button_click(self, char):
        if char == '=':
            self.calculate_result()
        else:
            self.expression += str(char)
            self.text_input.set(self.expression)

    def calculate_result(self):
        try:
            # Evaluate the expression using eval
            result = eval(self.expression)
            self.text_input.set(result)
            self.expression = str(result)
        except Exception as e:
            self.text_input.set("오류")
            self.expression = ""

# Run the calculator with GUI keypad
root = tk.Tk()
app = CalculatorApp(root)
root.mainloop()
