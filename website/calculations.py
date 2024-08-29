import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

class stats():
    # Obteniendo conjuntos de datos
    def __init__(self, filename):
        self.data = pd.read_csv(os.path.join('website', 'data', filename))
        self.CO2 = {}
        self.rank = {}
        for j in range(len(self.data)):
            self.CO2[self.data['name'][j]] = self.data[' metric tonnes of CO2'][j]
            self.rank[self.data['name'][j]] = self.data['ranking'][j]

    # Calculando estadísticas
    def calc(self, country):
        calcs = {}
        CO2 = self.CO2[country].replace(',', '')
        # Equivalente en emisiones de carbono a
        calcs['calgasoline_gallons'] = int(CO2) * 113.0
        calcs['passenger_miles'] = int(CO2) * 2564.0
        calcs['smartphones_charged'] = int(CO2) * 121643.0

        # Cantidad necesaria para secuestrar emisiones de carbono
        calcs['USforest_acres'] = int(CO2) * 1.2

        # Contrarrestando las emisiones
        calcs['trashbags_recycled'] = int(CO2) * 43.3
        calcs['windturbines_running'] = int(CO2) * 0.0003

        return calcs


class ai():
    # Definiendo el modelo y los datos
    def __init__(self, filename):
        self.data = pd.read_csv(os.path.join('website', 'data', filename))

        self.X = (self.data['year'].values).reshape(-1, 1)
        self.y = (self.data['trend'].values).reshape(-1, 1)
        self.model = LinearRegression()
    
    # Convierte la figura a png para enviar a html
    def fig_to_png(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode('utf-8')

    def train(self):
        # Divide los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

        # Entrena el modelo de regresión lineal
        self.model.fit(X_train, y_train)

        # Realiza predicciones
        y_pred_test = self.model.predict(X_test)

        # Visualiza los resultados
        fig, ax = plt.subplots(figsize=(5, 4), dpi=200)  # Ajusta el tamaño de la figura según sea necesario
        ax.scatter(X_test, y_test, color='blue', label='Emisiones de CO2 reales por año')  # Etiqueta para puntos de datos reales
        ax.plot(X_test, y_pred_test, color='red', label='Predicción de emisiones de CO2 a lo largo del tiempo')  # Etiqueta para la línea de tendencia predicha
        ax.set_title('Predicción de tendencias históricas de CO2')
        ax.set_xlabel('Año')
        ax.set_ylabel('Emisiones de CO2')

        # Estableciendo límites apropiados en los ejes
        ax.set_xlim(min(self.X), max(self.X))
        ax.set_ylim(min(self.y), max(self.y))

        # Rotando etiquetas del eje x para mejorar la legibilidad si es necesario
        plt.xticks(rotation=45)
        ax.legend()

        plt.tight_layout()
        img_data = self.fig_to_png(fig)
        plt.close(fig)

        # Devuelve la imagen como png representada en un valor base64
        return img_data


    def predict(self, year):
        # Rango de tiempo para predicciones futuras
        future_years = np.arange(2025, year)
        future_years = future_years.reshape(-1,1)
            
        # Ajusta un modelo de regresión lineal
        self.model.fit(self.X, self.y)

        # Realiza predicciones para años futuros
        future_predictions = self.model.predict(future_years)

        # Grafica las predicciones futuras
        fig, ax = plt.subplots(figsize=(5, 4), dpi=200)
        ax.plot(self.X, self.y, color='blue', label='Emisiones históricas de CO2')
        ax.scatter(future_years, future_predictions, color='red', label='Predicción de emisiones de CO2 por año')
        ax.set_title('Predicciones futuras de emisiones de CO2')
        ax.set_xlabel('Año')
        ax.set_ylabel('Emisiones de CO2')
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        img_data = self.fig_to_png(fig)
        plt.close(fig)

        # Devuelve la imagen como png representada en un valor base64
        return img_data
