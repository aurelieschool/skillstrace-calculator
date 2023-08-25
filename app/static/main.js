// TODO: FILE STATUS NEEDS TO CHANGE IF THEY UPLOAD A NEW FILE
// ALSO: THEY SHOULD NOT BE ABLE TO SELECT THE WRONG TYPE OF TEST IN THE DROPDOWN

function processFile() {
    const assessmentType = document.getElementById("assessment-types");
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (fileInput)
    if (assessmentType && assessmentType.value) {
        const formData = new FormData();

        formData.append("file", file);
        formData.append("assessment_type", assessmentType.value);

        fetch("/processFile", {
            method:"POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log("File uploaded successfully!", data);
        })
        .catch(error => {
            alert("Error uploading file", error);
        });
    } else {
        alert("Please select a file and assessment type.")
    }
}

function enableDownloadButton() {
    document.getElementById("download-button").disabled = false;
    document.getElementById("download-text").hidden = false;
}


function checkFileStatus() {
    fetch("/check_file_status", { method: "GET" })
        .then(response => response.json())
        .then(handleFileStatusResponse);
}


// handle backend response FOR FILE DOWNLOAD
function handleFileStatusResponse(response) {
    if (response.message === "done") {
        enableDownloadButton(); // download ready
    } else {
        setTimeout(checkFileStatus, 2000) // not ready, check every 2 seconds
    }
}

// FIX THIS. OUTPUT.XLSX SHOULD NOT EXIST...
function downloadButtonFunction() {
    var endpoint = "/download";

    var link = document.createElement("a");
    link.href = endpoint;
    link.download = "output.xlsx";
    link.style.display = "none"; // Hide the link element
    document.body.appendChild(link); // Add the link to the DOM
    link.click(); // Simulate a click to trigger the download

    // Optional: Remove the link from the DOM after the download is initiated
    document.body.removeChild(link);
}

checkFileStatus();
