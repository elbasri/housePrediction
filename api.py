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

app = Flask(__name__)

# مسار الملف النموذجي المحفوظ
# Path for the saved model
model_file = 'house_price_model.joblib'

# تحميل النموذج أو تدريبه
# Load or train the model
if os.path.exists(model_file):
    model = load(model_file)
else:
    # تحميل البيانات - تأكد من أن 'data.csv' هو المسار الصحيح
    # Load your data - ensure 'data.csv' is the correct path
    df = pd.read_csv('data.csv')

    # تحديد الميزات الفئوية والعددية
    # Define categorical and numeric features
    categorical_features = ['Zone', 'typeOfProperty', 'condition']
    numeric_features = ['construction_price_in_m_sqr', 'bedrooms', 'bathrooms', 
                        'sqft_living', 'sqft_lot', 'floors', 'waterfront', 
                        'view', 'yr_built']

    # إنشاء المُدخلات وسلسلة معالجة ما قبل النمذجة
    # Create imputers and preprocessing pipeline
    numeric_imputer = SimpleImputer(strategy='mean')
    categorical_imputer = SimpleImputer(strategy='most_frequent')
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', Pipeline(steps=[('imputer', numeric_imputer), ('scaler', StandardScaler())]), numeric_features),
            ('cat', Pipeline(steps=[('imputer', categorical_imputer), ('encoder', OneHotEncoder(handle_unknown='ignore'))]), categorical_features)
        ]
    )

    # تعريف سلسلة النموذج
    # Define the model pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    # تدريب النموذج
    # Train the model
    X = df.drop('price', axis=1)
    y = df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)

    # حفظ النموذج
    # Save the model
    dump(model, model_file)

    # تقييم النموذج
    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)

@app.route('/predict', methods=['POST'])
def predict_price():
    data = request.get_json()

    # إنشاء إطار بيانات جديد من بيانات الطلب
    # Create new data frame from the request data
    new_df = pd.DataFrame({key: [value] for key, value in data.items()})

    # التنبؤ بالسعر
    # Predict the price
    predicted_price = model.predict(new_df)[0]

    # توليد الرسم البياني استنادًا إلى البيانات الجديدة
    # Generate the graph based on the new data
    graph = generate_graph(new_df, 10)

    # حفظ الرسم البياني كصورة PNG في كائن BytesIO
    # Save the graph as a PNG image to a BytesIO object
    img = io.BytesIO()
    graph.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)

    encoded_img = base64.b64encode(img.getvalue()).decode('utf-8')

    
    
    # بعد إضافة ملف makePrediction.php 
    # لم نعد بحاجة لتخزين البيانات هنا، حيث يقوم الملف أعلاه بتخزينها بعد استرجاعها من هنا.. وهذا هو ما سيحدث في بيئة عمل فعلية
    # لكن، لازال بإمكانك عمل تخزين لها في قاعدة مايسكيول بإلغاء تعليق الجزء التالي من الرمز البرمجي
    #conn = mysql.connector.connect(**db_config)
    #cursor = conn.cursor()
    #insert_query = "INSERT INTO predictions (predicted_price, graph_image) VALUES (%s, %s)"
    #cursor.execute(insert_query, (predicted_price, encoded_img))
    #conn.commit()
    #prediction_id = cursor.lastrowid
    #cursor.close()
    #conn.close()

    response = jsonify({'predicted_price': predicted_price})
    response.headers.set('Content-Type', 'image/png')
    response.set_data(img.getvalue())
    
    return jsonify({
        'predicted_price': predicted_price,
        'encoded_img': encoded_img
    })

def generate_graph(new_df, xyears):
    # تحويل الأعمدة العددية إلى float إذا لم تكن كذلك بالفعل
    # Convert numeric columns to float if they are not already
    numeric_columns = ['construction_price_in_m_sqr', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view', 'yr_built']
    new_df[numeric_columns] = new_df[numeric_columns].astype(float)

    # توليد وإرجاع قائمة التنبؤات لمدة 1 إلى xyears
    # Generate and return a list of predictions for 1 to xyears
    predicted_prices = []
    years = list(range(1, xyears + 1))  # Generate predictions for 1 to xyears

    # معدلات الزيادة السنوية المحتملة بما في ذلك القيم السالبة
    # Possible annual increase rates including negative values
    annual_increase_rates = [-0.002, -0.001, 0, 0.001, 0.02, 0.03, 0.04]

    for future_year_adjustment in years:
        # اختيار معدل زيادة سنوي عشوائي لكل عام
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

        # تحويل إلى إطار بيانات
        # Convert to DataFrame
        new_df = pd.DataFrame(new_data)

        # التنبؤ باستخدام النموذج
        # Making prediction with the model
        predicted_price = model.predict(new_df)[0]
        predicted_prices.append(predicted_price)


    # رسم النتائج
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
