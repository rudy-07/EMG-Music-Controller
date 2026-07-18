# Troubleshooting Guide

Follow this guide to diagnose and resolve issues with the hardware components, wiring, serial connections, and desktop application.

---

## 1. EMG Sensor & Trigger Issues

### Symptom: Muscle flexes do not trigger play/pause
* **Check Skin Contact**: Verify that the pre-gelled electrodes are firmly attached to the forearm. Hair, dry skin, or reusable electrodes with dried gel can severely degrade the signal. Clean the skin with rubbing alcohol before application.
* **Verify Electrode Placement**: Ensure the Red (Active) and Green (Reference) electrodes are placed along the main muscle belly, and the Yellow (Ground) electrode is placed on a bony area (such as the wrist).
* **Trimpot Calibration**: Most analog EMG modules include a small physical trimpot (gain potentiometer). 
  - If the signal remains low, turn the trimpot **clockwise** to increase gain.
  - If the signal is saturated at max value ($1023$), turn the trimpot **counterclockwise** to reduce gain.
* **Monitor Raw Stream**: Open the PyQt6 desktop app or the Arduino Serial Plotter to watch the raw EMG readings. Ensure the signal stays below $580$ at rest and exceeds $650$ during a strong contraction.

### Symptom: Random/chattering triggers
* **Increase Cooldown**: The user may be contracting their muscle multiple times. Increase the `cooldownPeriod` to $5000\text{ ms}$ in the firmware.
* **Cable Strain**: Check for loose jumper wires. Movements of the sensor cable can create voltage spikes. Tape the cables to your arm to minimize motion artifacts.

---

## 2. Serial Communication Issues

### Symptom: Desktop app displays "SERIAL LIBRARY MISSING"
* **Install PySerial**: The Python environment does not have the `pyserial` package. Run:
  ```bash
  pip install pyserial
  ```
  *(Note: Avoid installing `serial`. If you did, uninstall it first: `pip uninstall serial pyserial` then run `pip install pyserial`).*

### Symptom: Desktop app displays "NO DEVICES FOUND" or fails to connect
* **Check USB Connection**: Ensure the Arduino is connected to the PC via the USB cable.
* **COM Port Conflicts**: The Arduino Serial Monitor in the Arduino IDE might be open, locking the COM port. **Close the Arduino IDE Serial Monitor** before starting the desktop application.
* **Driver Check**: If the COM port is not detected, you may need to install USB-to-Serial drivers for your Arduino board (e.g., CH340 drivers for clone boards, or official Arduino drivers).

---

## 3. OLED Display Issues

### Symptom: OLED display screen remains completely blank
* **Verify I2C Addressing**: The default I2C address for $0.96\text{-inch}$ SSD1306 displays is `0x3C`. Some displays use `0x3D`. Check the line in `arduino code.txt`:
  ```cpp
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  ```
* **Verify Pins**: Ensure SDA is connected to Arduino `A4` and SCL is connected to Arduino `A5`. **Never swap SDA and SCL**.
* **Check VCC/GND**: Verify the display is receiving +5V power and shares a ground rail with the Arduino.

---

## 4. Audio Stage & Speaker Issues

### Symptom: Loud buzzing or high-pitched hum in speakers
* **Common Ground Noise**: Ground loops are a major cause of audio noise. Make sure the ground connection between the DFPlayer Mini, the PAM8403 amplifier, and the Arduino is as short and thick as possible.
* **DFPlayer RX Resistor**: Check that a **$1\text{ kΩ}$ resistor** is in series between Arduino digital pin `D3` and DFPlayer pin `2` (RX). Without this resistor, digital noise from the serial commands will bleed into the analog audio stage.
* **Separate Power Rails**: The PAM8403 amplifier draws high transient currents. If powered directly from the Arduino's 5V pin, it can cause voltage sag and hum. For optimal quality, power the PAM8403 and the Arduino using a split USB power cable or a dedicated 5V power supply.
