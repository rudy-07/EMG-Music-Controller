# API Reference & Code Structure

This document outlines the software architecture, class structures, and function definitions of both the Arduino firmware and the PyQt6 companion application.

---

## 1. Arduino Firmware Functions

The embedded code resides in `arduino code.txt` and is structured as a cyclical executive program.

### `void setup()`
- Initializes standard hardware serial and SoftwareSerial at $9600\text{ Baud}$.
- Configures pins: `TRIG` (Output), `ECHO` (Input).
- Initializes the SSD1306 OLED display over I2C (`0x3C`).
- Connects to the DFPlayer Mini module and resets the volume to $15$.

### `void loop()`
- Cyclically runs the program modules in a non-blocking sequence: `updateUltrasonic()`, `updateEMG()`, `checkSerialCommands()`, `updateSongLogic()`, `drawUI()`, `sendSerialPacket()`.
- Incorporates a `delay(10)` to stabilize the ADC readings.

### `void updateUltrasonic()`
- Drives `TRIG` HIGH for $10\text{ µs}$ to emit ultrasonic bursts.
- Reads `ECHO` with a $30,000\text{ µs}$ timeout.
- Converts pulse time to distance in cm: $d = \frac{t}{58}$.
- Maps distance ($5\text{ cm} - 40\text{ cm}$) to volume ($30 - 5$) and updates the DFPlayer.

### `void updateEMG()`
- Reads the raw analog input from pin `A0`.
- Implements the dual-threshold hysteresis state machine (`650` flex / `580` relax).
- Validates the contraction cycle and toggles playback state.
- Implements the $5\text{-second}$ cooldown lock.

### `void checkSerialCommands()`
- Non-blockingly reads the serial buffer using `Serial.available()`.
- Parses incoming single-byte commands and triggers corresponding audio actions.

### `void updateSongLogic()`
- Compares elapsed milliseconds against active song durations.
- Automatically increments track counters and triggers next track commands upon song completion.

### `void drawUI()`
- Renders system state, track metadata, volume, distance, raw EMG value, and visual seekbar to the OLED display buffer, pushing it to screen.

---

## 2. PyQt6 Desktop Application Code Structure

The GUI application resides in `app.py` and is built using PyQt6.

### Class: `EMGMusicApp(QMainWindow)`
The main GUI Window.
- **`__init__()`**: Configures custom frameless window styling, window moving controls, custom widgets, and background animation.
- **`init_ui()`**: Constructs the UI layouts, integrating the gauges, graph plot, and player media controllers.
- **`update_dashboard(data, source)`**: Updates UI labels, gauges, seekbar, and scrolling graphs from incoming data dictionary packets.

### Class: `SerialWorker(QThread)`
An asynchronous thread that handles background communication with the Arduino.
- **`run()`**: Scans for active COM ports, attempts connection, reads lines from the buffer, parses comma-separated data, and emits PyQt signals back to the main thread.
- **`send_command(cmd)`**: Enqueues and sends command character bytes over the serial port.

### Class: `NeuroSimulator`
Simulates hardware inputs when the physical Arduino is not connected.
- **`get_data()`**: Computes synthetic values including random base noise, muscle flex spikes, and hand distance values (modeled via sine waves).

### Class: `AggressiveGauge(QWidget)`
A premium custom circular gauge widget.
- **`paintEvent()`**: Uses `QPainter` to draw custom radial arcs representing volume levels and distances.

### Class: `TechToggle(QWidget)`
A custom slide toggle switch.
- **`paintEvent()`**: Draws sliding track panel representing toggle states (e.g., SIM vs HARDWARE mode).

### Class: `TechBackground(QWidget)`
Draws the custom moving tech grid background.
- **`animate()`**: Shifts grid lines to give a dynamic, reactive feel to the workspace.
