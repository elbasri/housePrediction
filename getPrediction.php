<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</head>
<body>

<div class="container mt-5">
    <h2 class="mb-4">Real Estate Prediction Form</h2>

    <form action="getPrediction.php" method="post">
        <div class="form-group">
            <label for="Zone">Zone:</label>
            <input type="text" id="Zone" name="Zone" class="form-control" value="MA-GZ1" required>
        </div>

        <div class="form-group">
            <label for="typeOfProperty">Type of Property:</label>
            <input type="text" id="typeOfProperty" name="typeOfProperty" class="form-control" value="Villa" required>
        </div>

        <div class="form-group">
            <label for="condition">Condition:</label>
            <input type="text" id="condition" name="condition" class="form-control" value="recent" required>
        </div>

        <div class="form-group">
            <label for="construction_price_in_m_sqr">Construction Price (m^2):</label>
            <input type="text" id="construction_price_in_m_sqr" name="construction_price_in_m_sqr" class="form-control" value="3000" required>
        </div>

        <div class="form-group">
            <label for="bedrooms">Bedrooms:</label>
            <input type="text" id="bedrooms" name="bedrooms" class="form-control" value="2" required>
        </div>

        <div class="form-group">
            <label for="bathrooms">Bathrooms:</label>
            <input type="text" id="bathrooms" name="bathrooms" class="form-control" value="2" required>
        </div>

        <div class="form-group">
            <label for="sqft_living">Sqft Living:</label>
            <input type="text" id="sqft_living" name="sqft_living" class="form-control" value="780" required>
        </div>

        <div class="form-group">
            <label for="sqft_lot">Sqft Lot:</label>
            <input type="text" id="sqft_lot" name="sqft_lot" class="form-control" value="1542" required>
        </div>

        <div class="form-group">
            <label for="floors">Floors:</label>
            <input type="text" id="floors" name="floors" class="form-control" value="2" required>
        </div>

        <div class="form-group">
            <label for="waterfront">Waterfront (0 or 1):</label>
            <input type="text" id="waterfront" name="waterfront" class="form-control" value="0" required>
        </div>

        <div class="form-group">
            <label for="view">View:</label>
            <input type="text" id="view" name="view" class="form-control" value="1" required>
        </div>

        <div class="form-group">
            <label for="yr_built">Year Built:</label>
            <input type="text" id="yr_built" name="yr_built" class="form-control" value="1933" required>
        </div>


        <button type="submit" class="btn btn-primary mt-3">Submit</button>
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // Collect input data from the form
        $input_data = [
            'Zone' => $_POST['Zone'],
            'typeOfProperty' => $_POST['typeOfProperty'],
            'condition' => $_POST['condition'],
            'construction_price_in_m_sqr' => $_POST['construction_price_in_m_sqr'],
            'bedrooms' => $_POST['bedrooms'],
            'bathrooms' => $_POST['bathrooms'],
            'sqft_living' => $_POST['sqft_living'],
            'sqft_lot' => $_POST['sqft_lot'],
            'floors' => $_POST['floors'],
            'waterfront' => $_POST['waterfront'],
            'view' => $_POST['view'],
            'yr_built' => $_POST['yr_built']
        ];

        // Prepare the input data for the API call
        $json_data = json_encode($input_data);

        // Set up options for the API call
        $options_predict = [
            'http' => [
                'header' => 'Content-type: application/json',
                'method' => 'POST',
                'content' => $json_data,
            ],
        ];

        // Make the API call to get predictions
        $context_predict = stream_context_create($options_predict);
        $result_predict = file_get_contents('http://127.0.0.1:5000/predict', false, $context_predict);
        $data_predict = json_decode($result_predict, true);

        echo "<br>Predicted Price: ".round($data_predict["predicted_price"], 2)."<br>";
        echo "<img src='data:image/png;base64," . $data_predict["encoded_img"] . "' />";
        //var_dump($data_predict);
        //$prediction_id = $data_predict["prediction_id"];
        // MySQL connection details

/*
$host = "localhost";
$username = "stats_projet";
$password = "NCR123stats***";
$dbname = "pred";

$conn = new mysqli($host, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Retrieve data
$sql = "SELECT predicted_price, graph_image FROM predictions WHERE id = $prediction_id";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        echo "Predicted Price: " . $row["predicted_price"] . "<br>";
        
        // Display the graph image
        ";
    }
} else {
    echo "0 results";
}
*/
//$conn->close();
 
    }
    ?>

</div>

<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>

</body>
</html>
