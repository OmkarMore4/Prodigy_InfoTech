import tkinter as tk
from tkinter import ttk
import re

def check_password_strength():
    password = password_entry.get()
    strength = assess_password(password)
    strength_label.config(text=f"Password Strength: {strength}")

    # Provide more detailed feedback (optional)
    feedback = get_feedback(password)
    feedback_label.config(text=feedback)


def assess_password(password):
    if not password:  #handle empty password
        return "Empty"

    length_score = 0
    if len(password) >= 8:
        length_score = 25
    elif len(password) >= 6:
        length_score = 15
    else:
        length_score = 5

    complexity_score = 0
    if re.search(r"[a-z]", password):  # Lowercase
        complexity_score += 25
    if re.search(r"[A-Z]", password):  # Uppercase
        complexity_score += 25
    if re.search(r"[0-9]", password):  # Numbers
        complexity_score += 25
    if re.search(r"[^a-zA-Z0-9]", password):  # Special characters
        complexity_score += 25

    total_score = length_score + complexity_score

    if total_score >= 80:
        return "Strong"
    elif total_score >= 60:
        return "Good"
    elif total_score >= 40:
        return "Weak"
    else:
        return "Very Weak"

def get_feedback(password):
    feedback = ""
    if len(password) < 8:
        feedback += "Password should be at least 8 characters long.\n"
    if not re.search(r"[a-z]", password):
        feedback += "Include lowercase letters.\n"
    if not re.search(r"[A-Z]", password):
        feedback += "Include uppercase letters.\n"
    if not re.search(r"[0-9]", password):
        feedback += "Include numbers.\n"
    if not re.search(r"[^a-zA-Z0-9]", password):
        feedback += "Include special characters (e.g., !@#$%^&*).\n"

    if not feedback:  # If no specific issues, give general advice
        feedback = "Good password! Consider making it even longer and more complex."

    return feedback.strip()  # Remove trailing newline

root = tk.Tk()
root.title("Password Strength Checker")

password_label = ttk.Label(root, text="Password:")
password_label.grid(row=0, column=0, padx=30, pady=30, sticky="w")  # Sticky aligns to the west (left)

password_entry = ttk.Entry(root, show="*") #show="*" hides the password
password_entry.grid(row=0, column=1, padx=30, pady=10, sticky="ew") #sticky="ew" makes the entry expand horizontally

check_button = ttk.Button(root, text="Check", command=check_password_strength)
check_button.grid(row=1, column=0, columnspan=2, pady=(10, 5)) #columnspan makes the button span both columns

strength_label = ttk.Label(root, text="Password Strength:")
strength_label.grid(row=2, column=0, columnspan=2, pady=(5,10))

feedback_label = ttk.Label(root, text="")
feedback_label.grid(row=3, column=0, columnspan=2, sticky="w") #feedback aligned to the left

# Make the password entry expand when the window is resized
root.columnconfigure(1, weight=1)  # Make column 1 (entry) expand

root.mainloop()
