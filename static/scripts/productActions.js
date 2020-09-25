// =======================================================================
// Title:   productActions.js 
// Purpose: Functions performing actions with product forms
// Date:    September 2020
// ========================================================================

// Grab the product id from the form sending the request
function getProductUUID() {
	return document.getElementById("productUUID").value;
}


// Grab the product code from the form sending the request
function getProductCode() {
	return document.getElementById("productCode").value;
}


// Grab the product count from the form sending the request
function getProductCount() {
	return document.getElementById("productCount").value;
}

function validateProduct(getter){
	//takes in getter and checks for null values, returns the getter
	if (getter == 0)
	{
		return getter;
	}
	else if((getter.length) == 0) {
        return false;
    } else {
        return getter;
    }
}

function Create(){
	//validation function for creating products
	if((validateProduct(getProductCode()))&&(validateProduct(getProductCount())))
	{
		createProduct();
		return;
	}
	else{
		return;
	}		
}

function Submit(){
	//validation function for updating product
	if((validateProduct(getProductCode()))&&(validateProduct(getProductCount()))&&(validateProduct(getProductUUID())))
	{
		updateProduct();
		return;
	}
	else{
		return;
	}		
}

// Add a new product to the database
function createProduct() {
	/* Set up the request by specifying the correct API endpoint,
	grabbing the unique csrf token and collecting the data we
	would like to send to the API */
	const productActionURL = ('/api/products/');
	const securityToken = getCSRFToken('csrftoken');
	const productData = {productCount: getProductCount(), productCode: getProductCode()};

	// As per the comment in apiRequest.js, we need to use the POST verb to create a new database record
	ajaxPost(productActionURL, productData, securityToken, (callbackResponse) => {

	// Use the status code stored in our callbackResponse to see if the request was successful
	if (isSuccessResponse(callbackResponse)) {
		displayMessage('The product was successfully added.', 'success');
		document.getElementById('lookupcode').value = '';
		document.getElementById('count').value = ''
	}

	// Use the status code stored in our callbackResponse to see if the request failed
	if (isErrorResponse(callbackResponse)){
		displayMessage('The request to add a product was denied.', 'failed');
		document.getElementById('lookupcode').value = '';
		document.getElementById('count').value = ''
	}
});

}


// Remove a product from the database
function deleteProduct() {
	//Set up the request by specifying the correct API endpoint,
	const productActionURL = ('/api/products/' + (getProductUUID()) + '/');

	// As per the comment in apiRequest.js, we need to use the DELETE verb to remove an item from the database
	ajaxDelete(productActionURL, (callbackResponse) => {

	// Use the status code stored in our callbackResponse to see if the request was successful
	if (isSuccessResponse(callbackResponse)) {
		displayMessage('The product was successfully deleted.', 'success');
		document.getElementById('lookupcode').value = '';
		document.getElementById('count').value = ''
	}

	// Use the status code stored in our callbackResponse to see if the request failed
	if (isErrorResponse(callbackResponse)){
		displayMessage('The request to delete a product was denied.', 'fail');
		document.getElementById('lookupcode').value = '';
		document.getElementById('count').value = ''
	}
});

}


// Update an existing product in the database
function updateProduct() {
	/* Set up the request by specifying the correct API endpoint,
	grabbing the unique csrf token and collecting the data we
	would like to send to the API */
	const productActionURL = ('/api/products/' + (getProductUUID()) + '/');
	const securityToken = getCSRFToken('csrftoken');
	const productData = {productUUID: getProductUUID(), productCount: getProductCount(), productCode: getProductCode()};

	// As per the comment in apiRequest.js, we need to use the PUT verb to update an existing item in the database
	ajaxPut(productActionURL, productData, securityToken, (callbackResponse) => {

	// Use the status code stored in our callbackResponse to see if the request was successful
	if (isSuccessResponse(callbackResponse)) {
		displayMessage('The product was successfully updated.', 'success');
		document.getElementById('lookupcode').value = '';
		document.getElementById('count').value = ''
	}

	// Use the status code stored in our callbackResponse to see if the request failed
	if (isErrorResponse(callbackResponse)){
		displayMessage('The request to update a product was denied.', 'fail');
		document.getElementById('lookupcode').value = '';
		document.getElementById('count').value = ''
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