import tkinter as tk
from tkinter import messagebox

def calcular():
    try:
        # Valores dos campos
        capital = float(entrada_capital_inicial.get().replace(',', '.'))
        tipo_ativo = var_tipo_ativo.get()
        tempo = float(entrada_tempo.get().replace(',','.'))
        tipo_tempo = var_tipo_tempo.get()
        
        # Meses para anos
        if tipo_tempo == "2":
            tempo /= 12
        
        # Lógica de taxas
        if tipo_ativo == "POUPANCA":
            selic = float(entrada_taxa_base.get().replace(',', '.')) / 100
            taxa_referencial = 0.01
            if selic > 0.085:
                # mes capitlizado para 1 ano = ~6.17%
                taxa_anual_base = (1 + 0.005) ** 12 - 1
                taxa = taxa_anual_base + taxa_referencial
            else:
                taxa = (selic * 0.7) + taxa_referencial
        else:
            cdi = float(entrada_taxa_base.get().replace(',', '.')) / 100
            percentual = float(entrada_percentual.get().replace(',', '.')) / 100
            taxa = cdi * percentual
            
        montante = capital * (1 + taxa) ** tempo
        lucro = montante - capital

        # Imposto
        if tipo_ativo in ("LCI", "LCA", "CRI", "CRA", "POUPANCA"):
            imposto = 0
        else:
            if tempo <= 0.5: aliquota = 0.225
            elif tempo <= 1: aliquota = 0.20
            elif tempo <= 2: aliquota = 0.175
            else: aliquota = 0.15
            imposto = lucro * aliquota
            
        liquido = montante - imposto
        
        resultado = (
            f"Taxa anual: {taxa*100:.2f}%\n"
            f"Valor bruto: R$ {montante:.2f}\n"
            f"Imposto: R$ {imposto:.2f}\n"
            f"Valor líquido: R$ {liquido:.2f}\n"
            f"Lucro: R$ {lucro:.2f}"
        )
        
        label_resposta.config(text=resultado, justify="left")
        
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos")

# Configuração da janela
root = tk.Tk()
root.title("Calculadora de Investimentos")
root.geometry("400x500")

# Entrada
tk.Label(root, text="Capital Investido (R$):").pack(pady=5)
entrada_capital_inicial = tk.Entry(root)
entrada_capital_inicial.pack()

tk.Label(root, text="Tipo de Ativo:").pack(padx=5)
var_tipo_ativo = tk.StringVar(value="CDB")
tk.OptionMenu(root, var_tipo_ativo, "CDB", "LCI", "LCA", "CRI", "CRA", "POUPANCA").pack()

tk.Label(root, text="Taxa de Base (Selic ou CDI %):").pack(pady=5)
entrada_taxa_base = tk.Entry(root)
entrada_taxa_base.pack()

tk.Label(root, text="Percentual do CDI (se aplicável):").pack(pady=5)
entrada_percentual = tk.Entry(root)
entrada_percentual.insert(0, "100")
entrada_percentual.pack()

tk.Label(root, text="Tempo:").pack(pady=5)
entrada_tempo = tk.Entry(root)
entrada_tempo.pack()

var_tipo_tempo = tk.StringVar(value="1")
tk.Radiobutton(root, text="Anos", variable=var_tipo_tempo, value="1").pack()
tk.Radiobutton(root, text="Meses", variable=var_tipo_tempo, value="2").pack()

# Resultado
tk.Button(root, text="Calcular", command=calcular, bg="green", fg="white").pack(pady=20)
label_resposta = tk.Label(root, text="", font=("Arial", 12, "bold"))
label_resposta.pack()

root.mainloop()
