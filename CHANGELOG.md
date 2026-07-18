# Changelog

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-04-30
*Initial stable release compiled in the project report.*

### Added
- **Hardware Integration**: Custom schematics and support for EMG Sensor, HC-SR04 Ultrasonic Sensor, DFPlayer Mini, PAM8403 Amplifier, and SSD1306 OLED Display.
- **Embedded Firmware**: Strict non-blocking cyclic-executive loop design with a ~10ms execution cycle.
- **EMG Controller State Machine**: Flex/relax validation logic with hysteresis thresholds (650 flex, 580 relax) and a 5-second software-based cooldown.
- **Ultrasonic Distance to Volume Mapping**: Hands-free linear volume scaling ($5\text{ cm} \rightarrow \text{volume } 30$, $40\text{ cm} \rightarrow \text{volume } 5$) with a 30ms non-blocking timeout.
- **Two-way Serial Protocol**: Comma-separated status packets sent every 100ms and single-character control commands (`T`, `N`, `P`, `M`, `U`, and numeric tracks).
- **PyQt6 Desktop Application**: Real-time PyQt6 companion GUI with a live scrolling EMG graph, simulated signal controls, status gauges, and a visual seekbar.

### Fixed
- **Responsiveness**: Refactored blocking `pulseIn()` (no timeout) and `readStringUntil()` calls in firmware to prevent UI latency.
