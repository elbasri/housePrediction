# API توقع أسعار العقارات

## نظرة عامة

يعمل هذا الـ API باعتباره نظام توقع لأسعار العقارات. يتيح للمستخدمين إجراء توقعات لأسعار العقارات بناءً على البيانات المدخلة ويقوم بتصوير الأسعار المتوقعة على مدى السنوات القادمة.

## الميزات

- **توقع أسعار العقارات:** باستخدام بيانات الإدخال، يتوقع الـ API سعر العقار.
- **إنشاء رسوم بيانية للتوقعات:** يقوم الـ API بإنشاء رسوم بيانية تظهر الأسعار المتوقعة للعقارات على مدى السنوات القادمة.
- **تخزين التوقعات:** يمكن تخزين التوقعات والرسوم البيانية المرتبطة في قاعدة بيانات MySQL.

## المتطلبات الأولية

- Python (3.6 فما فوق)
- Pip (أداة تثبيت حزم Python)
- قاعدة بيانات MySQL

## التثبيت

1. **استنسخ النموذج:**

   ```bash
   git clone https://github.com/your-username/house-price-prediction.git

    ثبّت التبعيات:

    bash

cd house-price-prediction
pip install -r requirements.txt

أنشئ قاعدة بيانات MySQL بالاسم smartsouk مع الجداول المناسبة. يمكنك استخدام سيناريو SQL المقدم (database_setup.sql) لإعداد الهيكل البياني الضروري.

تأكد من تكوين تفاصيل اتصال قاعدة البيانات MySQL بشكل صحيح في المتغير db_config داخل ملف api.py

شغّل الـ Flask API:

bash

    python api.py

سيكون الـ API متاحًا على http://localhost:5000.
نقاط نهاية الـ API
POST /predict

    الإدخال: بيانات JSON تحتوي على تفاصيل المنزل.

    json

{
  "Zone": "MA-GZ1",
  "typeOfProperty": "apartment",
  "condition": "new",
  "construction_price_in_m_sqr": 8600000,
  "bedrooms": 2,
  "bathrooms": 2,
  "sqft_living": 86,
  "sqft_lot": 90,
  "floors": 1,
  "waterfront": 1,
  "view": 1,
  "yr_built": 2020
}

الإخراج: رد JSON مع سعر التوقع وصورة مشفرة للرسم التوضيحي.

json

    {
      "predicted_price": 1300000,
      "encoded_img": "base64_encoded_image_data"
    }

المساهمة

للمساهمة في المشروع، اتبع الخطوات التالية:

    قم بفورك النموذج.

    أنشئ فرعًا جديدًا لميزةك أو إصلاح الخطأ:

    bash

git checkout -b feature-name

قم بإجراء التغييرات الخاصة بك وقم بالاختبار بشكل جيد.

قم بعمل commit لتغييراتك:

bash

git commit -m "وصف لتغييراتك"

قم برفع التغييرات إلى فورك الخاص بك:

bash

    git push origin feature-name

    افتح طلب سحب إلى المستودع الرئيسي.

الترخيص

يتم ترخيص هذا المشروع بموجب رخصة MIT.



House Price Prediction API
Overview

This Flask API serves as a house price prediction system. It allows users to make predictions for house prices based on input data and visualizes the predicted prices over the next several years.
Features

    Predict House Prices: Given input data, the API predicts the price of a house.
    Generate Prediction Graphs: The API generates graphs showing predicted house prices over the next several years.
    Store Predictions: Predictions and associated graphs can be stored in a MySQL database.

Prerequisites

    Python (>=3.6)
    Pip (Python package installer)
    MySQL Database

Installation

    Clone the repository:

    bash

git clone https://github.com/your-username/house-price-prediction.git

Install dependencies:

bash

cd house-price-prediction
pip install -r requirements.txt

Create a MySQL database named smartsouk with the appropriate tables. You can use the provided SQL script (database_setup.sql) to set up the required schema.

Ensure your MySQL database connection details are correctly configured in the db_config variable within api.py.

Run the Flask API:

bash

    python api.py

The API will be accessible at http://localhost:5000.
API Endpoints
POST /predict

    Input: JSON payload containing house details.

    json

{
  "Zone": "MA-GZ1",
  "typeOfProperty": "apartment",
  "condition": "new",
  "construction_price_in_m_sqr": 8600000,
  "bedrooms": 2,
  "bathrooms": 2,
  "sqft_living": 86,
  "sqft_lot": 90,
  "floors": 1,
  "waterfront": 1,
  "view": 1,
  "yr_built": 2020
}

Output: JSON response with the predicted price and an encoded image of the prediction graph.

json

    {
      "predicted_price": 1300000,
      "encoded_img": "base64_encoded_image_data"
    }

Contributing

To contribute to the project, follow these steps:

    Fork the repository.

    Create a new branch for your feature or bug fix:

    bash

git checkout -b feature-name

Make your changes and test thoroughly.

Commit your changes:

bash

git commit -m "Description of your changes"

Push your changes to your fork:

bash

    git push origin feature-name

    Open a pull request to the main repository.

License

This project is licensed under the MIT License.
