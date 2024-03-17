from flask import Flask, request, jsonify



app = Flask(__name__)


@app.route('/predict', methods=['GET'])
def predict():
    # Obtém o ticker da query string
    ticker = request.args.get('ticker', default='PETR4.SA', type=str)
    
    # Aqui você integraria a lógica para buscar os dados da ação e fazer a previsão
    # Por enquanto, vamos apenas retornar o ticker recebido
    response = {
        "ticker": ticker,
        "message": "Previsão ainda não implementada."
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
