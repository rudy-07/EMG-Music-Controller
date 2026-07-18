# Serial Data & Simulation Protocol

The companion desktop application and the Arduino microcontroller communicate over a standard USB Serial link at a baud rate of **$9600$**. This document details the structured data exchange format and the interactive simulation model.

---

## 1. Outgoing Status Packets (Arduino -> PC)

Every $100\text{ ms}$, the Arduino compiles its local variables and transmits a structured, comma-separated ASCII packet over Serial, terminated by a newline (`\n`):

```text
STATE,SONG_INDEX,ELAPSED_SECONDS,TOTAL_SECONDS,VOLUME,EMG_VALUE,DISTANCE\n
```

### Field Definitions

| Position | Field Name | Data Type | Range / Format | Description |
| :--- | :--- | :--- | :--- | :--- |
| **1** | `STATE` | String | `PLAYING` or `PAUSED` | Current playback state of the MP3 player. |
| **2** | `SONG_INDEX` | Integer | `0`, `1`, `2` | Index of the active track (0-indexed). |
| **3** | `ELAPSED_SECONDS` | Integer | $\ge 0$ | Current elapsed playback position of the song. |
| **4** | `TOTAL_SECONDS`| Integer | $\ge 0$ | Total duration of the active song in seconds. |
| **5** | `VOLUME` | Integer | `5` to `30` | Current output volume level of the DFPlayer. |
| **6** | `EMG_VALUE` | Integer | `0` to `1023` | Live 10-bit raw ADC reading from pin A0. |
| **7** | `DISTANCE` | Integer | `5` to `40` | Live hand-to-sensor distance in centimeters. |

#### Example Packet
```text
PLAYING,1,42,169,22,548,14
```
*Meaning: The system is PLAYING track index 1 (Rave) at position 42 seconds of 169 total. The DFPlayer volume is set to 22. The live raw EMG value is 548, and the hand distance is 14 cm.*

---

## 2. Incoming Command Protocol (PC -> Arduino)

The Arduino parses single-character serial command bytes sent from the PC. It executes actions instantly in a non-blocking manner:

| Byte | Command Action | Firmware Processing Description |
| :---: | :--- | :--- |
| **`T`** | Toggle Playback | Simulates a valid muscle trigger, toggling the play/pause state. |
| **`N`** | Next Song | Increments the song index (looping to 0 if $>2$), resets timers. |
| **`P`** | Previous Song | Decrements the song index (looping to 2 if $<0$), resets timers. |
| **`M`** | Mute | Set DFPlayer volume register directly to $0$. |
| **`U`** | Unmute | Restores volume register to the value mapped by the ultrasonic sensor. |
| **`0`** | Play Song 0 | Loads and plays track `0001.mp3`, resets elapsed timer. |
| **`1`** | Play Song 1 | Loads and plays track `0002.mp3`, resets elapsed timer. |
| **`2`** | Play Song 2 | Loads and plays track `0003.mp3`, resets elapsed timer. |
| **`H`** | Time Sync | Precedes PC system time payload to update the on-board OLED clock. |

---

## 3. Interactive Desktop Simulation Mode

When the physical hardware is not connected, the desktop application enters **Simulation Mode**. A mathematical model generates synthetic signals that mimic physical sensors:

### EMG Envelope Simulation
- **Baseline Noise**: Modelled as a random uniform integer distribution:
  $$EMG_{base} \sim U(540, 580)$$
- **Muscle Flex Spike**: When an event occurs (automatically generated or manually triggered by the GUI's "FLEX" button), the value is spiked to:
  $$EMG_{flex} \sim U(670, 800)$$
- **Contraction Width**: Spikes last for a brief period ($100\text{-}200\text{ ms}$) to simulate a quick, sharp contraction, followed by a relaxation period.

### Hand Proximity Proximity Simulation
- In automatic mode, the hand distance is modeled using a sine wave to simulate a hand swaying closer and further from the sensor over time:
  $$d(t) = 25 + 10 \sin(0.3 \cdot t) + \epsilon$$
  Where $\epsilon \sim U(-0.5, 0.5)$ represents signal jitter.
- The distance is constrained to $[5\text{ cm}, 45\text{ cm}]$.
- The volume is scaled linearly:
  $$Vol(d) = \text{round}\left( \frac{40 - d}{40 - 5} \times 100 \right)\%$$
  This outputs a volume percentage ($0\text{-}100\%$) which directly drives the desktop audio outputs.
