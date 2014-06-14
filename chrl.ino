/* SPI version, connect pin 11 to DS1 and DS2, pin 13 to CP */

#include <SPI.h>

#define RED_BIT 2
#define GREEN_BIT 4
#define BLUE_BIT 8

#define LANTERNS 2

void setup() {
	Serial.begin(9600);
	SPI.setBitOrder(LSBFIRST);
	SPI.setDataMode(SPI_MODE0);
	SPI.setClockDivider(SPI_CLOCK_DIV2);
	SPI.begin();
}

void loop() {
	static uint8_t r[LANTERNS], g[LANTERNS], b[LANTERNS];

	if (Serial.available() >= LANTERNS * 3) {
		for (uint8_t lantern = 0; lantern < LANTERNS; lantern++) {
			r[lantern] = Serial.read();
			g[lantern] = Serial.read() / 3;
			b[lantern] = Serial.read() / 3;
		}
	}

	for (uint8_t i = 0x00; i != 0xFF; i++) {
		for (uint8_t lantern = 0; lantern < LANTERNS; lantern++) {
			uint8_t data = 0;
			if (r[lantern] > i) data |= RED_BIT;
			if (g[lantern] > i) data |= GREEN_BIT;
			if (b[lantern] > i) data |= BLUE_BIT;
			SPI.transfer(data);
		}
		delayMicroseconds(40);
	}
}
