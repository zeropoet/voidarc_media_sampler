let t = 0;

function setup() {
  createCanvas(windowWidth, windowHeight);
  noFill();
}

function draw() {
  background(240, 230, 250);
  let x = mouseX;
  let y = mouseY;

  for (let i = 0; i < 5; i++) {
    let radius = 50 + (t * 20 + i * 40) % 300;
    let alpha = map(radius, 50, 300, 255, 0);
    stroke(255, 215, 0, alpha);
    strokeWeight(2);
    ellipse(x, y, radius * 2, radius * 2);
  }

  t += 0.01;
}