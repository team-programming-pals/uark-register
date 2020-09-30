// Grab the employee uuid from the form sending the request
function getEmployeeUUID() {
	return document.getElementById("employeeUUID").value;
}


// Grab the employee id from the form sending the request
function getEmployeeID() {
	return document.getElementById("employeeID").value;
}


// Grab the employee password from the form sending the request
function getEmployeePassword() {
	return document.getElementById("employeePassword").value;
}


// Display a success or error notification within the status box of the calling view
function displayViewMessage(text, type) {
	// A successful message will give the statusBox a green background and show the hidden element
	if (type == 'successGeneral') {
		document.getElementById('statusBox').style.background = '#4CAF50';
		document.getElementById('statusBox').style.display = 'block';
		document.getElementById('status').innerHTML = text;
		setTimeout(function(){ document.getElementById('statusBox').style.display = 'none'; }, 5000);

	}


	// A failed message will give the statusBox a red background and show the hidden element
	if (type == 'errorGeneral') {

		document.getElementById('statusBox').style.background = '#FFCCCC';
		document.getElementById('statusBox').style.display = 'block';
		document.getElementById('status').innerHTML = text;
		setTimeout(function(){ document.getElementById('statusBox').style.display = 'none'; }, 5000);
	}
}