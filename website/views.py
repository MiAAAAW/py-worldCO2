# Usado para renderizar el front-end o las plantillas HTML para la página web
from flask import Blueprint, render_template, request, json, redirect, url_for, flash
from website.calculations import stats
from website.calculations import ai
import os
import pandas
import sys

views = Blueprint('views', __name__, template_folder='templates')

# Cálculos y estadísticas para cada país
country_data = stats('data.csv')

# Renderizando la página de inicio
@views.route('/')
def home():
    return render_template("home.html")

# Renderizando el mapa interactivo
@views.route('/map')
def map():
    return render_template('map.html')

# Renderizando las plantillas de salida de estadísticas de datos
@views.route('/click_information', methods = ['POST'])
def click_information():
    country_name = request.json['country']
    if country_name not in country_data.CO2:
        return 'No data found'
    rtn = country_data.calc(country_name)
    return json.dumps(rtn)

# Definiendo la acción de hover en el mapa
@views.route('/hover_information', methods = ['POST'])
def hover_information():
    country_name = request.json['country']
    if country_name not in country_data.CO2:
        rtn = {
            'CO2': 'No data' 
        }
    else:rtn = {
            'CO2' : country_data.CO2[country_name],
            'Ranking' : str(country_data.rank[country_name])
        }
    return json.dumps(rtn)

@views.route('/detailed_information')
def detailed_information():
    return render_template('information.html')

# Renderizando la página HTML de IA
@views.route('/ai', methods=['GET', 'POST'])
def ai_render():
    if request.method == 'POST':
        years_to_predict = int(round(float(request.form.get('numericValue', 0))))
        if years_to_predict < 2025:
            flash('¡Por favor ingresa un año mayor a 2025!', category="error")
            return redirect(url_for('views.ai_render'))

        ml = ai('co2_trend.csv')
        img1 = ml.train()
        img2 = ml.predict(years_to_predict)
        return render_template('ai.html', img1=img1, img2=img2)

    elif request.method == 'GET':
        ml = ai('co2_trend.csv')
        img1 = ml.train()
        img2 = ml.predict(2050)
        return render_template('ai.html', img1=img1, img2=img2)
