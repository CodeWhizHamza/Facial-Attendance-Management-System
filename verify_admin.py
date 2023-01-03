import tkinter as tk
import customtkinter as ctk
from helper import truncateWidget
from config import password
import attendance
from tkinter.messagebox import showwarning


def isAdmin(rightFrame, message, root_window):
    """This function will verify the admin password.

    Args:
        rightFrame (ctk.CTkFrame): This is the right frame.
        message (string): This is the message to be displayed.
        root_window (tk.Tk): This is the root window.
    """
    font40 = ctk.CTkFont('Arial', 40)
    font24 = ctk.CTkFont('Arial', 24)

    def verifyPassword():
        """This function will verify the password.

        Returns:
            bool: This is the result of the verification.
        """
        if passwordEntry.get() == password:
            return True
        else:
            return False

    def verifyAdmin():
        """This function will verify the admin password.

        If the password is correct, it will call the attendance.main function.
        """
        if verifyPassword():
            attendance.main(rightFrame, root_window)
        else:
            showwarning("Warning", "Invalid admin password.")
            isAdmin(rightFrame, "Invalid admin password.")

    truncateWidget(rightFrame)

    emptyFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", height=120)
    emptyFrame.pack(side=tk.TOP, fill=tk.X)

    rightHeaderFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=80)
    rightHeaderFrame.pack(side=tk.TOP, fill=tk.X)

    rightHeaderLabel = tk.Label(
        master=rightHeaderFrame, text="Verify your password" if not message else message, font=font40, bg="#ffffff", fg="#333333", justify='left', anchor='w', wraplength=960)
    rightHeaderLabel.pack(fill=tk.X, side=tk.LEFT, padx=80)

    # entry to enter password
    passwordEntryFrame = ctk.CTkFrame(
        master=rightFrame, bg_color="transparent", fg_color="transparent", width=960, height=80)
    passwordEntryFrame.pack(side=tk.TOP, fill=tk.X,
                            padx=80, pady=32, anchor=tk.W)

    passwordEntryLabel = tk.Label(
        master=passwordEntryFrame, text="Password: ", font=font24, bg="#ffffff", fg="#333333", justify='left')
    passwordEntryLabel.pack(fill=tk.X, side=tk.LEFT)

    passwordEntry = ctk.CTkEntry(
        master=passwordEntryFrame, font=font24, bg_color="#ffffff", fg_color="#ffffff", text_color="#333333", justify='left', width=300, show='●')
    passwordEntry.pack(fill=tk.X, side=tk.LEFT, padx=16)

    # buttons
    submitButton = tk.Button(master=rightFrame, text="Verify", font=font24, bg="#6FFD9D", fg="#333333", activebackground="#62E48C",
                             activeforeground="#333333", bd=0, highlightthickness=0, relief=tk.FLAT, padx=24, pady=12, command=verifyAdmin)
    submitButton.pack(side=tk.TOP, padx=80, anchor=tk.W)
