import * as crypto from "crypto-js";
import Voronoi from "./rhill-voronoi-core.js";

const imageElement: HTMLImageElement = document.querySelector(".identicon-image");
const stringSelect: HTMLInputElement = document.querySelector("#string-select");
const hashSelect: HTMLSelectElement = document.querySelector("#hash-select");
const downloadButton: HTMLButtonElement = document.querySelector("#download-button");
const canvas: HTMLCanvasElement = document.querySelector("#canvas");

canvas.width = 2048;
canvas.height = 2048;

// canvas context
// used to draw on the canvas
const ctx = canvas.getContext("2d");

const voronoi = new Voronoi();
var diagram = null;

class Point {
    constructor(public x: number, public y: number, public color: string) { }
}

generateDiagram("");

animate();

function animate() {
    // call animate in a loop for each frame
    requestAnimationFrame(animate);

    // clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (diagram != null) {
        for (let cell of diagram.cells) {
            ctx.fillStyle = cell.site.color;

            const startX = cell.site.x * canvas.width;
            const startY = cell.site.y * canvas.height;

            ctx.beginPath();
            ctx.moveTo(startX, startY);

            for (let point of cell.path) {
                const x = point.x * canvas.width;
                const y = point.y * canvas.height;
                ctx.lineTo(x, y);
            }
            ctx.closePath();
            ctx.fill();
        }
    }
}

function generateDiagram(seedString: string) {
    // hash the entered string
    const hash = crypto.SHA512(stringSelect.value);

    // convert the hash to hexadecimal
    const hashHex = hash.toString(crypto.enc.Hex);

    // console.log(hash);
    // console.log(hashHex);

    // convert hex to bytes
    const byteArray = [];
    for (let i = 0; i < hashHex.length; i += 2) {
        const hexByte = hashHex.substring(i, i + 2);
        const decimalByte = parseInt(hexByte, 16).toString(10);

        byteArray.push(decimalByte);
    }
    // console.log(byteArray);

    const numBytes = hashHex.length / 2;
    const numSectors = Math.floor(numBytes / 3);

    // console.log(numBytes, numSectors);

    const pointBytes = byteArray.slice(0, numSectors * 2);
    const colorBytes = byteArray.slice(numSectors * 2, numSectors * 3);

    // console.log(pointBytes);
    // console.log(colorBytes);

    const points: Array<Point> = [];

    for (let i = 0; i < numSectors; i++) {
        const x = pointBytes[(i * 2)] / 255;
        const y = pointBytes[(i * 2) + 1] / 255;
        const hue = colorBytes[i] * 360 / 255;
        const color = `hsl(${hue}, 100%, 50%)`;
        const point = new Point(x, y, color);
        points.push(point);
    }

    // console.log(points);

    const bbox = {
        xl: 0,
        xr: 1,
        yt: 0,
        yb: 1
    };

    if (diagram != null) {
        voronoi.recycle(diagram);
    }
    diagram = voronoi.compute(points, bbox);

    for (let cell of diagram.cells) {
        const path = [];
        for (let halfEdge of cell.halfedges) {
            path.push(halfEdge.getStartpoint());
            path.push(halfEdge.getEndpoint());
        }
        cell.path = path;
    }

    // console.log(diagram);
}

stringSelect.onkeyup = function () {
    // console.log(`generate ${stringSelect.value}`);

    generateDiagram(stringSelect.value);
}

downloadButton.onclick = downloadIdenticon;

function downloadIdenticon() {
    // get an url for the image data
    const dataUrl = canvas.toDataURL();

    // create an anchor tag which will download the identicon when clicked on
    const downloadLink = document.createElement('a');
    downloadLink.href = dataUrl;

    if (stringSelect.value == "") {
        downloadLink.download = "identicon.png";
    }
    else {
        // replace non-alphanumeric characters with '_'
        const name = stringSelect.value.replace(/[^a-z0-9]/gi, '_').toLowerCase();
        downloadLink.download = `identicon-${name}.png`;
    }

    // click the anchor tag
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}
