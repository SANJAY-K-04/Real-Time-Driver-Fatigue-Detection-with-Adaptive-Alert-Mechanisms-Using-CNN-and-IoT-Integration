// MOTOR PINS
int ena = 5;
int in1 = 6;
int in2 = 7;
int in3 = 8;
int in4 = 9;
int enb = 10;

// LED/Buzzer
int alertPin = 13;

char command = 'b';  // Default to normal running mode

void setup() {
  // Motor pins
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(ena, OUTPUT);
  pinMode(enb, OUTPUT);

  // LED pin
  pinMode(alertPin, OUTPUT);

  // Serial Communication
  Serial.begin(9600);

  // Start car normally
  runMotors();
}

void loop() {
  // Read incoming command from Python
  if (Serial.available()) {
    command = Serial.read();
  }

  if (command == 'z') {
    // Drowsy Alert: Blink LED, motors keep running
    blinkAlert(1);
    runMotors();
  }
  else if (command == 'a') {
    // Brake Mode: Stop motors and blink LED continuously
    stopMotors();
    blinkAlert(2);  // Blink in loop
  }
  else if (command == 'b') {
    // Resume: Normal running, LED off
    digitalWrite(alertPin, LOW);
    runMotors();
  }
}

// Function to run both motors forward
void runMotors() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(ena, 200);  // Adjust speed (0-255)
  analogWrite(enb, 200);
}

// Function to stop both motors
void stopMotors() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  analogWrite(ena, 0);
  analogWrite(enb, 0);
}

// Function to blink LED
void blinkAlert(int mode) {
  digitalWrite(alertPin, HIGH);
  delay(300);
  digitalWrite(alertPin, LOW);
  delay(300);
  
  // If brake mode, keep blinking in loop
  if (mode == 2) {
    while (command == 'a') {
      digitalWrite(alertPin, HIGH);
      delay(300);
      digitalWrite(alertPin, LOW);
      delay(300);
      // Allow breaking loop if new command comes
      if (Serial.available()) {
        command = Serial.read();
        break;
      }
    }
  }
}
