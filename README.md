# Real-Time Driver Fatigue Detection with Adaptive Alert Mechanisms With IoT Integrated

This project aims to **detect driver fatigue in real-time** and prevent accidents using **adaptive alert mechanisms**. It also integrates **IoT functionality** to send the driver’s location during drowsy conditions.

---

## Schematic 
<p align="center">
  <img src="https://github.com/SANJAY-K-04/Real-Time-Driver-Fatigue-Detection-with-Adaptive-Alert-Mechanisms-With-IoT-Integration/blob/main/top.jpg?raw=true" width="500" alt="Top View"><br>
  <b>TOP VIEW</b>
</p>

<p align="center">
  <img src="https://github.com/SANJAY-K-04/Real-Time-Driver-Fatigue-Detection-with-Adaptive-Alert-Mechanisms-With-IoT-Integration/blob/main/side.jpg?raw=true" width="500" alt="Side View"><br>
  <b>SIDE VIEW</b>
</p>

<p align="center">
  <img src="https://github.com/SANJAY-K-04/Real-Time-Driver-Fatigue-Detection-with-Adaptive-Alert-Mechanisms-With-IoT-Integration/blob/main/front.jpg?raw=true" width="500" alt="Front View"><br>
  <b>FRONT VIEW</b>
</p>


---


## Components Used

| Component               | Quantity | Description                               |
| ----------------------- | -------- | ----------------------------------------- |
| L298N Dual Motor Driver | 1        | Controls the DC motor (simulating brakes) |
| Gear DC Motor           | 4        | Simulates the vehicle motion              |
| LED                     | 2        | Used for visual alert                     |
| Buzzer                  | 1        | Sounds alert when drowsiness is detected  |
| Arduino UNO             | 1        | Controls the whole system                 |
| GPS Module NEO-6M       | 1        | Sends driver's location via message       |

---

## How It Works

1. The system uses a **camera (or external eye detection logic)** to monitor the driver’s eyes.
2. If the **driver's eyes remain closed for more than 1.5 seconds**, it is considered drowsiness.
3. The **buzzer sounds an alert** to wake the driver.
4. If the driver still doesn’t respond within **1 second**, the **DC motor (vehicle) stops** using the L298N driver (simulating brakes).
5. At the same time, the **current GPS location is captured and sent** (e.g., via SMS module if available, or through serial monitor/log).

---

## Features

* Real-time **driver eye monitoring**
* **Adaptive alert mechanism**: alerts first, then takes safety action
* **Motor control** simulates applying brakes
* **GPS integration** for location sharing in emergencies
* Simple and **cost-efficient hardware setup**

---

## How to Use

1. Upload the Arduino code to your board.
2. Power the circuit.
3. Simulate drowsiness by triggering the eye-closed condition.
4. Observe:

   * Buzzer sounds after 1.5 seconds.
   * Motor stops after 1 second if no action is taken.
   * GPS module captures location (to be integrated with SMS or logging).

---

