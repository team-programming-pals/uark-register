// =======================================================================
// Title:   productActions.js 
// Purpose: Functions performing actions with product forms
// Date:    September 2020
// ========================================================================
function getProductUUID() {
	return document.getElementById("productUUID").value;
}

function getProductCode() {
	return document.getElementById("productCode").value;
}

function getProductCount() {
	return document.getElementById("productCount").value;
}

function createProduct() {
	/* Set up the request by specifying the correct API endpoint,
	grabbing the unique csrf token and collecting the data we
	would like to send to the API */
	const actionURL = ('/products/manage/');
	const securityToken = getCSRFToken('csrftoken');
	const productData = {productCode: getProductCode(), productCount: getProductCount()};

	// As per the comment in apiRequest.js, we need to use the POST verb to create a new record
	ajaxPost(actionURL, productData, securityToken, (callbackResponse) => {

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

function updateProduct() {
	/* Set up the request by specifying the correct API endpoint,
	grabbing the unique csrf token and collecting the data we
	would like to send to the API */
	const actionURL = ('/products/manage/' + getProductUUID() + '/');
	const securityToken = getCSRFToken('csrftoken');
	const productData = {productCode: getProductCode(), productCount: getProductCount()};

	// As per the comment in apiRequest.js, we need to use the PUT verb to update an existing record
	ajaxPut(actionURL, productData, securityToken, (callbackResponse) => {

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

function deleteProduct() {
	/* Set up the request by specifying the correct API endpoint,
	grabbing the unique csrf token and collecting the data we
	would like to send to the API */
	const actionURL = ('/products/manage/' + getProductUUID() + '/');

	// As per the comment in apiRequest.js, we need to use the DELETE verb to delete an existing record
	ajaxDelete(actionURL, (callbackResponse) => {

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

/*
I squished these functions together to make one smaller function. This way
there is less confusion about what is going on. I also removed the check
if someone enters zero, because I feel like there is a legitimate case for
wanting to list an out of stock product
*/
function validateProduct() {
	if (getProductCode().length >= 32){
		displayMessage('The product name must be less than 32 characters', 'error');
		return false;
	}

	if (getProductCode().trim() === "") {
		displayMessage('The product name must may not be blank', 'error');
		return false;
	}

	if (Number(getProductCount()) < 0 || isNaN(getProductCount()) ){
		displayMessage('The product count must be a positive integer', 'error');
		return false;
	}

	return true;
}