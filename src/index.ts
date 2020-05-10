import * as paper from "paper";
import { Voronoi } from "./rhill-voronoi-core.js";


var imageElement: HTMLImageElement = document.querySelector(".identicon-image");
var stringSelect: HTMLInputElement = document.querySelector("#string-select");
var hashSelect: HTMLSelectElement = document.querySelector("#hash-select");
var downloadButton: HTMLButtonElement = document.querySelector("#download-button");

stringSelect.onkeyup = function () {
    if (stringSelect.value.length == 0) {
        alert("Must enter a string");
    }
    else {
        console.log(`generate ${stringSelect.value}`);
    }
}
