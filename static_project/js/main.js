var nodes = [];
var NODES = 10;
var CONNECT_DIST = 200;
var CONNECT_DIST2 = CONNECT_DIST * CONNECT_DIST;

var canvas = document.getElementById("can");
var ctx = canvas.getContext("2d");
canvas.width = window.innerWidth - 20;

var SCREENSIZE = [canvas.width, canvas.height];

for (var i = 0; i < NODES; i++) {
	nodes.push({
		x: Math.random() * SCREENSIZE[0],
		y: Math.random() * SCREENSIZE[1],
		z: Math.random() * 1 + 1,
	});
}
function fill(c) {
	ctx.fillStyle = c;
	ctx.fillRect(0, 0, canvas.width, canvas.height);
}
function line(x1, y1, x2, y2, c, w) {
	ctx.strokeStyle = c;
	ctx.lineWidth = w;
	ctx.beginPath();
	ctx.moveTo(x1, y1);
	ctx.lineTo(x2, y2);
	ctx.stroke();
}
function dot(x, y, r, c) {
	ctx.fillStyle = c;
	ctx.beginPath();
	ctx.arc(x, y, r, 0, 2 * Math.PI);
	ctx.fill();
}

setInterval(function draw() {
	fill("#000000");
	for (var i = 0; i < nodes.length; i++) {
		var node = nodes[i];
		dot(node.x, node.y, node.z * 3, "#ffffff07");
		node.x += node.z;
		if (node.x > SCREENSIZE[0] + CONNECT_DIST) {
			node.x = -CONNECT_DIST;
			node.y = Math.random() * SCREENSIZE[1];
			node.z = Math.random() * 1 + 1;
		}
		for (var ii = 0; ii < nodes.length; ii++) {
			var dist =
				Math.pow(nodes[i].x - nodes[ii].x, 2) +
				Math.pow(nodes[i].y - nodes[ii].y, 2);
			if (dist < CONNECT_DIST2) {
				line(
					nodes[i].x,
					nodes[i].y,
					nodes[ii].x,
					nodes[ii].y,
					"#ffffff07",
					(1 - dist / CONNECT_DIST2) * 2.5
				);
			}
		}
	}
}, 10);

var Slides = document.getElementsByClassName("feature");
var currentSlide = 0;
var slideInterval = setInterval(nextSlide, 5000);
for (var i = 0; i < Slides.length; i++) {
	Slides[i].style.display = "none";
}
Slides[currentSlide].style.display = "flex";

function nextSlide() {
	Slides[currentSlide].style.display = "none";
	currentSlide = (currentSlide + 1) % Slides.length;
	Slides[currentSlide].style.display = "flex";
}
