# Signal Acquisition & Preprocessing

The primary input of the system is the electromyographic (EMG) bio-signal. Because raw surface EMG (sEMG) signals are low-voltage ($0.1\text{ mV}$ to $10\text{ mV}$) and contain high levels of stochastic high-frequency noise and powerline interference, robust preprocessing is required before digital classification.

---

## 1. Electrode Placement Guidelines

The system uses three surface electrodes placed in a differential measurement configuration to capture electrical activity while canceling out common-mode environmental noise:

- **Active (Red) Electrode**: Placed over the thickest part of the forearm muscle belly (e.g., the *flexor carpi radialis*), which generates the largest action potentials during hand flexion.
- **Reference (Green) Electrode**: Placed along the same muscle, parallel to the active electrode (approximately $2\text{ cm}$ apart).
- **Ground (Yellow) Electrode**: Placed over an electrically neutral, bony area (such as the wrist or elbow joint) to serve as a stable zero-voltage reference.

```text
       [Active / Red]          [Reference / Green]
       (Muscle Belly)            (Muscle Belly)
             |                         |
    [=======o==========================o=======] <-- Forearm Muscle
                                                    [======o======] <-- Bony Wrist
                                                           |
                                                    [Ground / Yellow]
```

---

## 2. Analog Signal Conditioning

The EMG sensor module contains dedicated analog circuitry that prepares the microvolt-level muscle signals for the microcontroller's Analog-to-Digital Converter (ADC):

1. **Differential Amplification**: An instrumentation amplifier amplifies the tiny voltage difference between the Red (Active) and Green (Reference) electrodes. Signals common to both electrodes (such as $50\text{Hz}/60\text{Hz}$ environmental powerline hum) are canceled out, utilizing a high Common-Mode Rejection Ratio (CMRR).
2. **Filtering**: 
   - A **High-Pass Filter** (typically cutoff at $10\text{ Hz}$) removes low-frequency movement artifacts caused by electrode displacement or skin stretching.
   - A **Low-Pass Filter** (typically cutoff at $500\text{ Hz}$) removes high-frequency thermal noise and electromagnetic interference.
3. **Rectification**: The raw AC muscle potentials are fully rectified, converting negative voltage lobes into positive values to form a unipolar signal.
4. **Envelope Extraction**: An active integrator smooths out the rectified high-frequency spikes, outputting an analog voltage envelope ($0\text{V}$ to $5\text{V}$) that represents the active force of the muscle contraction.

---

## 3. ADC Conversion and Sampling

The smoothed analog voltage output from the sensor is routed to the Arduino Uno's analog pin `A0`.

### 10-Bit ADC Math
The ATmega328P microcontroller utilizes a 10-bit successive-approximation ADC. It maps the incoming analog voltage ($0\text{V}$ to $5\text{V}$) to a digital value between $0$ and $1023$:

$$ADC = \text{round}\left( \frac{V_{in}}{V_{ref}} \times 1023 \right)$$

Where $V_{ref} = 5.0\text{ V}$. Conversely, the voltage envelope can be calculated from the digital reading:

$$V_{in} = \frac{ADC \times 5.0}{1023}$$

### Sampling Rate
The main program loop of the firmware executes cyclically with a short delay at the end:
```cpp
delay(10); // 10ms smooth loop
```
Accounting for loop overhead and sensor reading, this creates an effective sampling rate of approximately **$100\text{ Hz}$** ($100$ samples per second). According to the Nyquist-Shannon sampling theorem, this allows the system to reconstruct signal envelope changes up to $50\text{ Hz}$, which is more than sufficient for detecting deliberate, macro-level muscle contraction gestures (typically taking $300\text{ ms}$ to $1\text{ s}$).
