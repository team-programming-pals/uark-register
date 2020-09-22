function getProductId() {
	return document.getElementById("productID").value;
}

function getProductLookupCode() {
	return document.getElementById("lookupcode").value;
}

function getProductCount() {
	return Number(document.getElementById("count").value);
}

function getProductAction() {
	return document.getElementById("action").value;
}

function getCSRFToken(name) {
    let tokenValue = null;
    if (document.cookie && document.cookie !== '') {
        const tokens = document.cookie.split(';');
        for (let i = 0; i < tokens.length; i++) {
            const token = tokens[i].trim();
            if (token.substring(0, name.length + 1) === (name + '=')) {
                tokenValue = decodeURIComponent(token.substring(name.length + 1));
                break;
            }
        }
    }
    return tokenValue;
}

function createProduct() {
	const productActionURL = ('/api/products/');
	const csrftoken = getCSRFToken('csrftoken');
	const productData = {count: getProductCount(), lookupcode: getProductLookupCode()};

	ajaxPost(productActionURL, productData, csrftoken, (callbackResponse) => {

	if (isSuccessResponse(callbackResponse)) {
		document.getElementById("status").innerHTML = "Database successfully updated.";
	}

	if (isErrorResponse(callbackResponse)){
		document.getElementById("status").innerHTML = "Unable to update database.";
	}
});

}

function updateProduct() {
	const productActionURL = ('/api/products/' + (getProductId()) + '/');
	const csrftoken = getCSRFToken('csrftoken');
	const productData = {id: getProductId(), count: getProductCount(), lookupcode: getProductLookupCode()};

	ajaxPut(productActionURL, productData, csrftoken, (callbackResponse) => {

	if (isSuccessResponse(callbackResponse)) {
		document.getElementById("status").innerHTML = "Database successfully updated.";
	}

	if (isErrorResponse(callbackResponse)){
		document.getElementById("status").innerHTML = "Unable to update database.";
	}
});

}