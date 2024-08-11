import tkinter as tk
from tkinter import simpledialog

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

def calculator():
    root = tk.Tk()
    # root.withdraw()  # Hide the root window

    operations = {"1": add, "2": subtract, "3": multiply, "4": divide}

    choice = simpledialog.askstring("계산기", "연산 선택:\n1. 더하기\n2. 빼기\n3. 곱하기\n4. 나누기")

    if choice in operations:
        num1 = float(simpledialog.askstring("Input", "첫 번째 숫자를 입력하세요:"))
        num2 = float(simpledialog.askstring("Input", "두 번째 숫자를 입력하세요:"))

        result = operations[choice](num1, num2)
        simpledialog.messagebox.showinfo("Result", f"결과: {result}")
    else:
        simpledialog.messagebox.showerror("Error", "잘못된 입력입니다")

# Run the calculator
calculator()




