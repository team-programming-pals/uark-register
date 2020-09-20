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

function updateProduct() {
	const csrftoken = getCSRFToken('csrftoken');
	const productData = {id: getProductId(), count: getProductCount(), lookupcode: getProductLookupCode(), action: getProductAction()};

	ajaxPost('/api/product/', productData, csrftoken, (callbackResponse) => {

	if (isSuccessResponse(callbackResponse)) {
		// We need code here to display a successful request on the productDetails.html page
		document.getElementById("status").innerHTML = "Database successfully updated.";
	}

	if (isErrorResponse(callbackResponse)){
		// We need code here to display a failed request on the productDetails.html page
		document.getElementById("status").innerHTML = "Unable to update database.";
	}
});

}