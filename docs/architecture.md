# System Architecture and Wiring

The EMG Controlled Music System utilizes a hierarchical, multi-stage architecture with an **Arduino Uno R3** acting as the central processing unit. The system processes bio-signal and distance inputs simultaneously, driving an on-board audio stage, an OLED display, and a synchronized desktop application.

---

## Hardware Block Diagram

The block diagram below visualizes the flow of power, sensor signals, and control commands across the system components:

```mermaid
graph TD
    %% Input Stage
    subgraph Input Stage
        EMG[EMG Sensor Module] -->|Analog Signal - A0| Arduino[Arduino Uno R3]
        US[HC-SR04 Ultrasonic] -->|Echo pulse - D7| Arduino
        Arduino -->|Trigger pulse - D6| US
    end

    %% Processing & Control
    subgraph Core Processing
        Arduino
    end

    %% Visual & Serial Output Stage
    subgraph Outputs & Comms
        Arduino -->|I2C Protocol - SDA/SCL| OLED[SSD1306 OLED Display]
        Arduino <=>|USB Serial - 9600 Baud| PC[PyQt6 Desktop Application]
    end

    %% Audio Subsystem
    subgraph Audio Subsystem
        Arduino -->|Software Serial - D3 RX| DF[DFPlayer Mini MP3]
        DF -->|Software Serial - D2 TX| Arduino
        DF -->|Stereo Audio Out L/R| Amp[PAM8403 Amplifier]
        SD[microSD Card] -.->|Read MP3s| DF
        Amp -->|Stereo Output| Spk[3W Speakers x2]
    end

    %% Power distribution
    VCC_5V[USB Power / 5V Rail] ===> EMG
    VCC_5V ===> US
    VCC_5V ===> OLED
    VCC_5V ===> DF
    VCC_5V ===> Amp
    
    style Arduino fill:#1B4F72,stroke:#333,stroke-width:2px,color:#fff
    style EMG fill:#78281F,stroke:#333,stroke-width:2px,color:#fff
    style DF fill:#512E5F,stroke:#333,stroke-width:2px,color:#fff
    style Amp fill:#196F3D,stroke:#333,stroke-width:2px,color:#fff
```

---

## Pin Connections & Wiring Tables

To ensure signal stability and prevent damage to components, use the following wiring configurations.

> [!IMPORTANT]
> **Common Ground Rule**: All components (Arduino, EMG sensor, DFPlayer Mini, OLED, and PAM8403) must share a common ground connection. A floating ground will lead to erratic sensor spikes and communication dropouts.

### 1. EMG Sensor Module
The active and reference electrodes are placed over the forearm muscle, while the ground electrode is placed over a bony, electrically neutral area (such as the wrist or elbow).

| EMG Sensor Pin | Arduino Uno Pin | Signal Type | Description |
| :--- | :--- | :--- | :--- |
| **VCC** | 5V | Power | +5V DC Supply |
| **GND** | GND | Power | Common Ground Reference |
| **SIG** | A0 | Analog Input | Differential muscle output voltage (0-5V) |

### 2. Ultrasonic Proximity Sensor (HC-SR04)
Measures the distance from the sensor to the user's hand.

| HC-SR04 Pin | Arduino Uno Pin | Signal Type | Description |
| :--- | :--- | :--- | :--- |
| **VCC** | 5V | Power | +5V DC Supply |
| **GND** | GND | Power | Common Ground Reference |
| **TRIG** | D6 | Digital Output | Sends 10µs trigger pulse from Arduino |
| **ECHO** | D7 | Digital Input | Sends echo pulse width back to Arduino |

### 3. DFPlayer Mini MP3 Player
Decodes audio tracks from the microSD card.

| DFPlayer Pin | Arduino Uno Pin | Signal Type | Description |
| :--- | :--- | :--- | :--- |
| **VCC (Pin 1)** | 5V | Power | +5V DC Supply |
| **GND (Pin 7)** | GND | Power | Common Ground Reference |
| **RX (Pin 2)** | D3 (via 1kΩ Resistor) | Serial RX | Commands from Arduino (Protected via resistor) |
| **TX (Pin 3)** | D2 | Serial TX | Feedback responses to Arduino |
| **SPK1 (Pin 6)** | PAM8403 L-Input | Analog Output | Left-channel audio signal output |
| **SPK2 (Pin 8)** | PAM8403 R-Input | Analog Output | Right-channel audio signal output |

> [!TIP]
> **RX Line Protection**: Standard Arduino digital output pins supply 5V logic. The DFPlayer Mini RX pin operates at 3.3V logic. A **1kΩ series resistor** must be placed on the Arduino D3 to DFPlayer RX line to prevent logic damage and suppress communication noise.

### 4. SSD1306 OLED Display (128x64)
Provides real-time feedback on-device.

| SSD1306 OLED Pin | Arduino Uno Pin | Signal Type | Description |
| :--- | :--- | :--- | :--- |
| **VCC** | 5V | Power | +5V DC Supply |
| **GND** | GND | Power | Common Ground Reference |
| **SDA** | A4 | I2C Data | Serial Data Line |
| **SCL** | A5 | I2C Clock | Serial Clock Line |

---

## Audio Stage and Speaker Connections

The audio output from the DFPlayer Mini `SPK1` and `SPK2` pins must be amplified to drive two 3W, 4Ω speakers. A **PAM8403 Class-D Stereo Amplifier** is wired as follows:

1. **Power**: Connect the PAM8403 `+5V` and `GND` pins directly to the shared power rails.
2. **Audio Inputs**: 
   - Connect DFPlayer `SPK1` to the Left input (`L`) on the amplifier.
   - Connect DFPlayer `SPK2` to the Right input (`R`) on the amplifier.
   - Connect the central ground input pin (`G`) to the common ground rail.
3. **Audio Outputs**:
   - Wire the left speaker to `L+` and `L-`.
   - Wire the right speaker to `R+` and `R-`.

> [!WARNING]
> **Amplifier Outputs**: The PAM8403 outputs are configured as Bridge-Tied Loads (BTL). **Never** connect the speaker output terminals (`L-` and `R-`) together, and **never** connect them to the system ground. Doing so will permanently damage the amplifier IC.
