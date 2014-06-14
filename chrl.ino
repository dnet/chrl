/* SPI version, connect pin 11 to DS1 and DS2, pin 13 to CP */

#include <SPI.h>

#define RED_BIT 2
#define GREEN_BIT 4
#define BLUE_BIT 8

void setup() {
	Serial.begin(9600);
	SPI.setBitOrder(LSBFIRST);
	SPI.setDataMode(SPI_MODE0);
	SPI.setClockDivider(SPI_CLOCK_DIV2);
	SPI.begin();
}

void loop() {
	static uint8_t r = 0, g = 0, b = 0;

	if (Serial.available() > 2) {
		r = Serial.read();
		g = Serial.read() / 3;
		b = Serial.read() / 3;
	}

	for (uint8_t i = 0x00; i != 0xFF; i++) {
		uint8_t data = 0;
		if (r > i) data |= RED_BIT;
		if (g > i) data |= GREEN_BIT;
		if (b > i) data |= BLUE_BIT;
		SPI.transfer(data);
		delayMicroseconds(40);
	}
}
