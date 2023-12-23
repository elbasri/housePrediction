# استخدام خوارزميات تعلم الالة لتدريب نموذج توقع أسعار العقارات (يوفر واجهة برمجة تطبيقات)

## نظرة عامة

يعمل هذا المشروع باعتباره نموذج مصغر لنظام توقع لأسعار العقارات. يتيح للمستخدمين إجراء توقعات لأسعار العقارات بناءً على البيانات المدخلة ويقوم بتصوير الأسعار المتوقعة على مدى السنوات القادمة.
وطريقة عمله أنه قادر على إنشاء نماذج مُدربة.

## الميزات

- **توقع أسعار العقارات:** باستخدام بيانات الإدخال، ثم يتم ارسالها لواجهة برمجة التطبيقات للحصول على سعر العقار.
- **إنشاء رسوم بيانية للتوقعات:** يقوم بإنشاء رسوم بيانية تظهر الأسعار المتوقعة للعقارات على مدى السنوات القادمة.. يمكنك تحديد المدة التي تريد.
- **تخزين التوقعات:** يمكن تخزين التوقعات والرسوم البيانية المرتبطة في قاعدة بيانات مايسكيول.

## المتطلبات الأولية

- بايثون (3.6 فما فوق)
- بايب (أداة تثبيت حزم بايثون)
- قاعدة بيانات مايسكيول
- -لمن يريد استخدام نموذج ارسال البيانات التجريبي هنا سيحتاج تثبيت وإعداد وتشغيل "بي إتش بي"

  
## مثال حي للنتيجة المنتظرة (بعد استخدام هذا النموذج في مشروع فعلي)

![مثال لتوقع ثمن منزل](https://www.alarabiya.ma/wp-content/uploads/2023/12/Screenshot-2023-12-23-at-02-11-40-Beautiful-villa.png)
## التثبيت

1. **استنسخ النموذج:**
 
اإما عبر برنامج جيتهوب لسطح المكتب، أو باستخدام الأمر التالي:

    git clone https://github.com/elbasri/housePrediction.git

   
أنشئ قاعدة بيانات ماسكيول بالاسم smartsouk مع الجداول المناسبة.

تأكد من تكوين تفاصيل اتصال قاعدة البيانات مايسكيول بشكل صحيح داخل ملف api.py

شغّل البرنامج (واجهة برمجة التطبيقات):


    python api.py

سيكون الان متاحًا على



    http://localhost:5000
    
### نقطة الإتصال:

POST /predict

    الإدخال: بيانات تحتوي على تفاصيل المنزل.. مثال:

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

الإخراج: رد مع سعر التوقع وصورة مشفرة للرسم التوضيحي.


    {
      "predicted_price": 1300000,
      "encoded_img": "base64_encoded_image_data"
    }

المساهمة

للمساهمة في المشروع، اتبع الخطوات التالية:

 قم بنسخ المشروع

 أنشئ فرعًا جديدًا لميزة أو إصلاح خطأ ما:



    git checkout -b feature-name

قم بإجراء التغييرات الخاصة بك وقم بالاختبار بشكل جيد.

قم بعمل رفع لتغييراتك:



    git commit -m "وصف لتغييراتك"

قم برفع التغييرات إلى النسخة الخاصة بك:


    git push origin feature-name

 افتح طلب سحب إلى المشروع الرئيسي.

الترخيص

يتم ترخيص هذا المشروع بموجب رخصة MIT.

للتواصل:
https://twitter.com/abdennacerelb



