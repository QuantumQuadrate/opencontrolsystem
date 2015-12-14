/*
  String to Float conversion

 Reads a serial input string until it sees a newline, then converts
 the string to a float number if the characters are digits. Note that 
 floating point numbers are only accurate up to about 7 characters.

 The circuit:
 No external components needed.

 created 10 Nov 2014 by Arturo Guadalupi
 modified 10 Dec 2014 by Michael Shiloh

 This example code is in the public domain.
 */

String inString = "";    // string to hold input

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }

  // send an intro:
  Serial.println("\n\nExample of the toFloat() method of the String class.\n");
  Serial.println("Type a legitimate floating point string and it will be converted to a float.");
  Serial.println("One decimal point is allowed.");
  Serial.println("Any non-numeric character or a second decimal point stops the conversion.");
  Serial.println();
  Serial.println("Make sure you set your terminal to send Newline line endings");
}

void loop() {
  // Read serial input:
  while (Serial.available() > 0) {
    int inChar = Serial.read();

    if (inChar != '\n') { 

      // As long as the incoming byte
      // is not a newline,
      // convert the incoming byte to a char
      // and add it to the string
      inString += (char)inChar;
    }
    // if you get a newline, print the string,
    // then the string's value as a float:
    else {
      Serial.print("Input string: ");
      Serial.print(inString);
      Serial.print("\tAfter conversion to float:");
      Serial.println(inString.toFloat());
      // clear the string for new input:
      inString = "";
    }
  }
}
