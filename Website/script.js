function validateForm(event) {
  const address = document.getElementById("address").value;
  const submitButton = document.getElementById("submit-btn"); 
  const url = `https://nominatim.openstreetmap.org/search?q=${address}&format=json&addressdetails=1&limit=1`;
  fetch(url)
    .then(response => response.json())
    .then(data => {
      if (data.length === 0) {
		document.getElementById("address").setCustomValidity("Invalid address"); // Set custom validation message
        document.getElementById("address").reportValidity(); // Trigger validation error

        // Clear the address input field
        document.getElementById("address").value = "";
        document.getElementById("coordinates").innerHTML = "Invalid address";
        submitButton.disabled = true; // Disable submit button
      } else {
        let result = "";
        for (const key in data[0]) {
          result += `${key}: ${data[0][key]}<br>`;
        }
        const latitude = data[0].lat;
        const longitude = data[0].lon;
		document.getElementById("latitude").value = latitude;
		document.getElementById("longitude").value = longitude;
        //document.getElementById("coordinates").innerHTML = result;
        submitButton.disabled = false; // Enable submit button
		document.getElementById("coordinates").innerHTML = "";
        // Form submission continues as normal
      }
    })
    .catch(error => console.log(error));
}

function showCoordinates() {
  validateForm(event);
}

