from flask import Flask, request, jsonify, send_file
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from joblib import dump, load
import os
import io
import mysql.connector
import base64


# MySQL connection details
db_config = {
    'user': 'smartsouk',
    'password': 'NACER123smartsouk***',
    'host': 'localhost',
    'database': 'smartsouk'
}

app = Flask(__name__)

# Path for the saved model
model_file = 'house_price_model.joblib'

# Load or train the model
if os.path.exists(model_file):
    model = load(model_file)
else:
    # Load your data - ensure 'data.csv' is the correct path
    df = pd.read_csv('data.csv')

    # Define categorical and numeric features
    categorical_features = ['Zone', 'typeOfProperty', 'condition']
    numeric_features = ['construction_price_in_m_sqr', 'bedrooms', 'bathrooms', 
                        'sqft_living', 'sqft_lot', 'floors', 'waterfront', 
                        'view', 'yr_built']

    # Create imputers and preprocessing pipeline
    numeric_imputer = SimpleImputer(strategy='mean')
    categorical_imputer = SimpleImputer(strategy='most_frequent')
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', Pipeline(steps=[('imputer', numeric_imputer), ('scaler', StandardScaler())]), numeric_features),
            ('cat', Pipeline(steps=[('imputer', categorical_imputer), ('encoder', OneHotEncoder(handle_unknown='ignore'))]), categorical_features)
        ]
    )

    # Define the model pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    # Train the model
    X = df.drop('price', axis=1)
    y = df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)

    # Save the model
    dump(model, model_file)

    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)

@app.route('/predict', methods=['POST'])
def predict_price():
    data = request.get_json()

    # Create new data frame from the request data
    new_df = pd.DataFrame({key: [value] for key, value in data.items()})

    # Predict the price
    predicted_price = model.predict(new_df)[0]

    # Generate the graph based on the new data
    graph = generate_graph(new_df, 10)

    # Save the graph as a PNG image to a BytesIO object
    img = io.BytesIO()
    graph.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)

    encoded_img = base64.b64encode(img.getvalue()).decode('utf-8')

    # Save predicted_price and encoded_img to MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    insert_query = "INSERT INTO predictions (predicted_price, graph_image) VALUES (%s, %s)"
    cursor.execute(insert_query, (predicted_price, encoded_img))
    conn.commit()
    prediction_id = cursor.lastrowid
    cursor.close()
    conn.close()


    response = jsonify({'predicted_price': predicted_price})
    response.headers.set('Content-Type', 'image/png')
    response.set_data(img.getvalue())
    
    return jsonify({
        'predicted_price': predicted_price,
        'prediction_id': prediction_id  # Use this ID to retrieve data from PHP
    })

def generate_graph(new_df, xyears):
    # Convert numeric columns to float if they are not already
    numeric_columns = ['construction_price_in_m_sqr', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view', 'yr_built']
    new_df[numeric_columns] = new_df[numeric_columns].astype(float)

    # Generate and return a list of predictions for 1 to xyears
    predicted_prices = []
    years = list(range(1, xyears + 1))  # Generate predictions for 1 to xyears

    # Possible annual increase rates including negative values
    annual_increase_rates = [-0.002, -0.001, 0, 0.001, 0.02, 0.03, 0.04]

    for future_year_adjustment in years:
        # Randomly select an annual increase rate for each year
        annual_increase_rate = random.choice(annual_increase_rates)

        adjusted_construction_price = new_df['construction_price_in_m_sqr'] * (1 + annual_increase_rate) ** future_year_adjustment
        adjusted_year_built = new_df['yr_built'] + future_year_adjustment

        new_data = {
            'Zone': new_df['Zone'],
            'typeOfProperty': new_df['typeOfProperty'],
            'condition': new_df['condition'],
            'construction_price_in_m_sqr': adjusted_construction_price,
            'bedrooms': new_df['bedrooms'],
            'bathrooms': new_df['bathrooms'],
            'sqft_living': new_df['sqft_living'],
            'sqft_lot': new_df['sqft_lot'],
            'floors': new_df['floors'],
            'waterfront': new_df['waterfront'],
            'view': new_df['view'],
            'yr_built': adjusted_year_built
        }

        # Convert to DataFrame
        new_df = pd.DataFrame(new_data)

        # Making prediction with the model
        predicted_price = model.predict(new_df)[0]
        predicted_prices.append(predicted_price)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(years, predicted_prices, marker='o')
    plt.title('Predicted House Prices Over the Next ' + str(xyears) + ' Years')
    plt.xlabel('Years into the Future')
    plt.ylabel('Predicted Price')
    plt.grid(True)
    return plt

if __name__ == '__main__':
    app.run(debug=True)
