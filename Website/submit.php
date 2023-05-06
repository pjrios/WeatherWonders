<?php
include 'config.php';
// Connect to the database
$conn = mysqli_connect('localhost', 'root', $password, 'STOPICS');

// Check if the form is submitted
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Get the form data
    $device_id = mysqli_real_escape_string($conn, $_POST['device_id']);
    $name = mysqli_real_escape_string($conn, $_POST['name']);
    $email = mysqli_real_escape_string($conn, $_POST['email']);
	$lon = mysqli_real_escape_string($conn, $_POST['longitude']);
    $lat = mysqli_real_escape_string($conn, $_POST['latitude']);
	
	$command = 'test.exe ' . escapeshellarg($lon) . ' ' . escapeshellarg($lat);
	$output = array();
	$return_value = 0;
	exec($command, $output, $return_value);
	
	$integer_value = mysqli_real_escape_string($conn,intval($output[0]));
	// Output the result
	if ($return_value == 0) {
		echo $integer_value;
	} else {
		echo "An error occurred while running the program.";
	}
    //Insert the data into the database
	$query = "INSERT INTO USERDATA (DEVICEID, NAME, EMAIL, GEOID)
			  VALUES ('$device_id', '$name', '$email', '$integer_value')";

    mysqli_query($conn, $query);

    // Redirect to a success page
    header('Location: success.html');
    exit;
}
?>

