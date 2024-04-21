#━━━━━━━━━━━━━━━━━━❮Bibliotecas❯━━━━━━━━━━━━━━━━━━

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import base64
#━━━━━━━━━━━━━━━━━━❮◆❯━━━━━━━━━━━━━━━━━━
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
from API.Taxas_de_Retorno import calcular_retorno_simples_quantico, calcular_retorno_logaritmico_quantico, normalizar_e_plotar, calcular_retorno_portfolio_quantico
from flask import Flask, request, jsonify

#━━━━━━━━━━━━━━━━━━❮◆❯━━━━━━━━━━━━━━━━━━


app = Flask(__name__)

def get_data(ticker):
    """Busca dados históricos de ações do Yahoo Finance."""
    data = yf.download(ticker, start="2020-01-01", end="2021-01-01")
    return data


#━━━━━━━━━━━━━━━━━━❮Rota de Taxa de Retorno Simples❯━━━━━━━━━━━━━━━━━━

@app.route('/predict/simple_return', methods=['GET'])
def predict_simple_return():
    ticker = request.args.get('ticker', default='AAPL')
    data = get_data(ticker)
    retorno_simples, contagens = calcular_retorno_simples_quantico(data)
    return jsonify({"retorno_simples": retorno_simples.to_json(), "contagens": contagens})
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❮◆❯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━





#━━━━━━━━━━━━━━━━━━❮Rota de Taxa de Retorno Logaritmico❯━━━━━━━━━━━━━━━━━━

@app.route('/predict/log_return', methods=['GET'])
def predict_log_return():
    ticker = request.args.get('ticker', default='AAPL')
    data = get_data(ticker)
    retorno_logaritmico, contagens = calcular_retorno_logaritmico_quantico(data)
    return jsonify({"retorno_logaritmico": retorno_logaritmico.to_json(), "contagens": contagens})

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❮◆❯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━





#━━━━━━━━━━━━━━━━━━❮Rota de Plotagem❯━━━━━━━━━━━━━━━━━━

@app.route('/predict/normalize_plot', methods=['GET'])
def normalize_plot():
    ticker = request.args.get('ticker', default='AAPL')
    data = get_data(ticker)
    fig, ax = plt.subplots(figsize=(10, 10))
    normalizar_e_plotar(data, ax=ax)
    # Salvar o gráfico em um buffer.
    pngOutput = BytesIO()
    FigureCanvas(fig).print_png(pngOutput)
    plt.close(fig)
    pngOutput.seek(0)
    pngBase64 = base64.b64encode(pngOutput.getvalue()).decode('ascii')
    return jsonify({"image": "data:image/png;base64," + pngBase64})

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❮◆❯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━




#━━━━━━━━━━━━━━━━━━❮Rota de Retorno de Portfolio❯━━━━━━━━━━━━━━━━━━

@app.route('/predict/portfolio_return', methods=['POST'])
def portfolio_return():
    data = request.get_json()
    ticker = data.get('ticker', 'AAPL')
    pesos = np.array(data.get('pesos', [0.5, 0.5]))
    stock_data = get_data(ticker)
    retorno_portfolio = calcular_retorno_portfolio_quantico(stock_data, pesos)
    return jsonify({"retorno_portfolio": retorno_portfolio})

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❮◆❯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━



if __name__ == '__main__':
    app.run(debug=True)
