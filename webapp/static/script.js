var imageElement = document.querySelector(".identicon-image");
var stringSelect = document.querySelector("#string-select");
var sizeSelect = document.querySelector("#size-select");
var hashSelect = document.querySelector("#hash-select");
var blurSelect = document.querySelector("#blur-select");
var submitButton = document.querySelector("#generate-button");
var downloadButton = document.querySelector("#download-button");

submitButton.onclick = function () {
    if (stringSelect.value.length == 0) {
        alert("Must enter a string");
    }
    else if (stringSelect.value.includes("/")) {
        alert("String cannot contain '/'");
    }
    else {
        console.log(stringSelect.value, sizeSelect.value, hashSelect.value, blurSelect.value);
        let apiUrl = `/identicons/${hashSelect.value}/${sizeSelect.value}/${blurSelect.value}/${stringSelect.value}`;
        console.log(apiUrl);

        imageElement.src = "static/loading.gif"
        downloadButton.style.display = "none";

        fetch(apiUrl).then((response) => {
            return response.json();
        }).then((json) => {
            imageElement.src = json["image_url"];

            downloadButton.style.display = "block";
            downloadButton.href = imageElement.src;
            // downloadButton.onclick = function() {
            //     window.open(imageElement.src);
            // }
        });
    }
}