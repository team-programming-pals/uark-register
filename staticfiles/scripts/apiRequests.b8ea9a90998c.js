// Use ajaxGet when you want to get information from the database
function ajaxGet(resourceRelativeUri, callback) {
	return ajax(resourceRelativeUri, action, "GET", null, null, callback);
}

// Use ajaxPost when you want to create a new database record
function ajaxPost(resourceRelativeUri, data, token, callback) {
	return ajax(resourceRelativeUri, "POST", data, token, callback);
}

// Use ajaxPut when you want to update an existing database record
function ajaxPut(resourceRelativeUri, data, token, callback) {
	return ajax(resourceRelativeUri, "PUT", data, token, callback);
}

// Use ajaxPatch when you want to update an individual field within a database record
function ajaxPatch(resourceRelativeUri, data, token, callback) {
	return ajax(resourceRelativeUri, "PATCH", data, token, callback);
}

// Use ajaxDelete when you want to delete a record from the database
function ajaxDelete(resourceRelativeUri, callback) {
	return ajax(resourceRelativeUri, "DELETE", null, null, callback);
}

// Construct a valid HTTP request and send the request to our API
function ajax(resourceRelativeUri, verb, data, token, callback) {
	const httpRequest = new XMLHttpRequest();

	// Make sure we are using a valid httpRequest object
	if (httpRequest == null) {
		return httpRequest;
	}

	// Check to see if we can communicate with the API
	httpRequest.onreadystatechange = () => {
		if (httpRequest.readyState === XMLHttpRequest.DONE) {
			if ((httpRequest.status >= 200) && (httpRequest.status < 300)) {
				handleSuccessResponse(httpRequest, callback);
			} else {
				handleFailureResponse(httpRequest, callback);
			}
		}
	};

	// Build and send an appropriate request for the specified verb
	httpRequest.open(verb, resourceRelativeUri, true);
	if ((data != null) && (token != null)) {
		// Sends the data and headers for the POST, PUT, and PATCH verbs
		httpRequest.setRequestHeader('X-CSRFToken', token);
		httpRequest.setRequestHeader('Content-Type', 'application/json');
		httpRequest.send(JSON.stringify(data));
	} else {
		// Sends the request for the GET and DELETE verbs
		httpRequest.send();
	}

	return httpRequest;
}

// Update the callback if our API is accessible
function handleSuccessResponse(httpRequest, callback) {
	if (callback != null) {
		// Add the returned status code to callbackResponse
		let callbackResponse = { status: httpRequest.status };

		if ((httpRequest.responseText != null)
			&& (httpRequest.responseText !== "")) {

			let responseObject = JSON.parse(httpRequest.responseText);
			if (responseObject != null) {

				// If the API sends a response back, add the response to callbackResponse
				callbackResponse.data = responseObject;
			}
		}

		// Update the requesting functions callback so it can have the status code and response
		callback({ status: httpRequest.status, responseMessage: httpRequest.responseText });
	}
}

// Update the callback if our API is not accessible
function handleFailureResponse(httpRequest, callback) {
	if ((httpRequest == null) || (httpRequest.status === 0)) {
		return;
	}

	let errorMessage = "The API is not responding. Try again later.";

	if ((httpRequest.responseText != null)
		&& (httpRequest.responseText !== "")) {

		let responseObject = JSON.parse(httpRequest.responseText);

		// Handle the failed request with a redirect
		if ((responseObject != null)
			&& (responseObject.redirectUrl != null)
			&& (responseObject.redirectUrl !== "")) {

			if (callback) {
				// Update the requesting functions callback so it can have the status code
				callback({ status: httpRequest.status });
			}

			// Allow the API to redirect the client after a bad request
			window.location.assign(responseObject.redirectUrl);

			return;
		}

		// Handle the failed request by sending an error message to the calling page
		if ((responseObject != null)
			&& (responseObject.errorMessage != null)
			&& (responseObject.errorMessage !== "")) {

			errorMessage = responseObject.errorMessage;
		}
	}

	if (callback != null) {
		// Update the callback so we can pass along the status code and responseText
		callback({ status: httpRequest.status, responseMessage: httpRequest.responseText });
	}
}


// Use the status code stored in our callbackResponse to see if the request was successful
function isSuccessResponse(callbackResponse) {
	//Check out https://www.w3schools.com/tags/ref_httpmessages.asp to see what the codes mean 
	return ((callbackResponse != null)
		&& (callbackResponse.status != null)
		&& (callbackResponse.status >= 200)
		&& (callbackResponse.status < 300));
}

// Use the status code stored in our callbackResponse to see if the request failed
function isErrorResponse(callbackResponse) {
	return !isSuccessResponse(callbackResponse);
}
