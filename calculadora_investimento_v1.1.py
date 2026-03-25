def limpar_float(mensagem):
    # Função para capturar e limpar entradas númericas
    try:
        return float(input(mensagem).replace(',', '.'))
    except ValueError:
        print("Erro: Digite um valor númerico válido.")
        exit()

def calcular_imposto(lucro, tempo_anos, tipo_ativo):
    # Separar lógica tributária
    if tipo_ativo in (2, 3, 4, 5, 6):
        return 0
    if tempo_anos <= 0.5: aliquota = 0.225
    elif tempo_anos <= 1: aliquota = 0.20
    elif tempo_anos <=2: aliquota = 0.175
    else: aliquota = 0.15
    return lucro * aliquota

# Fluxo principal
print("=== CALCULADORA DE INVESTIMENTO ===")

capital = limpar_float("Digite o valor investido R$:\n")

print("\nEscolha o ativo:\n1.CDB | 2.LCI | 3.LCA | 4.CRI | 5.CRA | 6.POUPANCA")
tipo = int(input("\nDigite o número da opção:\n"))

# Lógica de taxas
if tipo == 6:
    selic = limpar_float("\nDigite a taxa Selic ('%' ao ano):\n") / 100
    taxa_referencial = 0.01
    if selic > 0.085:
        taxa_anual_base = (1 + 0.005) ** 12 - 1
        taxa = taxa_anual_base + taxa_referencial
    else:
        taxa = (selic * 0.7) + taxa_referencial
else:
    cdi = limpar_float("\nDigite o CDI ('%' ao ano):\n") / 100
    percentual = limpar_float("\nDigite o '%' do CDI do ativo:\n") / 100
    taxa = cdi * percentual

# Tempo
print("\nEscolha um tipo de tempo:\n1.ANOS | 2.MESES")
modo = int(limpar_float("\nDigite a opção de tempo:\n"))
tempo = limpar_float("\nDigite a quantidade de tempo:\n")
    
if modo == 2:
    tempo /= 12

montante = capital * (1 + taxa) ** tempo
lucro = montante - capital
imposto = calcular_imposto(lucro, tempo, tipo)
liquido = montante - imposto
        
# Resultado
print("\n======= RESULTADO =======")
print(f"Taxa anual:        {taxa*100:.2f}%")
print(f"Valor bruto:    R$ {montante:.2f}")
print(f"Imposto:        R$ {imposto:.2f}")
print(f"Lucro:          R$ {lucro:.2f}")
print("----------------------------")
print(f"Valor líquido:  R$ {liquido:.2f}")