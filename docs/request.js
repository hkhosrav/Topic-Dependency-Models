function uploadQT() {
	var formdata = new FormData(); //FormData object
    var fileInput = document.getElementById('qt');
	if (fileInput.value == "" || fileInput.files[0].name != "QT.csv"){
		alert("Pleas upload QT.csv");
		return false;
	}
            //Iterating through each files selected in fileInput
    for (i = 0; i < fileInput.files.length; i++) {
                //Appending each file to FormData object
		formdata.append(fileInput.files[i].name, fileInput.files[i]);
    }

            //Creating an XMLHttpRequest and sending
    var xhr = new XMLHttpRequest();
    xhr.open('POST', "https://khosravi.uqcloud.net/tdm/",true);
    xhr.send(formdata);

}

function uploadSQA() {
	var formdata = new FormData(); //FormData object
    var fileInput = document.getElementById('sqa');
	if (fileInput.value == "" || fileInput.files[0].name != "SQA.csv"){
		alert("Pleas upload SQA.csv");
		return false;
	}
            //Iterating through each files selected in fileInput
    for (i = 0; i < fileInput.files.length; i++) {
                //Appending each file to FormData object
		formdata.append(fileInput.files[i].name, fileInput.files[i]);
    }

            //Creating an XMLHttpRequest and sending
    var xhr = new XMLHttpRequest();
    xhr.open('POST', "https://khosravi.uqcloud.net/tdm/",true);
    xhr.send(formdata);

}
