// Grab the employee uuid from the form sending the request
function getEmployeeUUID() {
	return document.getElementById("employeeUUID").value;
}


// Grab the employee id from the form sending the request
function getEmployeeID() {
	return document.getElementById("employeeID").value;
}

// Grab the employee password from the form sending the request
function getEmployeeFirstName() {
	return document.getElementById("employeeFirstName").value;
}

// Grab the employee password from the form sending the request
function getEmployeeLastName() {
	return document.getElementById("employeeLastName").value;
}

// Grab the employee password from the form sending the request
function getEmployeePassword() {
	return document.getElementById("employeePassword").value;
}

// Grab the employee password from the form sending the request
function getEmployeePasswordConfirm() {
	return document.getElementById("employeePasswordConfirm").value;
}


// Grab the employee password from the form sending the request
function getEmployeeClassification() {
	return document.getElementById("employeeClassification").value;
}

// Add a new product to the database
function UpdateEmployee() {
	/* Set up the request by specifying the correct API endpoint,
	grabbing the unique csrf token and collecting the data we
	would like to send to the API */
	const productActionURL = ('/employees/create/' + getEmployeeUUID() + '/');
	const securityToken = getCSRFToken('csrftoken');
	const productData = {employeeID: getEmployeeID(), employeeFirstName: getEmployeeFirstName(), employeeLastName: getEmployeeLastName(), employeePassword: getEmployeePassword(), employeeClassification: getEmployeeClassification()};

	// As per the comment in apiRequest.js, we need to use the POST verb to create a new database record
	ajaxPut(productActionURL, productData, securityToken, (callbackResponse) => {

	// Use the status code stored in our callbackResponse to see if the request was successful
	if (isSuccessResponse(callbackResponse)) {
		alert(callbackResponse.responseMessage);
		displayMessage(callbackResponse.responseMessage, 'success');
	}

	// Use the status code stored in our callbackResponse to see if the request failed
	if (isErrorResponse(callbackResponse)){
		//alert(callbackResponse.responseMessage);
		alert('lol');
		if (callbackResponse.responseMessage != undefined) {
			var message = JSON.parse(responseMessage)
			alert('test');
		}
		displayMessage('The request to add a product was denied.', 'failed');
	}
});

}

// Display a success or error notification within the status box of the calling view
function displayViewMessage(text, type) {
	// A successful message will give the statusBox a green background and show the hidden element
	if (type == 'successGeneral' || type == 'successCreate' || type == 'successUpdate' ||
		type == 'successDelete'  || type == 'success') {

		document.getElementById('statusBox').style.background = '#4CAF50';
		document.getElementById('statusBox').style.display = 'block';
		document.getElementById('status').innerHTML = text;
		setTimeout(function(){ document.getElementById('statusBox').style.display = 'none'; }, 5000);

	}


	// A failed message will give the statusBox a red background and show the hidden element
	if (type == 'errorGeneral' || type == 'errorFirstName' || type == 'errorLastName' || 
		type == 'errorPassword' || type == 'errorNotFound' || type == 'errorRedirect' ||
		type == 'errorSignIn' || type == 'errorEmployeeID' || type == 'errorEmployeeInt') {

		document.getElementById('statusBox').style.background = '#FFCCCC';
		document.getElementById('statusBox').style.display = 'block';
		document.getElementById('status').innerHTML = text;
		setTimeout(function(){ document.getElementById('statusBox').style.display = 'none'; }, 5000);
	}
}

// Pass status text from here so we do not have to edit a bunch of different source files to change something so trivial
function displayViewSpecial(type) {
	if (type == 'successCreate') {
		displayViewMessage('The entry was successfully added to the database', type);
	}

	if (type == 'successUpdate') {
		displayViewMessage('The entry was successfully updated', type);
	}

	if (type == 'successDelete') {
		displayViewMessage('The entry was successfully deleted from the database', type);
	}

	if (type == 'errorFirstName') {
		displayViewMessage('The first name field may not be left blank', type);
	}

	if (type == 'errorLastName') {
		displayViewMessage('The last name field may not be left blank', type);
	}

	if (type == 'errorPassword') {
		displayViewMessage('The password field may not be left blank', type);
	}

	if (type == 'errorEmptyDatabase') {
		displayViewMessage('That entry does not exist in the database', type);
	}

	if (type == 'errorRedirect'){
		displayViewMessage('You must be signed into the register to view that page', type);
	}

	if (type == 'errorSignIn'){
		displayViewMessage('Bad EmployeeID or password', type);
	}

	if (type == 'errorEmployeeID'){
		displayViewMessage('The EmployeeID field may not be left blank', type);
	}

	if (type == 'errorEmployeeInt'){
		displayViewMessage('The EmployeeID must be a valid integer', type);
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