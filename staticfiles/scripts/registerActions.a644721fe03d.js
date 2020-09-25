// Grab the employee uuid from the form sending the request
function getEmployeeUUID() {
	return document.getElementById("employeeUUID").value;
}


// Grab the employee id from the form sending the request
function getEmployeeID() {
	return document.getElementById("employeeID").value;
}


// Grab the employee password from the form sending the request
function getEmployeePassword() {
	return document.getElementById("employeePassword").value;
}


// Sign into an existing account
function registerSignIn() {
	/* Set up the request by specifying the correct API endpoint,
	grabbing the unique csrf token and collecting the data we
	would like to send to the API */
	const productActionURL = ('/signIn/');
	const securityToken = getCSRFToken('csrftoken');
	const productData = {employeeID: getEmployeeID(), employeePassword: getEmployeePassword()};

	// As per the comment in apiRequest.js, we need to use the POST verb to create a new database record
	ajaxPost(productActionURL, productData, securityToken, (callbackResponse) => {

	// Use the status code stored in our callbackResponse to see if the request was successful
	if (isSuccessResponse(callbackResponse)) {

		// Redirect to the main page after a successful sign in
		window.location.href='/registerMenu'
	}

	// Use the status code stored in our callbackResponse to see if the request failed
	if (isErrorResponse(callbackResponse)){
		displayMessage(callbackResponse.errorMessage, 'failed');
		document.getElementById('employeeID').value = '';
		document.getElementById('employeePassword').value = ''
	}
});

}


// Remove an employee record from the database
function deleteEmployee() {
	//Set up the request by specifying the correct API endpoint,
	const productActionURL = ('/api/employees/' + (getEmployeeUUID()) + '/');

	// As per the comment in apiRequest.js, we need to use the DELETE verb to remove an item from the database
	ajaxDelete(productActionURL, (callbackResponse) => {

	// Use the status code stored in our callbackResponse to see if the request was successful
	if (isSuccessResponse(callbackResponse)) {
		displayMessage('The employee was successfully deleted.', 'success');
	}

	// Use the status code stored in our callbackResponse to see if the request failed
	if (isErrorResponse(callbackResponse)){
		displayMessage('The request to delete an employee was denied.', 'fail');
	}
});

}

// Display a message on the page that made the request
function displayMessage(text, type) {
	// A successful message will give the statusBox a green background and show the hidden element
	if (type == 'success') {
		document.getElementById('statusBox').style.background = '#4CAF50';
		document.getElementById('statusBox').style.display = 'block';
		document.getElementById('status').innerHTML = text;
		setTimeout(function(){ document.getElementById('statusBox').style.display = 'none'; }, 5000);

	}


	// A failed message will give the statusBox a red background and show the hidden element
	if (type == 'failed') {
		document.getElementById('statusBox').style.background = '#f44336';
		document.getElementById('statusBox').style.display = 'block';
		document.getElementById('status').innerHTML = text;
		setTimeout(function(){ document.getElementById('statusBox').style.display = 'none'; }, 5000);
	}
}


// Grab a CSRF token from a cookie
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