// Getters and setters
function getSaveActionElement() {
	return document.getElementById("saveButton");
}


function getProductId() {
	return getProductIdElement().value;
}

function getProductIdElement() {
	return document.getElementById("productId");
}

function getProductLookupCode() {
	return getProductLookupCodeElement().value;
}

function getProductLookupCodeElement() {
	return document.getElementById("productLookupCode");
}

function getProductCount() {
	return Number(getProductCountElement().value);
}

function getProductCountElement() {
	return document.getElementById("productCount");
}


function updateProduct() {
	const saveActionUrl = ("/api/product/");
	const productData = {id: getProductId(), count: getProductCount(), lookupCode: getProductLookupCode()};

	ajaxPost(saveActionUrl, productData, (callbackResponse) => {
	saveActionElement.disabled = false;

	if (isSuccessResponse(callbackResponse)) {
		alert('Database updated successfully!');

		if ((callbackResponse.data != null)
					&& (callbackResponse.data.id != null)
			&& (callbackResponse.data.id.trim() !== "")) {
		}
	}
});

}