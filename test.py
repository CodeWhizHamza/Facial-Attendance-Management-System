import tkinter as tk

window = tk.Tk()
window.title("How you want to proceed?")
window.geometry("700x400")

# functions


def now_you_are_admin():
    admin_windows = tk.Tk()
    admin_windows.title("Admin panel")
    admin_windows.geometry("700x450")

    admin_windows.mainloop()


def continue_as_admin():
    signin_windows = tk.Tk()
    signin_windows.title("Sign in")
    signin_windows.geometry("400x240")

    def signin():
        username = username_entry.get()
        password = password_entry.get()

        if len(username) == 0:
            message.set("username cannot be empty")
            messageLabel.config(text=message.get())
            return
        else:
            message.set("")
            messageLabel.config(text=message.get())
        if len(password) == 0:
            message.set("password cannot be empty")
            messageLabel.config(text=message.get())
            return
        else:
            message.set("")
            messageLabel.config(text=message.get())

        if username != 'abc' or password != '123':
            message.set("Invalid credentials")
            messageLabel.config(text=message.get())
            return

        signin_windows.destroy()
        now_you_are_admin()

    message = tk.StringVar()
    messageLabel = tk.Label(
        master=signin_windows, text=message.get(), font="Arial 14", foreground='red')
    messageLabel.pack()

    username_entry = tk.Entry(master=signin_windows, font="Arial 14")
    username_entry.pack()
    password_entry = tk.Entry(master=signin_windows, font="Arial 14", show="*")
    password_entry.pack()

    signin_button = tk.Button(master=signin_windows,
                              text="Sign in", font="Arial 14", command=signin)
    signin_button.pack()

    signin_windows.mainloop()


def continue_as_user():
    print("You're going like an normal user.")

# widgets (buttons, entries, labels)


adminButton = tk.Button(
    master=window, text="Continue as admin", font="Arial 16", command=continue_as_admin)
userButton = tk.Button(
    master=window, text="Continue as normal user", font="Arial 16", command=continue_as_user)

adminButton.pack()
userButton.pack()

window.mainloop()
