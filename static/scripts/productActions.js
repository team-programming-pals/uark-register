// Getters and setters
function getProductId() {
	return getProductIdElement().value;
}

function getProductIdElement() {
	return document.getElementById("productID");
}

function getProductLookupCode() {
	return getProductLookupCodeElement().value;
}

function getProductLookupCodeElement() {
	return document.getElementById("lookupcode");
}

function getProductCount() {
	return Number(getProductCountElement().value);
}

function getProductCountElement() {
	return document.getElementById("count");
}

function getProductAction() {
	return getProductActionElement().value;
}

function getProductActionElement() {
	return document.getElementById("action");
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateProduct() {
	const csrftoken = getCookie('csrftoken');
	const productData = {id: getProductId(), count: getProductCount(), lookupcode: getProductLookupCode(), action: getProductAction()};

	ajaxPost('/api/product/', productData, csrftoken, (callbackResponse) => {

	if (isSuccessResponse(callbackResponse)) {
		alert('Database updated successfully!');

		if ((callbackResponse.data != null)
					&& (callbackResponse.data.id != null)
			&& (callbackResponse.data.id.trim() !== "")) {
		}
	}
});

}