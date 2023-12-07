import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, send_file
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

linear_reg_predictions_history = []
gradient_boost_predictions_history = []

data = pd.read_csv('data.csv')

features = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view',
            'condition', 'grade', 'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated',
            'zipcode', 'lat', 'long', 'sqft_living15', 'sqft_lot15']

labels = data['price']

conv_dates = [1 if values == 2014 else 0 for values in data.date]
data['date'] = conv_dates

train_data = data[features]

x_train, x_test, y_train, y_test = train_test_split(train_data, labels, test_size=0.10, random_state=2)

reg = LinearRegression()
reg.fit(x_train, y_train)

clf = GradientBoostingRegressor(n_estimators=400, max_depth=5, min_samples_split=2,
                                learning_rate=0.1, loss='squared_error')
clf.fit(x_train, y_train)

pca = PCA()
pca.fit_transform(scale(train_data))

@app.route('/predict', methods=['POST'])
def predict():
    data_input = request.get_json()

    input_features = [data_input.get(feature) for feature in features]

    input_df = pd.DataFrame([input_features], columns=features)

    linear_reg_prediction = reg.predict(input_df)[0]
    gradient_boost_prediction = clf.predict(input_df)[0]

    linear_reg_predictions_history.append(linear_reg_prediction)
    gradient_boost_predictions_history.append(gradient_boost_prediction)

    return jsonify({
        'linear_reg_prediction': linear_reg_prediction,
        'gradient_boost_prediction': gradient_boost_prediction
    })

@app.route('/history')
def history():
    plt.plot(linear_reg_predictions_history, label='Linear Regression')
    plt.plot(gradient_boost_predictions_history, label='Gradient Boosting')
    plt.xlabel('Prediction Number')
    plt.ylabel('Price Prediction')
    plt.title('Prediction History')
    plt.legend()

    image_data = io.BytesIO()
    plt.savefig(image_data, format='png')
    image_data.seek(0)
    
    plt.clf()
    plt.close()

    return send_file(image_data, mimetype='image/png', as_attachment=True, download_name='prediction_history.png')

if __name__ == '__main__':
    print("API is running and listening on http://127.0.0.1:5000/")
    app.run(debug=True)
