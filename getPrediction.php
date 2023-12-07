<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Real Estate Prediction Form</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</head>
<body>

<div class="container mt-5">
    <h2 class="mb-4">Real Estate Prediction Form</h2>

    <form action="getPrediction.php" method="post">
        <div class="form-group">
            <label for="bedrooms">Bedrooms:</label>
            <input type="text" id="bedrooms" name="bedrooms" value="3" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="bathrooms">Bathrooms:</label>
            <input type="text" id="bathrooms" name="bathrooms" value="2" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="sqft_living">Sqft Living:</label>
            <input type="text" id="sqft_living" name="sqft_living" value="1500" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="sqft_lot">Sqft Lot:</label>
            <input type="text" id="sqft_lot" name="sqft_lot" value="5000" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="floors">Floors:</label>
            <input type="text" id="floors" name="floors" value="2" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="waterfront">Waterfront (0 or 1):</label>
            <input type="text" id="waterfront" name="waterfront" value="0" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="view">View:</label>
            <input type="text" id="view" name="view" value="2" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="condition">Condition:</label>
            <input type="text" id="condition" name="condition" value="3" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="grade">Grade:</label>
            <input type="text" id="grade" name="grade" value="7" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="sqft_above">Sqft Above:</label>
            <input type="text" id="sqft_above" name="sqft_above" value="1200" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="sqft_basement">Sqft Basement:</label>
            <input type="text" id="sqft_basement" name="sqft_basement" value="300" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="yr_built">Year Built:</label>
            <input type="text" id="yr_built" name="yr_built" value="2000" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="yr_renovated">Year Renovated:</label>
            <input type="text" id="yr_renovated" name="yr_renovated" value="2015" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="zipcode">Zipcode:</label>
            <input type="text" id="zipcode" name="zipcode" value="98001" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="lat">Latitude:</label>
            <input type="text" id="lat" name="lat" value="47.5112" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="long">Longitude:</label>
            <input type="text" id="long" name="long" value="-122.257" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="sqft_living15">Sqft Living15:</label>
            <input type="text" id="sqft_living15" name="sqft_living15" value="1400" class="form-control" required>
        </div>

        <div class="form-group">
            <label for="sqft_lot15">Sqft Lot15:</label>
            <input type="text" id="sqft_lot15" name="sqft_lot15" value="4500" class="form-control" required>
        </div>

        <button type="submit" class="btn btn-primary mt-3">Submit</button>
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $input_data = [
            'bedrooms' => $_POST['bedrooms'],
            'bathrooms' => $_POST['bathrooms'],
            'sqft_living' => $_POST['sqft_living'],
            'sqft_lot' => $_POST['sqft_lot'],
            'floors' => $_POST['floors'],
            'waterfront' => $_POST['waterfront'],
            'view' => $_POST['view'],
            'condition' => $_POST['condition'],
            'grade' => $_POST['grade'],
            'sqft_above' => $_POST['sqft_above'],
            'sqft_basement' => $_POST['sqft_basement'],
            'yr_built' => $_POST['yr_built'],
            'yr_renovated' => $_POST['yr_renovated'],
            'zipcode' => $_POST['zipcode'],
            'lat' => $_POST['lat'],
            'long' => $_POST['long'],
            'sqft_living15' => $_POST['sqft_living15'],
            'sqft_lot15' => $_POST['sqft_lot15'],
        ];

        $json_data = json_encode($input_data);

        $options_predict = [
            'http' => [
                'header' => 'Content-type: application/json',
                'method' => 'POST',
                'content' => $json_data,
            ],
        ];

        $context_predict = stream_context_create($options_predict);
        $result_predict = file_get_contents('http://127.0.0.1:5000/predict', false, $context_predict);
        $data_predict = json_decode($result_predict, true);

        echo "<h3 class='mt-4'>Linear Regression Prediction: " . $data_predict['linear_reg_prediction'] . "</h3>";
        echo "<h3>Gradient Boosting Prediction: " . $data_predict['gradient_boost_prediction'] . "</h3>";

        $result_history_image = file_get_contents('http://127.0.0.1:5000/history');

        echo '<img src="data:image/png;base64,' . base64_encode($result_history_image) . '" alt="Prediction History" class="img-fluid mt-3">';
    }
    ?>

</div>

<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>

</body>
</html>
