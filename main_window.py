import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import threading
import queue

class VulDeePeckerInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("VulDeePecker Interface")

        self.file_label = tk.Label(root, text="Select a gadget file:")
        self.file_label.pack()

        self.file_entry = tk.Entry(root, width=50)
        self.file_entry.pack()

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.run_button = tk.Button(root, text="Run VulDeePecker", command=self.run_vuldeepecker)
        self.run_button.pack()

        self.output_text = tk.Text(root, height=10, width=80)
        self.output_text.pack()

        self.queue = queue.Queue()

    def browse_file(self):
        filename = filedialog.askopenfilename(title="Select a gadget file", filetypes=[("Text files", "*.txt")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, filename)

    def run_vuldeepecker(self):
        filename = self.file_entry.get()
        if not filename:
            self.output_text.insert(tk.END, "Please select a gadget file.\n")
            return
        command = f"python vuldeepecker.py {filename}"
        self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=1)
        self.thread = threading.Thread(target=self.read_output)
        self.thread.daemon = True
        self.thread.start()
        self.update_output()

    def read_output(self):
        for line in iter(self.process.stdout.readline, ''):
            self.queue.put(line)
        self.process.stdout.close()
        self.process.wait()

    def update_output(self):
        while not self.queue.empty():
            line = self.queue.get()
            self.output_text.insert(tk.END, line)
            self.output_text.see(tk.END)
        self.root.after(100, self.update_output)

if __name__ == "__main__":
    root = tk.Tk()
    interface = VulDeePeckerInterface(root)
    root.mainloop()