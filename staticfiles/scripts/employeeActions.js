function getEmployeeUUID() {
	return document.getElementById("employeeUUID").value;
}

function getEmployeeID() {
	return document.getElementById("employeeID").value;
}

function getEmployeeFirstName() {
	return document.getElementById("employeeFirstName").value;
}

function getEmployeeLastName() {
	return document.getElementById("employeeLastName").value;
}

function getEmployeePassword() {
	return document.getElementById("employeePassword").value;
}

function getEmployeePasswordConfirm() {
	return document.getElementById("employeePasswordConfirm").value;
}


function getEmployeeClassification() {
	return document.getElementById("employeeClassification").value;
}

function createEmployee() {
	/* Set up the request by specifying the correct API endpoint,
	grabbing the unique csrf token and collecting the data we
	would like to send to the API */
	const actionURL = ('/employees/manage/');
	const securityToken = getCSRFToken('csrftoken');
	const employeeData = {employeeFirstName: getEmployeeFirstName(), 
						 employeeLastName: getEmployeeLastName(), 
						 employeePassword: getEmployeePassword(), 
						 employeeClassification: getEmployeeClassification()};

	// As per the comment in apiRequest.js, we need to use the POST verb to create a new record
	ajaxPost(actionURL, employeeData, securityToken, (callbackResponse) => {

	// Use the status code stored in our callbackResponse to see if the request was successful
	if (isSuccessResponse(callbackResponse)) {
		// Grab the respose from the API end-point and parse it
		var apiResponse = JSON.parse(callbackResponse.apiResponse);

		// Redirect to the sign-in if this is the initial employee
		if (apiResponse['queryResponse'] == 'initial') {
			window.location.href = '/signIn/' + apiResponse['employeeID'];
		}

		// Redirect to the created employees profile
		if (apiResponse['queryResponse'] != 'initial'){
			window.location.href = '/employeeDetails/' + apiResponse['employeeID'];
		}

	}

	// Use the status code stored in our callbackResponse to see if the request failed
	if (isErrorResponse(callbackResponse)){
		// Grab the respose from the API end-point and parse it
		var apiResponse = JSON.parse(callbackResponse.apiResponse);

		// Display error messages
		if (apiResponse['queryResponse']){
			displayMessage(apiResponse['queryResponse'], 'error');
		}
	}
});
}

function updateEmployee() {
	/* Set up the request by specifying the correct API endpoint,
	grabbing the unique csrf token and collecting the data we
	would like to send to the API */
	const actionURL = ('/employees/manage/' + getEmployeeUUID() + '/');
	const securityToken = getCSRFToken('csrftoken');
	const employeeData = {employeeID: getEmployeeID(),
						 employeeFirstName: getEmployeeFirstName(), 
						 employeeLastName: getEmployeeLastName(), 
						 employeePassword: getEmployeePassword(), 
						 employeeClassification: getEmployeeClassification()};

	// As per the comment in apiRequest.js, we need to use the PUT verb to update an existing record
	ajaxPut(actionURL, employeeData, securityToken, (callbackResponse) => {

	// Use the status code stored in our callbackResponse to see if the request was successful
	if (isSuccessResponse(callbackResponse)) {
		// Grab the respose from the API end-point and parse it
		var apiResponse = JSON.parse(callbackResponse.apiResponse);

		// Display success messages
		if (apiResponse['queryResponse']){
			displayMessage(apiResponse['queryResponse'], 'success');
		}
	}

	// Use the status code stored in our callbackResponse to see if the request failed
	if (isErrorResponse(callbackResponse)){
		// Grab the respose from the API end-point and parse it
		var apiResponse = JSON.parse(callbackResponse.apiResponse);

		// Display error messages
		if (apiResponse['queryResponse']){
			displayMessage(apiResponse['queryResponse'], 'error');
		}
	}
});
}

function validateSignIn() {
	employeeID = getEmployeeID();
	employeePassword = getEmployeePassword();

	if (isNaN(employeeID)) {
		displayMessage('The EmployeeID field must be a positive integer', 'error');
		return false;
	}

	if (employeeID.trim() == "") {
		displayMessage('The EmployeeID field may not be blank', 'error');
		return false;
	}

	if (employeePassword.trim() == "") {
		displayMessage('The password field may not be blank', 'error');
		return false;
	}

	return true;
}