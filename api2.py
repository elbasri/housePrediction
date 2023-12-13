import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, send_file
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
import matplotlib   #Salam aleikom

matplotlib.use("Agg")  # Use Agg backend
import matplotlib.pyplot as plt
import io
import joblib
from sklearn.impute import SimpleImputer

app = Flask(__name__)

linear_reg_predictions_history = []
gradient_boost_predictions_history = []

model_filename = 'house_price_model.joblib'
reg = None  # Initialize reg and clf to None
clf = None

# Load the trained model if it exists
try:
    reg = joblib.load(model_filename)
    # Load the Gradient Boosting model
    clf = joblib.load('gradient_boost_model.joblib')
except FileNotFoundError:
    # If the model doesn't exist, train a new one
    print("doesnt exist")
    data = pd.read_csv('data.csv')
    imputer = SimpleImputer(strategy='mean')
    data = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)

    # Assuming features is a list of relevant columns for prediction
    features = ['Zone', 'typeOfProperty', 'condition', 'price', 'construction_price_in_m_sqr', 'bedrooms', 'bathrooms',
                'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view', 'yr_built', 'yr_renovated', 'zipcode', 'lat',
                'long']

    labels = data['price']

    train_data = data[features]

    x_train, x_test, y_train, y_test = train_test_split(train_data, labels, test_size=0.10, random_state=2)

    reg = LinearRegression()
    reg.fit(x_train, y_train)

    clf = GradientBoostingRegressor(n_estimators=400, max_depth=5, min_samples_split=2,
                                    learning_rate=0.1, loss='squared_error')
    clf.fit(x_train, y_train)

    pca = PCA()
    pca.fit_transform(scale(train_data))

    # Save the trained models
    joblib.dump(reg, model_filename)
    joblib.dump(clf, 'gradient_boost_model.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    features = ['Zone', 'typeOfProperty', 'condition', 'price', 'construction_price_in_m_sqr', 'bedrooms', 'bathrooms',
                'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view', 'yr_built', 'yr_renovated', 'zipcode', 'lat', 'long']

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


@app.route('/future', methods=['POST'])
def future():
    data_input = request.get_json()
    features = ['Zone', 'typeOfProperty', 'condition', 'price', 'construction_price_in_m_sqr', 'bedrooms', 'bathrooms',
                'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view', 'yr_built', 'yr_renovated', 'zipcode', 'lat', 'long']
    
    input_features = [data_input.get(feature) for feature in features]

    input_df = pd.DataFrame([input_features], columns=features)

    future_predictions = []
    for _ in range(10):  # Assuming 10 predictions for the next 5 years (every 6 months)
        print("Input Data for Prediction:")
        print(input_df)
        future_price = reg.predict(input_df)[0]

        # Update input data for the next prediction
        # You might need to adjust this part based on your actual use case
        # For example, you could increase the year or change other features
        input_df.at[0, 'yr_built'] = int(input_df.at[0, 'yr_built']) + 1        
        future_predictions.append(future_price)
        # Assuming your input data is dynamic, update it for the next prediction
        # You might need to adjust this part based on your actual use case

    # Generate a graph
    plt.plot(future_predictions, label='Future Predictions')
    plt.xlabel('Prediction Number')
    plt.ylabel('Price Prediction')
    plt.title('Future Predictions')
    plt.legend()

    image_data = io.BytesIO()
    plt.savefig(image_data, format='png')
    image_data.seek(0)

    plt.clf()
    plt.close()

    return send_file(image_data, mimetype='image/png', as_attachment=True, download_name='future_predictions.png')


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
