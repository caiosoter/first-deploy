from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os


colunas = ["tamanho", "ano", "garagem"]
linear_model = pickle.load(open('.\.\models\modelo.sav', 'rb'))

app = Flask(__name__) # O __name__ faz com que o flask identifique aonde a API está rodando, e ajuda ele encontrar os recursos para rodar a API.
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return "Minha primeira API"

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(from_lang='pt', to="en")
    polaridade = tb_en.sentiment.polarity
    return "polaridade é: {}".format(polaridade)

@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json() # Recebe dados json do usuário.
    dados_input = [dados[col] for col in colunas] # Mantem a ordem dos dados.
    y_pred = linear_model.predict([dados_input])
    return jsonify(preco=y_pred[0]) # Retorna um json do resultado

app.run(debug=True, host="0.0.0.0") # host 0.0.0.0, vai fazer com que nossa aplicação reconheça as chamadas mesmo dentro da docker ou no

# O debug igual a True faz com que o flask identificar automaticamente que fizemos modificação na API e vai dar restart.