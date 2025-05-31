import tkinter as tk
from tkinter import messagebox


class TelaCotacaoMoedas(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cotações de Moedas")
        self.geometry("350x200")
        self.db = master.db

        self.criar_widgets()
        self.atualizar_cotacoes()

    def criar_widgets(self):

        frame = tk.Frame(self)
        frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.label_dolar_titulo = tk.Label(frame, text="Dólar (USD):", font=('Arial', 10, 'bold'))
        self.label_dolar_titulo.grid(row=0, column=0, sticky="w")

        self.label_dolar = tk.Label(frame, text="R$ 0,0000", font=('Arial', 10))
        self.label_dolar.grid(row=0, column=1, sticky="e")

        self.label_euro_titulo = tk.Label(frame, text="Euro (EUR):", font=('Arial', 10, 'bold'))
        self.label_euro_titulo.grid(row=1, column=0, sticky="w", pady=10)

        self.label_euro = tk.Label(frame, text="R$ 0,0000", font=('Arial', 10))
        self.label_euro.grid(row=1, column=1, sticky="e", pady=10)

        self.label_atualizado = tk.Label(frame, text="", font=('Arial', 8))
        self.label_atualizado.grid(row=2, column=0, columnspan=2, pady=10)

        self.btn_atualizar = tk.Button(
            frame,
            text="Atualizar Cotações",
            command=self.atualizar_cotacoes,
            bg="#4CAF50",
            fg="white"
        )
        self.btn_atualizar.grid(row=3, column=0, columnspan=2, pady=10)

    def atualizar_cotacoes(self):
        self.btn_atualizar.config(state=tk.DISABLED, text="Atualizando...")
        self.update()

        try:
            # Substitua esta parte pela implementação real da API de cotações
            cotacoes = {
                'dolar': 5.0,
                'euro': 5.5,
                'atualizado': '01/01/2023'
            }

            if cotacoes:
                self.label_dolar.config(text=f"R$ {cotacoes['dolar']:.4f}")
                self.label_euro.config(text=f"R$ {cotacoes['euro']:.4f}")
                self.label_atualizado.config(
                    text=f"Última atualização: {cotacoes['atualizado']}",
                    fg="green"
                )
            else:
                raise ValueError("Não foi possível obter as cotações")
        except Exception as e:
            self.label_atualizado.config(
                text=f"Erro ao obter cotações: {str(e)}",
                fg="red"
            )
        finally:
            self.btn_atualizar.config(state=tk.NORMAL, text="Atualizar Cotações")