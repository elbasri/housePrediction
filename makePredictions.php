<?php
// تفاصيل اتصال قاعدة البيانات MySQL
// MySQL connection details
$host = "localhost";
$username = "smartsouk";
$password = "NACER123smartsouk***";
$dbname = "smartsouk";

$conn = new mysqli($host, $username, $password, $dbname);

// التحقق من الاتصال
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// استرجاع البيانات من manage_properties
// Retrieve data from manage_properties
$sql = "SELECT * FROM manage_properties";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        // تجهيز بيانات الإدخال لاستدعاء API
        // Prepare the input data for the API call
        $input_data = [
            'Zone' => $row['Zone'],
            'typeOfProperty' => $row['typeOfProperty'],
            'condition' => $row['condition'],
            'construction_price_in_m_sqr' => $row['construction_price_in_m_sqr'],
            'bedrooms' => $row['bedrooms'],
            'bathrooms' => $row['bathrooms'],
            'sqft_living' => $row['sqft_living'],
            'sqft_lot' => $row['sqft_lot'],
            'floors' => $row['floors'],
            'waterfront' => $row['waterfront'],
            'view' => $row['view'],
            'yr_built' => $row['yr_built'],
        ];

        // تضمين معرف العقار في بيانات الإدخال
        //$input_data['property_id'] = $row['id'];

        // تجهيز بيانات الإدخال لاستدعاء API
        $json_data = json_encode($input_data);

        // ضبط الخيارات لاستدعاء API
        // Set up options for the API call
        $options_predict = [
            'http' => [
                'header' => 'Content-type: application/json',
                'method' => 'POST',
                'content' => $json_data,
            ],
        ];

        // القيام باستدعاء API للحصول على التنبؤات
        // Make the API call to get predictions
        $context_predict = stream_context_create($options_predict);
        $result_predict = file_get_contents('http://127.0.0.1:5000/predict', false, $context_predict);
        $data_predict = json_decode($result_predict, true);

        // تحديث manage_properties بالسعر المتوقع والصورة المشفرة
        //$prediction_id = $data_predict["prediction_id"];
        $update_sql = "UPDATE manage_properties SET predicted_price = {$data_predict['predicted_price']}, graph_image = '{$data_predict['encoded_img']}' WHERE id = {$row['id']}";
        $conn->query($update_sql);
    }
} else {
    echo "0 نتائج";
    // echo "0 results";
}

$conn->close();
?>
