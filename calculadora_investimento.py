from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import requests
from tkcalendar import DateEntry


class CalculadoraInvestimento:
	def __init__(self, root):
		self.root = root
		self.root.title('Calculadora financeira')
		self.root.geometry('420x450')

		self.taxa_cdi_anual = self.buscar_cdi()
		self.setup_ui()

	def buscar_cdi(self):
		# Buscar CDI no Banco Central
		try:
			url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados/ultimos/1?formato=json'
			valor = float(requests.get(url).json()[0]['valor'])
			return round(((1 + valor / 100) ** 252 - 1) * 100, 2)
		except:
			return 10.50

	def setup_ui(self):
		# Container principal
		main_frame = ttk.Frame(self.root, padding='20')
		main_frame.pack(fill='both', expand=True)

		# Capital
		ttk.Label(main_frame, text='Capital Inicial (R$):').pack(anchor='w')
		self.ent_capital = ttk.Entry(main_frame)
		self.ent_capital.pack(fill='x', pady=5)

		# Tipo de ativo
		ttk.Label(main_frame, text='Tipo de Investimento:').pack(anchor='w')
		self.combo_ativo = ttk.Combobox(
			main_frame, values=['CDB Pós', 'CDB Pré', 'LCI/LCA Pós', 'Poupança']
		)
		self.combo_ativo.current(0)
		self.combo_ativo.pack(fill='x', pady=5)

		# Taxa (dinamica)
		ttk.Label(main_frame, text="Taxa Anual (%) ou '%' do CDI:").pack(anchor='w')
		self.ent_taxa = ttk.Entry(main_frame)
		self.ent_taxa.insert(0, '100')  # 100% CDI
		self.ent_taxa.pack(fill='x', pady=5)

		# Tempo
		ttk.Label(main_frame, text='Data de Vencimento:').pack(anchor='w')
		self.ent_vencimento = DateEntry(
			main_frame,
			width=12,
			background='darkblue',
			foregound='white',
			borderwidth=2,
			date_pattern='dd/MM/yyyy',
		)
		self.ent_vencimento.pack(fill='x', pady=5)

		# Calcular
		self.btn_calc = tk.Button(
			main_frame,
			text='CALCULAR',
			bg='#2ecc71',
			fg='white',
			font=('Arial', 10, 'bold'),
			anchor='center',
			justify='center',
			command=self.processar_calculo,
		)
		self.btn_calc.pack(fill='x', pady=10, side='bottom')

		# Resultado
		self.lbl_res = ttk.Label(
			main_frame, text='', font=('Arial', 13), justify='left', anchor='center'
		)
		self.lbl_res.pack(fill='both', pady=10)

	def calcular_ir(self, lucro, prazo_anos):
		dias = prazo_anos * 365
		if dias <= 180:
			return lucro * 0.225
		if dias <= 360:
			return lucro * 0.20
		if dias <= 720:
			return lucro * 0.175
		return lucro * 0.15

	def processar_calculo(self):
		try:
			capital_input = float(self.ent_capital.get().replace(',', '.'))
			ativo = self.combo_ativo.get()
			taxa_input = float(self.ent_taxa.get().replace(',', '.')) / 100

			# Captura a data atual
			data_hoje = datetime.now().date()

			# Captura a data do componente
			data_vencimento = self.ent_vencimento.get_date()

			# Calcula diferença em dias
			diferenca_dias = (data_vencimento - data_hoje).days

			if diferenca_dias <= 0:
				messagebox.showerror(
					'Erro', 'A data de vencimento deve ser maior que a data de hoje.'
				)
				return

			# 4. Converte os dias exatos para anos (base 365)
			tempo_anos = diferenca_dias / 365.0

			# Lógica de taxa por ativo
			if 'Pós' in ativo:
				taxa_anual = (self.taxa_cdi_anual / 100) * taxa_input
			elif 'Poupança' in ativo:
				# Poupança (selic > 8.5% = 0.5% am + TR)
				taxa_anual = 0.0617  # Aproximação de 6.17% aa + TR
			else:  # Prefixado
				taxa_anual = taxa_input

			# Juros compostos
			bruto = capital_input * (1 + taxa_anual) ** tempo_anos
			lucro = bruto - capital_input

			# Imposto
			isento = any(x in ativo for x in ['LCI', 'LCA', 'Poupança'])
			ir = 0 if isento else self.calcular_ir(lucro, tempo_anos)
			liquido = bruto - ir

			res_text = (
				f'RESULTADO\n'
				f'Taxa Aplicada: {taxa_anual * 100:.2f}% a.a.\n'
				f'Bruto: R$ {bruto:.2f}\n'
				f'IR: R$ {ir:.2f}\n'
				f'Líquido: R$ {liquido:.2f}\n'
				f'Rentabilidade: {(liquido / capital_input - 1) * 100:.2f}%\n'
			)
			self.lbl_res.config(text=res_text)

		except Exception as e:
			messagebox.showerror(
				'Erro', 'Verifique os todos os campos foram preenchidos corretamente.'
			)


if __name__ == '__main__':
	root = tk.Tk()
	app = CalculadoraInvestimento(root)
	root.mainloop()
