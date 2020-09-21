// Return data from API endpoint
function ajaxGet(resourceRelativeUri, callback) {
	return ajax(resourceRelativeUri, action, "GET", null, null, callback);
}

// Create new database records
function ajaxPost(resourceRelativeUri, data, csrftoken, callback) {
	return ajax(resourceRelativeUri, "POST", data, csrftoken, callback);
}

// Update existing database records
function ajaxPut(resourceRelativeUri, data, csrftoken, callback) {
	return ajax(resourceRelativeUri, "PUT", data, csrftoken, callback);
}

// Update individual fields of a record
function ajaxPatch(resourceRelativeUri, data, callback) {
	return ajax(resourceRelativeUri, "PATCH", data, null, callback);
}

// Delete records from the database
function ajaxDelete(resourceRelativeUri, csrftoken, callback) {
	return ajax(resourceRelativeUri, "DELETE", null, csrftoken, callback);
}

// Build and fire off our HTTP request
function ajax(resourceRelativeUri, verb, data, csrftoken, callback) {
	const httpRequest = new XMLHttpRequest();

	if (httpRequest == null) {
		return httpRequest;
	}

	httpRequest.onreadystatechange = () => {
		if (httpRequest.readyState === XMLHttpRequest.DONE) {
			if ((httpRequest.status >= 200) && (httpRequest.status < 300)) {
				handleSuccessResponse(httpRequest, callback);
			} else {
				handleFailureResponse(httpRequest, callback);
			}
		}
	};

	httpRequest.open(verb, resourceRelativeUri, true);
	if ((data != null) && (csrftoken != null)) {
		httpRequest.setRequestHeader('X-CSRFToken', csrftoken);
		httpRequest.setRequestHeader('Content-Type', 'application/json');
		httpRequest.send(JSON.stringify(data));
	} else {
		httpRequest.send();
	}

	return httpRequest;
}

// Generate a response if the API is accessible
function handleSuccessResponse(httpRequest, callback) {
	if (callback != null) {
		let callbackResponse = { status: httpRequest.status };

		if ((httpRequest.responseText != null)
			&& (httpRequest.responseText !== "")) {

			let responseObject = JSON.parse(httpRequest.responseText);
			if (responseObject != null) {
				callbackResponse.data = responseObject;
			}
		}

		callback(callbackResponse);
	}
}

// Generate a response if the API is inaccessible
function handleFailureResponse(httpRequest, callback) {
	if ((httpRequest == null) || (httpRequest.status === 0)) {
		return;
	}

	let errorMessage = "The API is not responding. Try again later.";

	if ((httpRequest.responseText != null)
		&& (httpRequest.responseText !== "")) {

		let responseObject = JSON.parse(httpRequest.responseText);

		if ((responseObject != null)
			&& (responseObject.redirectUrl != null)
			&& (responseObject.redirectUrl !== "")) {

			if (callback) {
				callback({ status: httpRequest.status });
			}
			window.location.assign(responseObject.redirectUrl);

			return;
		}

		if ((responseObject != null)
			&& (responseObject.errorMessage != null)
			&& (responseObject.errorMessage !== "")) {

			errorMessage = responseObject.errorMessage;
		}
	}

	 document.getElementById("status").innerHTML = errorMessage;

	if (callback != null) {
		callback({ status: httpRequest.status });
	}
}

// Check if our request succeeded
function isSuccessResponse(callbackResponse) {
	return ((callbackResponse != null)
		&& (callbackResponse.status != null)
		&& (callbackResponse.status >= 200)
		&& (callbackResponse.status < 300));
}

// Check if our request failed
function isErrorResponse(callbackResponse) {
	return !isSuccessResponse(callbackResponse);
}
