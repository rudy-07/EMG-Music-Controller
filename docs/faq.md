# Frequently Asked Questions

Common questions about setting up, calibrating, and using the EMG Controlled Music System:

---

## Hardware Questions

### 1. Which EMG sensor is compatible with this project?
The project is compatible with standard analog surface EMG modules that operate on $5\text{V}$ and output a rectified envelope signal between $0\text{V}$ and $5\text{V}$ (such as the *MyoWare Muscle Sensor* or the *Gravity: Analog EMG Sensor* by DFRobot).

### 2. Can I use a microcontroller other than the Arduino Uno?
Yes. You can use any board compatible with the Arduino ecosystem (e.g., Arduino Nano, Mega, or ESP32). Note that if you use a $3.3\text{V}$ board like the ESP32, you will need to adjust the ADC math ($3.3\text{V}$ reference instead of $5.0\text{V}$) and adjust the thresholds accordingly.

### 3. Do I need gel electrodes?
Yes. Pre-gelled silver/silver-chloride (Ag/AgCl) disposable surface electrodes are highly recommended for the best skin-electrode impedance and noise reduction. Dry electrodes can be used but are significantly more susceptible to movement noise.

---

## Calibration & Calibration Settings

### 4. How do I change the play/pause muscle thresholds?
In `arduino code.txt`, you can change the global thresholds at the top of the file:
```cpp
int flexThreshold  = 650; // Increase if triggering too easily
int relaxThreshold = 580; // Increase if it's hard to trigger release
```
If you find it difficult to trigger a contraction, decrease the `flexThreshold` (e.g., to $600$). If it triggers randomly from hand movements, increase it (e.g., to $700$).

### 5. Why is there a 5-second delay before I can flex again?
The $5\text{-second}$ cooldown is a intentional debounce safety margin. It prevents the system from triggering multiple plays/pauses from a single long muscle contraction. If you want a more rapid trigger rate, you can reduce this in `arduino code.txt`:
```cpp
unsigned long cooldownPeriod = 5000; // Change to 2000 for 2 seconds
```

---

## Audio & Music Customization

### 6. How do I add my own songs to the microSD card?
1. Format your microSD card as **FAT16** or **FAT32**.
2. Create an audio file list. The DFPlayer Mini requires files to be named sequentially, such as `0001.mp3`, `0002.mp3`, `0003.mp3`, etc.
3. Place these files directly in the root directory.
4. Update the song list in both the Arduino code (`songs` struct array) and the Python app database (`SONG_DB` array) with corresponding titles, artists, and durations to keep the metadata synchronized.
