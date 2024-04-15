#━━━━━━━━━━━━━━━━━━❮Bibliotecas❯━━━━━━━━━━━━━━━━━━
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#━━━━━━━━━━━━━━━━━━❮◆❯━━━━━━━━━━━━━━━━━━

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.circuit import ClassicalRegister


#━━━━━━━━━━━━━━━━━━❮◆❯━━━━━━━━━━━━━━━━━━

ticker =str(input('Digite o ticker da ação: '))     


#━━━━━━━━━━━━━━━━━━❮Função de Taxa de Retorno Simples❯━━━━━━━━━━━━━━━━━━


def calcular_retorno_simples_quantico(dados):
    # Isolando a parte 'Adj Close' dos dados e calculando retorno simples para cada ticker
    dados_trs = (dados['Adj Close'] / dados['Adj Close'].shift(1)) - 1
    
    num_qubits = int(np.ceil(np.log2(len(dados_trs.dropna().stack()))))  # Calculando baseado no total de dados disponíveis
    circuito = QuantumCircuit(num_qubits)
    
    # Achatando os dados para uma série única para processamento quântico
    flat_returns = dados_trs.dropna().stack()
    
    for i, retorno in enumerate(flat_returns):
        angle = np.pi * retorno
        circuito.ry(angle, i % num_qubits)  # Aplicar rotação em qubits com base no retorno

    # Adicionando um registro clássico e medidas ao circuito
    registro_classico = ClassicalRegister(num_qubits)
    circuito.add_register(registro_classico)
    circuito.measure(range(num_qubits), range(num_qubits))

    # Configurando o simulador e executando o circuito
    simulador = Aer.get_backend('qasm_simulator')
    circuito_transpilado = transpile(circuito, simulador)
    job = simulador.run(circuito_transpilado, shots=1)
    resultado = job.result()
    contagens = resultado.get_counts(circuito)

    # Retornando os dados de retorno simples e contagens da simulação
    return dados_trs, contagens


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❮◆❯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━






#━━━━━━━━━━━━━━━━━━❮Função de Taxa de Retorno Logaritmico❯━━━━━━━━━━━━━━━━━━

def calcular_retorno_logaritmico_quantico(dados):
    # Calculando o retorno logarítmico para cada ticker
    dados_trl = np.log(dados['Adj Close'] / dados['Adj Close'].shift(1))
    
    num_qubits = int(np.ceil(np.log2(len(dados_trl.dropna().stack()))))  # Calculando com base no total de dados disponíveis
    circuito = QuantumCircuit(num_qubits)
    
    # Achatando os dados para uma série única para processamento quântico
    flat_returns = dados_trl.dropna().stack()
    
    for i, retorno in enumerate(flat_returns):
        angle = np.pi * retorno
        circuito.ry(angle, i % num_qubits)  # Aplicar rotação em qubits com base no retorno

    # Adicionando um registro clássico e medidas ao circuito
    registro_classico = ClassicalRegister(num_qubits)
    circuito.add_register(registro_classico)
    circuito.measure(range(num_qubits), range(num_qubits))

    # Configurando o simulador e executando o circuito
    simulador = Aer.get_backend('qasm_simulator')
    circuito_transpilado = transpile(circuito, simulador)
    job = simulador.run(circuito_transpilado, shots=1)
    resultado = job.result()
    contagens = resultado.get_counts(circuito)

    return dados_trl, contagens


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❮◆❯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━






#━━━━━━━━━━━━━━━━━━❮Função de Plotagem❯━━━━━━━━━━━━━━━━━━


def normalizar_e_plotar(dados, tamanho_figura=(10, 10)):
    """
    Normaliza os dados para a base 100 e plota o gráfico de linha.

    Args:
    dados (DataFrame): DataFrame com preços de ações.
    tamanho_figura (tuple): Dimensões da figura para o plot.
    """
    # Normalizando os dados para 100 na base
    dados_normalizados = (dados / dados.iloc[0] * 100)
    plt.figure(figsize=tamanho_figura)
    plt.plot(dados_normalizados)
    plt.title('Preços Normalizados de Ações para Base 100')
    plt.xlabel('Data')
    plt.ylabel('Preço Normalizado')
    plt.legend(dados_normalizados.columns)
    plt.grid(True)
    plt.show()
    
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❮◆❯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━







#━━━━━━━━━━━━━━━━━━❮Função de Retorno de Portfolio❯━━━━━━━━━━━━━━━━━━


def calcular_retorno_portfolio_quantico(dados, pesos):
    """
    Calcula o retorno anualizado do portfólio com base nos pesos atribuídos às ações.

    Args:
    dados (DataFrame): DataFrame com preços de ações.
    pesos (np.array): Array de pesos atribuídos a cada ação no portfólio.

    Returns:
    float: Retorno anualizado do portfólio.
    """
    # Calculando o retorno diário para cada ação
    retorno_diario = (dados / dados.shift(1)) - 1

    # Calculando a média dos retornos diários e anualizando
    retorno_anualizado = retorno_diario.mean() * 250

    # Calculando o retorno do portfólio usando o produto escalar dos retornos anualizados e os pesos
    retorno_portfolio = np.dot(retorno_anualizado, pesos)

    return retorno_portfolio


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❮◆❯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
