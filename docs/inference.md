# Real-Time Execution Loop & Non-Blocking Design

A critical requirement of the embedded software is real-time responsiveness. The Arduino Uno must process physical sensor signals, drive the audio player, render data on the OLED display, and communicate with the PC. 

To achieve this without lag, the firmware is structured on a **strictly non-blocking cyclic-executive architecture**.

---

## 1. The Cyclic Loop Architecture

The main loop consists of modular functions called sequentially. The CPU never sleeps or waits in a blocked state:

```cpp
void loop() {
  updateUltrasonic();    // Digital read of proximity (volume control)
  updateEMG();           // Analog read of muscle signal (play/pause control)
  checkSerialCommands(); // Read incoming commands from the PC app
  updateSongLogic();     // Track track durations and loop logic
  drawUI();              // Update the 128x64 OLED display
  sendSerialPacket();    // Send system state data to the PC app
  
  delay(10);             // 10ms pacing delay (non-blocking margin)
}
```

---

## 2. Refactoring Analysis: Eliminating Blocking I/O

In early iterations, the system suffered from significant user-interface lag and missed muscle contraction triggers. Profile analysis identified two major blocking bottlenecks: the ultrasonic read and serial character reads.

### A. Ultrasonic Proximity Bottleneck
The standard Arduino `pulseIn(pin, HIGH)` function waits for a pin to transition from LOW to HIGH, then counts the duration until it transitions back to LOW. If the user's hand is out of range, or the signal is absorbed, `pulseIn()` blocks execution for its default timeout of **$1\text{ second}$** ($1,000,000\text{ µs}$).

#### The Solution: Custom Timeout Parameter
We applied a strict $30\text{ ms}$ ($30,000\text{ µs}$) timeout to the function:
```cpp
durationUS = pulseIn(ECHO, HIGH, 30000); // 30ms timeout limit
```
If no echo returns within $30\text{ ms}$ (representing an object distance greater than $\approx 5\text{ meters}$), the function terminates immediately, returning `0`. The loop continues uninterrupted, preventing latency spikes.

### B. Serial Communication Bottleneck
Reading PC commands using `Serial.readStringUntil('\n')` blocks the processor until a newline character arrives or the serial timeout (defaulting to $1,000\text{ ms}$) expires.

#### The Solution: Character-by-Character Buffering
We refactored this into a fast, non-blocking check:
```cpp
void checkSerialCommands() {
  if (!Serial.available()) return; // Exit immediately if buffer is empty
  
  char cmd = Serial.read(); // Read exactly one byte from hardware register
  
  // Immediately process command
  if (cmd == 'T') {
    togglePlayPause();
  }
  // ... (process other commands)
}
```
This check executes in less than a microsecond when no serial bytes are present.

---

## 3. Software-Based Song Timing

The DFPlayer Mini does not have registers that expose the current elapsed playback position (e.g., "elapsed seconds"). To display a progress bar on the OLED, the Arduino must track playback time using its internal hardware timer (`millis()`).

### The Mathematical Model
We maintain two states: `PLAYING` and `PAUSED`.

#### When PLAYING:
The elapsed playback time ($t_{elapsed}$) is the sum of the time accumulated in prior playing intervals ($t_{accumulated}$) and the time spent in the current active interval (current time minus the start time of the current play session):

$$t_{elapsed} = t_{accumulated} + \left( t_{now} - t_{start} \right)$$

In C++:
```cpp
elapsed = accumulatedTime + (millis() - songStartTime);
```

#### When PAUSED:
The elapsed playback time is frozen at the accumulated time:

$$t_{elapsed} = t_{accumulated}$$

When the system transitions from `PLAYING` to `PAUSED`, the elapsed time is finalized and added to the accumulator:
```cpp
// On Pause Trigger:
accumulatedTime += millis() - songStartTime;
isPlaying = false;
```
When transitioning from `PAUSED` to `PLAYING`, the reference point is reset:
```cpp
// On Play/Resume Trigger:
songStartTime = millis();
isPlaying = true;
```

This math tracks the song progress with millisecond precision, enabling automatic song looping when $t_{elapsed} \ge t_{duration}$.
