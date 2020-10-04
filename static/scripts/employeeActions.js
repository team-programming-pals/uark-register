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
function validatePassword(pass1, pass2){
	//case: passwords do not match
	if(pass1 != pass2){
		displayMessage('Employee passwords do not match.', 'error');
		return false;
	}

}



function validateEmployee() {
	/*
		possible things to check for later:
		-first character is a blank
		-any blanks?
		-is employee id and classification handled correctly?
		-size of password and other blanks
		
	*/
	employeeFirstName = getEmployeeFirstName();
	employeeLastName = getEmployeeLastName();
	employeePassword = getEmployeePassword();
	employeePasswordConfirm = getEmployeePasswordConfirm();
	employeeClassification = getEmployeeClassification();
	if(validatePassword(employeePassword, employeePasswordConfirm) == false){
		return false;
	}
	
	if (employeeFirstName.trim() == "") {
		displayMessage('The First Name field may not be blank', 'error');
		return false;
	}

	if (employeeLastName.trim() == "") {
		displayMessage('The Last Name field may not be blank', 'error');
		return false;
	}
	
	if (employeePassword.trim() == "") {
		displayMessage('The Password field may not be blank', 'error');
		return false;
	}

	if (employeePasswordConfirm.trim() == "") {
		displayMessage('The Password Confirmation field may not be blank', 'error');
		return false;
	}
	
	if (employeePasswordConfirm.trim() == "") {
		displayMessage('The Password Confirmation field may not be blank', 'error');
		return false;
	}

	if (employeeClassification){
		if((employeeClassification != 0)&&(employeeClassification != 1)&&(employeeClassification != 2)) {
		displayMessage('Employee Classification must be 0, 1, or 2.', 'error');
		return false;}
	}
	
	if(employeeID){
		if(employeeID < 0){
			displayMessage('Employee ID must be a positive integer.', 'error');
			return false;
		}
	}
	return true;
}