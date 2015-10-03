#include "SparkButton.h"

Adafruit_NeoPixel lanterns(PIXEL_COUNT, PIXEL_PIN, PIXEL_TYPE);
UDP udp;

void setup() {
	lanterns.begin();
	lanterns.show();
	udp.begin(17504);
}

void loop() {
	byte len = udp.parsePacket();
	if (len > 0) {
		byte buf[len];
		udp.read((char*)buf, len);
		for (byte i = 0; i < len / 3; i++) {
			byte offset = i * 3;
			lanterns.setPixelColor(i, buf[offset], buf[offset + 1], buf[offset + 2]);
		}
		lanterns.show();
		udp.flush();
	}
}
