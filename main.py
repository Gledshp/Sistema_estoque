import tkinter as tk
from app.interface.tela_login import TelaLogin

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = TelaLogin()
    app.mainloop()