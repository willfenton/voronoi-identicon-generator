import java.util.Random;

String input_str = "giancarlo";
int RUNS = 8;

void setup() {
   size(256, 256);
   environment();
}

void draw() {
   Random hash = new Random(seed(input_str));
   identicon(hash, 0, width, width / RUNS, RUNS);
}

void environment() {
   background(255);
   noStroke();
   rectMode(CORNERS);
   colorMode(HSB);
}

long seed(String str) {
  long num = 1;
  for (int i = 0; i < str.length(); i++) {
    num += int(str.charAt(i));
  }
  return num;
}

void col(Random r) {
  fill(abs(r.nextInt() % 256), 150, 255);
}

void identicon(Random r, float x, float y, float d, int level) {
  col(r);
  rect(x, x, y - d, x + d);
  col(r);
  rect(y - d, x, y, y - d);
  col(r);
  rect(x + d, y - d, y, y);
  col(r);
  rect(x, x + d, x + d, y);
  //recursively repeat inside blank square
  if (level > 1) {
    identicon(r, x + d, y - d, d, level - 1);
  }
}
