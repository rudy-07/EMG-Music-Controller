# Contributing to EMG Controlled Music System

Thank you for your interest in contributing to the **EMG Controlled Music System**! We welcome contributions from researchers, engineers, and makers alike. By contributing, you help make hands-free, bio-signal interfaces more accessible and robust.

---

## Code of Conduct

By participating in this project, you agree to abide by the terms of our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs
- Search the existing [Issues](https://github.com/rudy-07/EMG-Music-Controller/issues) to see if the bug has already been reported.
- If not, open a new Issue, including:
  - A clear and descriptive title.
  - Steps to reproduce the issue.
  - Details about your hardware setup (e.g., Arduino Board, EMG Sensor model).
  - Operating system version (for the desktop app).
  - Error logs and screenshots if applicable.

### Requesting Features
- Open a new Issue and describe the feature you would like to see, along with real-world use cases (e.g., adding BLE support, DSP filter integration).

### Submitting Code Changes (Pull Requests)
1. **Fork** the repository and create your branch from `main`:
   ```bash
   git checkout -b feature/my-amazing-feature
   ```
2. **Set up** the development environment (see below).
3. **Make your changes**:
   - For **firmware** changes, ensure code is strictly non-blocking (`delay()` is prohibited).
   - For **desktop app** changes, follow PEP 8 styling rules for Python.
4. **Test** your changes to ensure no regression in loop latency.
5. **Commit** your changes with clear, descriptive commit messages.
6. **Push** to your fork and submit a **Pull Request (PR)** to the main repository.

---

## Development Setup

### Python GUI App
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```

### Arduino Firmware
1. Open `arduino code.txt` in the Arduino IDE (or rename to `.ino` for native support).
2. Install the required libraries via the Arduino Library Manager:
   - `Adafruit GFX Library`
   - `Adafruit SSD1306`
   - `DFRobotDFPlayerMini`
   - `SoftwareSerial` (built-in)
3. Select **Arduino Uno** and your corresponding COM port, then upload.

---

## Coding Standards

### Firmware
- **Strictly Non-blocking**: Never use `delay()`. Use `millis()` comparisons for tasks that require timing.
- **Structured Data**: Keep serial outputs formatted in the standard comma-separated packet:
  `STATE,SONG_INDEX,ELAPSED_MS,TOTAL_MS,VOLUME,EMG_VALUE,DISTANCE\n`
- Use clear comments for hardware pin assignments.

### Desktop Application (Python)
- Format code using standard PEP 8 guidelines.
- Use meaningful variable names and document all classes and helper functions.
- Handle exceptions gracefully, particularly serial port disconnections.
