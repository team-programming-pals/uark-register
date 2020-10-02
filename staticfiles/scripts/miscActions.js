function displayMessage(text, type) {

	// Create a div element and assign it to the alert class from the CSS file
	alertDiv = document.createElement('div');
	alertDiv.classList.add('alert');

	// Specify the type of alertbox that should be displayed
	if (type == 'success')
		alertDiv.classList.add('success');
	if (type == 'warning')
		alertDiv.classList.add('warning');
	if (type == 'info')
		alertDiv.classList.add('info');
	

	// Create a span element that will display the "X" to close the alert
	alertSpan = document.createElement('span');
	alertSpan.classList.add('closebtn');
	alertSpan.innerHTML = '&times;';
	alertSpan.onclick = function () {
		// Hide the alertbox when the "X" is clicked
		alertDiv.style.display = 'none';
	};

	// Create a strong element to be used as a title
	alertTitle = document.createElement('strong');
	alertTitle.innerHTML = 'Uark Register Response: ';

	// Create an additional span to hold the body of our text
	alertMessage = document.createElement('span');
	alertMessage.innerHTML = text;

	// Assemble the elements together to a nice alertbox
	alertDiv.appendChild(alertSpan);
	alertDiv.appendChild(alertTitle);
	alertDiv.appendChild(alertMessage);

	// Display the alertbox
	document.getElementById('alert').appendChild(alertDiv);
	document.getElementById('alert').style = 'block';
}

function getCSRFToken(name) {
	/* Django has cross site request forgery protection, so we have to
	send a unique token along with certain requests or the web server
	will flat-out reject the request.

	When a form is submitted our template will store this special token
	in a cookie named "csrftoken". The getCSRFToken function will get
	the token from the cookie so it can be sent along with any request
	that needs a CSRF token to work.*/

	let tokenValue = null;

	// If the cookie exists, grab the data inside of it
	if (document.cookie && document.cookie !== '') {
		const tokens = document.cookie.split(';');
		// Cycle through the token's characters
		for (let i = 0; i < tokens.length; i++) {
			// Remove whitespace
			const token = tokens[i].trim();
			// Verify that this is a valid CSRF token generated by Django
			if (token.substring(0, name.length + 1) === (name + '=')) {
				// Decode the token and store it in tokenValue
				tokenValue = decodeURIComponent(token.substring(name.length + 1));
				break;
			}
		}
	}

	return tokenValue;
}