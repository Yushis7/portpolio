#만든 코드 exe로 프로그램 짜기
#pip install pyinstaller
#pyinstaller --onefile --windowed stopwatch.py
#cd path\to\your\script
#pyinstaller --onefile --windowed stopwatch.py
#cd dist



import tkinter as tk
from datetime import datetime, timedelta



class Stopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch")
        self.running = False
        self.start_time = None
        self.elapsed_time = timedelta()
        
        self.time_label = tk.Label(root, text="00:00:00", font=("Helvetica", 48))
        self.time_label.pack()
        
        self.start_button = tk.Button(root, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT)
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT)

        self.update_clock()

    def update_clock(self):
        if self.running:
            now = datetime.now()
            self.elapsed_time = now - self.start_time
            self.time_label.config(text=str(self.elapsed_time).split(".")[0])
        self.root.after(50, self.update_clock)

    def start(self):
        if not self.running:
            self.start_time = datetime.now() - self.elapsed_time
            self.running = True

    def stop(self):
        if self.running:
            self.elapsed_time = datetime.now() - self.start_time
            self.running = False

    def reset(self):
        self.running = False
        self.start_time = None
        self.elapsed_time = timedelta()
        self.time_label.config(text="00:00:00")

if __name__ == "__main__":
    root = tk.Tk()
    stopwatch = Stopwatch(root)
    root.mainloop()

