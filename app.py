import sys
import random
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QListWidget, QVBoxLayout, QHBoxLayout, QFrame, QSlider,
    QGridLayout, QStackedWidget, QSizePolicy, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QTimer, QRectF, QPropertyAnimation, QEasingCurve, QPoint, pyqtSignal, pyqtProperty, QUrl
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QRadialGradient, QBrush, QPolygonF, QLinearGradient, QCursor, QPainterPath
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import pyqtgraph as pg

# --- Constants & Configuration ---
THEME_BG = "#050505"
THEME_ACCENT = "#ff0000"   # Red
THEME_ACCENT_DIM = "#440000"
THEME_GRID = "#110505"     
TEXT_COLOR = "#ffffff"
FONT_FAMILY = "Segoe UI" 

# PROFESSIONAL STYLESHEET
STYLESHEET = f"""
    QMainWindow {{
        background-color: {THEME_BG};
        border: 1px solid #333;
    }}
    QWidget {{
        font-family: '{FONT_FAMILY}';
        color: {TEXT_COLOR};
    }}
    
    QFrame[class="panel"] {{
        background-color: rgba(10, 10, 10, 0.9);
        border: 1px solid #333;
        border-radius: 4px; 
    }}
    
    /* CONTROL DECK */
    QFrame[class="deck"] {{
        background-color: rgba(20, 0, 0, 0.3);
        border-top: 2px solid {THEME_ACCENT};
        border-bottom: 2px solid {THEME_ACCENT};
    }}
    
    /* LABELS */
    QLabel[class="title"] {{
        font-size: 11px;
        font-weight: 700;
        color: #aaa;
        letter-spacing: 1px;
        text-transform: uppercase;
    }}
    
    /* BUTTONS */
    QPushButton {{
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #222, stop:1 #111);
        border: 1px solid #444;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: 700;
        color: #eee;
        font-size: 13px;
        letter-spacing: 1px;
    }}
    QPushButton:hover {{
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #333, stop:1 #222);
        border: 1px solid {THEME_ACCENT};
        color: #fff;
    }}
    QPushButton:pressed {{
        background-color: {THEME_ACCENT};
        color: #000;
    }}
    QPushButton:disabled {{
        background-color: #111;
        border: 1px solid #222;
        color: #444;
    }}
    
    /* WINDOW CONTROLS */
    QPushButton[class="win-btn"] {{
        background-color: transparent;
        border: none;
        font-size: 16px;
        color: #888;
        padding: 5px 10px;
    }}
    QPushButton[class="win-btn"]:hover {{
        background-color: #222;
        color: #fff;
    }}
    QPushButton[class="close-btn"]:hover {{
        background-color: {THEME_ACCENT};
        color: #fff;
    }}

    /* SPECIFIC BUTTONS */
    QPushButton[class="control-btn"] {{
        min-height: 40px;
        font-size: 14px;
    }}
    QPushButton[class="play-btn"] {{
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {THEME_ACCENT_DIM}, stop:1 #220000);
        border: 2px solid {THEME_ACCENT};
        min-height: 55px;
        min-width: 120px;
        font-size: 18px;
        font-weight: 900;
        color: #fff;
        border-radius: 6px;
    }}
    QPushButton[class="play-btn"]:hover {{
        background-color: {THEME_ACCENT};
        color: #000;
    }}
    
    /* SIMULATION CONTROL BUTTONS */
    QPushButton[class="sim-btn"] {{
        background-color: transparent;
        border: 1px solid #333;
        border-radius: 4px;
        padding: 4px 12px;
        color: #ccc;
        font-weight: bold;
    }}
    QPushButton[class="sim-btn"]:hover {{
        background-color: rgba(255,0,0,0.1);
        border: 1px solid {THEME_ACCENT};
        color: #fff;
    }}
    QPushButton[class="sim-btn"]:checked {{
        background-color: {THEME_ACCENT};
        border: 1px solid {THEME_ACCENT};
        color: #000;
        font-weight: bold;
    }}
    
    /* LIST WIDGET */
    QListWidget {{
        background-color: rgba(10,10,10,0.9);
        border-right: 1px solid #444;
        color: #ccc;
        outline: none;
    }}
    QListWidget::item {{
        padding: 12px;
        border-bottom: 1px solid #222;
    }}
    QListWidget::item:selected {{
        background-color: {THEME_ACCENT_DIM};
        color: #fff;
        border-left: 4px solid {THEME_ACCENT};
    }}
    
    /* PROGRESS BAR */
    QProgressBar {{
        background-color: #111;
        border: 1px solid #333;
        border-radius: 3px;
        text-align: center;
        color: transparent;
        height: 6px;
    }}
    QProgressBar::chunk {{
        background-color: {THEME_ACCENT};
        border-radius: 2px;
    }}
    
    /* SLIDER */
    QSlider::groove:horizontal {{
        border: 1px solid #333;
        height: 6px;
        background: #111;
        margin: 2px 0;
        border-radius: 3px;
    }}

    QSlider::handle:horizontal {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {THEME_ACCENT}, stop:1 #ff4444);
        border: 1px solid #ffaaaa;
        width: 14px;
        margin: -4px 0;
        border-radius: 7px;
    }}
"""

# --- Song DB Backup ---
SONG_DB = [
    {"name": "Metamorphosis", "artist": "Interworld", "duration": 141},
    {"name": "Rave", "artist": "Dxrk", "duration": 169},
    {"name": "Murder In My Mind", "artist": "Kordhell", "duration": 145}
]

# --- Custom Background ---
class TechBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.t_offset = 0

    def animate(self):
        self.t_offset += 0.2
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        
        painter.fillRect(0, 0, w, h, QColor(THEME_BG))
        
        # Grid
        pen = QPen(QColor(THEME_GRID))
        pen.setWidth(1)
        painter.setPen(pen)
        
        spacing = 80
        for i in range(0, w, spacing):
            painter.drawLine(i, 0, i, h)
        for i in range(0, h, spacing):
            painter.drawLine(0, i, w, i)
            
        # Subtle Data
        painter.setPen(Qt.PenStyle.NoPen)
        for i in range(3): 
            x = (i * 300 + self.t_offset) % w
            grad = QLinearGradient(x, 0, x, h)
            grad.setColorAt(0, QColor(255, 0, 0, 0))
            grad.setColorAt(0.5, QColor(255, 0, 0, 15))
            grad.setColorAt(1, QColor(255, 0, 0, 0))
            painter.setBrush(QBrush(grad))
            painter.drawRect(int(x), 0, 100, h)

# --- Custom Gauge ---
class AggressiveGauge(QWidget):
    def __init__(self, title, units, max_val=100, parent=None):
        super().__init__(parent)
        self.title, self.units, self.max_val = title, units, max_val
        self.current_val, self.target_val = 0, 0
        self.setMinimumSize(220, 220)

    def set_value(self, val):
        self.target_val = max(0, min(self.max_val, val))
        
    def update_anim(self):
        diff = self.target_val - self.current_val
        if abs(diff) < 0.1:
            self.current_val = float(self.target_val)
        else:
            self.current_val += diff * 0.15
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        side = min(w, h)
        
        painter.translate(w / 2, h / 2)
        painter.scale(side / 220.0, side / 220.0)

        # Background Ring (Dashed Arc)
        pen_bg = QPen(QColor(THEME_ACCENT_DIM))
        pen_bg.setWidth(6)
        pen_bg.setStyle(Qt.PenStyle.DashLine)
        pen_bg.setCapStyle(Qt.PenCapStyle.FlatCap)
        painter.setPen(pen_bg)
        start_angle = 225 * 16
        span_angle = -270 * 16
        painter.drawArc(QRectF(-90, -90, 180, 180), start_angle, span_angle)

        # Value Arc
        pen_val = QPen(QColor(THEME_ACCENT))
        pen_val.setWidth(14)
        pen_val.setCapStyle(Qt.PenCapStyle.FlatCap) 
        painter.setPen(pen_val)
        
        # Determine actual max so it fills up to 100% when current_val == max_val
        pct = min(1.0, max(0.0, self.current_val / self.max_val))
        value_span = -270 * pct * 16 # Full span is -270 degrees
        painter.drawArc(QRectF(-85, -85, 170, 170), int(start_angle), int(value_span))

        # Text
        painter.setPen(QColor(TEXT_COLOR))
        font_val = QFont(FONT_FAMILY, 36, QFont.Weight.Bold)
        painter.setFont(font_val)
        
        # Explicit rounding to avoid 39.99 converting to 39 via int() flooring
        display_val = f"{int(round(self.current_val))}"
        if self.title == "DISTANCE" and self.current_val >= 60:
             display_val = "> 60"
             font_val.setPointSize(28) 
             painter.setFont(font_val)

        painter.drawText(QRectF(-100, -25, 200, 50), Qt.AlignmentFlag.AlignCenter, display_val)
        
        painter.setPen(QColor("#888"))
        font_unit = QFont(FONT_FAMILY, 12)
        painter.setFont(font_unit)
        painter.drawText(QRectF(-100, 25, 200, 30), Qt.AlignmentFlag.AlignCenter, self.units)
        
        painter.setPen(QColor(THEME_ACCENT))
        font_title = QFont(FONT_FAMILY, 10, QFont.Weight.Bold)
        painter.setFont(font_title)
        painter.drawText(QRectF(-100, 60, 200, 30), Qt.AlignmentFlag.AlignCenter, self.title)

# --- Custom Toggle (Squircle) ---
class TechToggle(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, left_text="SIM", right_text="HARDWARE", parent=None):
        super().__init__(parent)
        self.left_text = left_text
        self.right_text = right_text
        self.setFixedSize(160, 40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._checked = False
        self._thumb_x = 4
        self._anim = QPropertyAnimation(self, b"thumb_x", self)
        self._anim.setDuration(250)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.disabled_mode = False

    @pyqtProperty(float)
    def thumb_x(self):
        return self._thumb_x

    @thumb_x.setter
    def thumb_x(self, val):
        self._thumb_x = val
        self.update()

    def setChecked(self, checked):
        if self.disabled_mode: return
        self._checked = checked
        # End value is 0 (Sim) or width/2 (Hardware)
        end = self.width() / 2 if checked else 0
        self._anim.stop()
        self._anim.setEndValue(end)
        self._anim.start()
        self.toggled.emit(checked)
        self.update()

    def set_disabled_mode(self, disabled):
        self.disabled_mode = disabled
        self.setCursor(Qt.CursorShape.ForbiddenCursor if disabled else Qt.CursorShape.PointingHandCursor)
        self.update()

    def isChecked(self):
        return self._checked

    def mousePressEvent(self, event):
        if self.disabled_mode: return
        if event.button() == Qt.MouseButton.LeftButton:
            self.setChecked(not self._checked)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Track Colors
        if self.disabled_mode:
            bg_col = QColor("#111")
            text_l = QColor("#333")
            text_r = QColor("#333")
        elif self._checked:
            bg_col = QColor(THEME_ACCENT_DIM)
            text_l = QColor("#444")
            text_r = QColor("#fff")
        else:
            bg_col = QColor("#222")
            text_l = QColor("#fff")
            text_r = QColor("#444")

        # Draw Track (Squircle)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)
        p.fillPath(path, bg_col)
        
        # Draw Sliding Panel (Thumb) - Now rectangular/squircle
        thumb_col = QColor("#444") if self.disabled_mode else QColor(THEME_ACCENT)
        thumb_path = QPainterPath()
        # Thumb covers exactly half the width
        thumb_path.addRoundedRect(self._thumb_x, 0, self.width()/2, self.height(), 20, 20)
        p.fillPath(thumb_path, thumb_col)
        
        p.setPen(QPen(QColor("#333"), 1))
        p.drawPath(path)
        
        # Draw Text (Layered)
        font = QFont(FONT_FAMILY, 9, QFont.Weight.Bold)
        p.setFont(font)
        
        # Logic: Text color depends on overlap with thumb? 
        # Simpler: Just use high contrast.
        
        # Left Label
        if self._checked: p.setPen(QColor("#666")) # Inactive
        else: p.setPen(QColor("#fff"))            # Active (White on Red)
        p.drawText(QRectF(0, 0, self.width()/2, self.height()), Qt.AlignmentFlag.AlignCenter, self.left_text)
        
        # Right Label
        if self._checked: p.setPen(QColor("#fff")) # Active (White on Red)
        else: p.setPen(QColor("#666"))            # Inactive
        p.drawText(QRectF(self.width()/2, 0, self.width()/2, self.height()), Qt.AlignmentFlag.AlignCenter, self.right_text)

# --- App Logic ---
class NeuroSimulator:
    def __init__(self):
        self.time_step = 0
        self.is_flexed = False
        self.flex_duration, self.flex_cooldown = 0, 0
        
        self.sim_state = "PAUSED"
        self.sim_song = 0
        self.sim_time = 0
        
        # Interactive Manual Controls
        self.manual_mode = False
        self.manual_flex = False
        self.manual_dist = 20

    def get_data(self):
        self.time_step += 0.1
        
        if not self.manual_mode:
            # --- AUTO SIMULATION ---
            # Flex cooldown prevents constant twitching
            if self.flex_cooldown > 0: 
                self.flex_cooldown -= 1
            elif random.random() < 0.01: # Rare spike ~ every few seconds
                self.is_flexed = True
                self.flex_duration = random.randint(10, 20) # Very narrow/sharp spike width
            
            if self.flex_duration > 0:
                self.flex_duration -= 1
                if self.flex_duration == 0:
                    self.is_flexed = False
                    self.flex_cooldown = 200 # 5-second cooldown in loop cycles
                    
                    if self.sim_state == "PLAYING":
                        self.sim_state = "PAUSED"
                    else:
                        self.sim_state = "PLAYING"
            
            emg_val = random.randint(670, 800) if self.is_flexed else random.randint(540, 580)
            dist_base = 25 + (math.sin(self.time_step * 0.3) * 10)
            dist = max(5, min(45, dist_base + random.uniform(-0.5, 0.5)))
        else:
            # --- MANUAL SIMULATION ---
            # Emg follows explicit button toggle
            emg_val = random.randint(670, 800) if self.manual_flex else random.randint(540, 580)
            dist = self.manual_dist
                
            # If the state transitioned from Flex -> Relax this cycle, toggle play/pause
            if self.is_flexed and not self.manual_flex:
                if self.sim_state == "PLAYING":
                    self.sim_state = "PAUSED"
                else:
                    self.sim_state = "PLAYING"
            self.is_flexed = self.manual_flex
            
        if self.sim_state == "PLAYING":
            self.sim_time += 0.1
            if self.sim_time > SONG_DB[self.sim_song]["duration"]:
                self.sim_time = 0
                self.sim_song = (self.sim_song + 1) % len(SONG_DB)
        
        # Old vol was specifically mapping for Simulation audio, we handle volume mapping primarily in update_dashboard now, 
        # but let's just make it cleanly map 0-100 right here for the data packet.
        vol = max(0, min(100, int(map_val(dist, 0, 40, 100, 0))))
        
        return {
            "emg": emg_val, 
            "distance": round(dist, 1), 
            "volume": vol,
            "flexed": self.is_flexed,
            "state": self.sim_state,
            "song": self.sim_song,
            "time": int(self.sim_time)
        }

def map_val(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# --- Serial Worker (Hardware Integration) ---
from PyQt6.QtCore import QThread, pyqtSignal
try:
    import serial
    import serial.tools.list_ports
    HAS_SERIAL = True
except ImportError:
    HAS_SERIAL = False

class SerialWorker(QThread):
    data_received = pyqtSignal(dict)
    connection_status = pyqtSignal(bool, str)

    def __init__(self, port=None, baud=9600):
        super().__init__()
        self.port = port
        self.baud = baud
        self.running = True
        self.serial_conn = None

    def run(self):
        if not self.port:
            ports = list(serial.tools.list_ports.comports())
            arduino_ports = [p.device for p in ports if "Arduino" in p.description or "CH340" in p.description or "USB" in p.description]
            if not arduino_ports:
                 if ports:
                     self.port = ports[0].device
                 else:
                     self.connection_status.emit(False, "NO DEVICES FOUND")
                     return
            else:
                self.port = arduino_ports[0]

        try:
            self.serial_conn = serial.Serial(self.port, self.baud, timeout=1)
            self.connection_status.emit(True, f"CONNECTED: {self.port}")
        except Exception as e:
            self.connection_status.emit(False, str(e))
            return

        while self.running and self.serial_conn.is_open:
            try:
                if self.serial_conn.in_waiting:
                    line = self.serial_conn.readline().decode('utf-8').strip()
                    if line and "EMG:" in line and "TIME:" in line:
                        # Parse: EMG:532|DIST:14|VOL:22|STATE:PLAYING|SONG:1|TIME:42
                        try:
                            parts = line.split("|")
                            data = {}
                            for p in parts:
                                k, v = p.split(":")
                                if k in ["EMG", "DIST", "VOL", "SONG", "TIME"]:
                                    data[k.lower()] = int(v)
                                else:
                                    data[k.lower()] = v
                            
                            # Normalize key for app compat
                            data["distance"] = data.pop("dist")
                            data["volume"] = data.pop("vol")
                            data["flexed"] = data["emg"] > 650
                            
                            self.data_received.emit(data)
                        except Exception as e:
                            print(f"Data parse error: {e}")
            except (serial.SerialException, OSError) as e:
                print(f"Serial Disconnected: {e}")
                self.connection_status.emit(False, "DISCONNECTED")
                break
            except Exception as e:
                print(f"Serial Error: {e}")
                pass # Ignore random parse errors
            self.msleep(5)
        
        if self.serial_conn:
            self.serial_conn.close()

    def send_command(self, cmd: str):
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write(f"{cmd}\n".encode('utf-8'))
            except Exception as e:
                print(f"Failed to send command {cmd}: {e}")

    def stop(self):
        self.running = False
        self.wait()

class EMGMusicApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # 1. Frameless Window Hint
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.resize(1300, 950)
        self.setStyleSheet(STYLESHEET)
        
        self.bg = TechBackground(self)
        self.bg.resize(1300, 950)
        self.bg.lower()
        
        # State
        self.is_muted = False
        self.is_hardware_available = False # Can we connect?
        self.force_sim_mode = False        # User overrides to Sim

        # --- AUDIO SIMULATION ---
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.5)

        # Data
        self.x_data, self.y_data = list(range(300)), [0] * 300
        self.sim = NeuroSimulator()
        
        self.init_ui()
        
        # Serial Init
        if HAS_SERIAL:
            self.serial_thread = SerialWorker()
            self.serial_thread.data_received.connect(self.update_from_serial)
            self.serial_thread.connection_status.connect(self.on_serial_status)
            self.serial_thread.start()
        else:
            self.status.setText("SERIAL LIBRARY MISSING")
            self.btn_mode.setDisabled(True)
            self.btn_mode.setToolTip("Hardware Not Detected")

        self.timer = QTimer()
        self.timer.timeout.connect(self.loop_ui)
        self.timer.start(20)
        
        # Win Drag & Resize
        self.old_pos = None
        self.resize_mode = None
        self.MARGIN = 10
        self.setMouseTracking(True) # Required for hover detection

    def create_label(self, text, class_name):
        lbl = QLabel(text)
        lbl.setProperty("class", class_name)
        return lbl
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Native Resize Logic
            edges = Qt.Edge(0)
            pos = event.position()
            w, h = self.width(), self.height()
            
            if pos.x() < self.MARGIN: edges |= Qt.Edge.LeftEdge
            if pos.x() > w - self.MARGIN: edges |= Qt.Edge.RightEdge
            if pos.y() < self.MARGIN: edges |= Qt.Edge.TopEdge
            if pos.y() > h - self.MARGIN: edges |= Qt.Edge.BottomEdge
            
            # If we are on an edge, resize.
            if edges != Qt.Edge(0):
                if self.windowHandle():
                    self.windowHandle().startSystemResize(edges)
            # If we are in the title bar (and NOT on an edge), move.
            elif pos.y() < 40:
                if self.windowHandle():
                    self.windowHandle().startSystemMove()

    def mouseMoveEvent(self, event):
        # Hover Detection (Set Cursor)
        pos = event.position()
        w, h = self.width(), self.height()
        
        # Check edges
        left = pos.x() < self.MARGIN
        right = pos.x() > w - self.MARGIN
        top = pos.y() < self.MARGIN
        bottom = pos.y() > h - self.MARGIN
        
        if left and top: self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif right and bottom: self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif right and top: self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif left and bottom: self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif left or right: self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif top or bottom: self.setCursor(Qt.CursorShape.SizeVerCursor)
        else: self.setCursor(Qt.CursorShape.ArrowCursor)

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def resizeEvent(self, event):
        self.bg.resize(self.width(), self.height())
        super().resizeEvent(event)

    def on_serial_status(self, connected, msg):
        self.is_hardware_available = connected
        if connected:
            self.status.setText(msg)
            self.status.setStyleSheet(f"color: {THEME_ACCENT}; font-size: 14px; font-weight: 700;")
            self.btn_mode.set_disabled_mode(False)
            self.btn_mode.setChecked(True) # Auto-switch to HW
            self.sim_controls.hide() # Hide Manual UI
            # Hardware controls playback, so pause simulation audio
            self.player.pause()
        else:
            self.status.setText(f"SIMULATION MODE ({msg})")
            self.status.setStyleSheet("color: #666; font-size: 14px; font-weight: 700;")
            self.btn_mode.setChecked(False)
            self.btn_mode.set_disabled_mode(True)
            self.sim_controls.show() # Show Manual UI

    def toggle_mode(self, checked):
        if not self.is_hardware_available: return
        self.force_sim_mode = not checked
        if not checked:
            self.status.setText("SIMULATION MODE (USER OVERRIDE)")
            self.sim_controls.show()
        else:
            self.status.setText("HARDWARE CONNECTED")
            self.sim_controls.hide()
            self.player.pause() # Stop Sim audio

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def update_from_serial(self, d):
        if not self.force_sim_mode:
            self.update_dashboard(d, source="HW")

    def loop_ui(self):
        self.bg.animate()
        # If simulation (either forced or no hardware)
        if self.force_sim_mode or not self.is_hardware_available:
            d = self.sim.get_data()
            self.update_dashboard(d, source="SIM")

    def update_dashboard(self, d, source="SIM"):
        # Explicit math float rounding to avoid 99% or 39cm rounding bugs
        dist = max(0.0, min(40.0, float(d['distance'])))
        vol = max(0, min(100, int(round((40.0 - dist) * 2.5))))
        
        self.g_vol.set_value(vol)
        self.g_vol.update_anim()
        
        # We explicitly round distance so the display can natively hit 40 cleanly instead of 39.8 etc
        self.g_dist.set_value(int(round(dist)))
        self.g_dist.update_anim()
        
        # Audio Volume Sync for Simulation
        if source == "SIM" and not self.is_muted:
            # vol is 0-100. QAudioOutput uses 0.0-1.0 linear volume
            self.audio_output.setVolume(vol / 100.0)
        
        # Update UI Labels from State
        if "state" in d:
            if d["state"] == "PLAYING":
                self.btn_play.setText("PAUSE")
                self.btn_play.setStyleSheet(f"background-color: {THEME_ACCENT}; color: #000;")
                self.status.setText(f"PLAYING [{source}]")
                if source == "SIM" and self.player.playbackState() != QMediaPlayer.PlaybackState.PlayingState:
                    self._play_sim_audio(d.get("song", 0))
            else:
                self.btn_play.setText("PLAY")
                self.btn_play.setStyleSheet("")
                if source == "HW": self.status.setText("HARDWARE CONNECTED")
                else: self.status.setText("SYSTEM READY (SIM)")
                if source == "SIM": self.player.pause()
                
        # Update Song Meta
        if "song" in d:
            s_idx = d["song"]
            if 0 <= s_idx < len(SONG_DB):
                song = SONG_DB[s_idx]
                self.lbl_song_title.setText(song["name"].upper())
                self.lbl_song_artist.setText(song["artist"].upper())
                
                # Fetch time
                # In HW mode, we use Arduino's 'time'
                # In OS Simulation mode, we use real QMediaPlayer time
                if source == "SIM":
                    cur_sec = self.player.position() // 1000
                    self.sim.sim_time = cur_sec # Sync visual simulator timer to actual media
                else:
                    cur_sec = d.get("time", 0)
                    
                tot_sec = song["duration"]
                
                cm, cs = cur_sec // 60, cur_sec % 60
                tm, ts = tot_sec // 60, tot_sec % 60
                
                self.lbl_time.setText(f"{cm:02d}:{cs:02d} / {tm:02d}:{ts:02d}")
                
                # Seekbar
                pct = int((cur_sec / tot_sec) * 100) if tot_sec > 0 else 0
                self.progress_bar.setValue(min(100, max(0, pct)))

        if self.g_box.isVisible():
            raw = d["emg"]
            
            # Since baseline is now ~560 and max is ~800:
            # Shift the visual baseline down so it sits at the bottom of the graph.
            # E.g. raw=560 -> val=0. raw=800 -> val=240
            # Then amplify it so the spike looks huge.
            baseline = 550 
            val = (raw - baseline) * 3.5 
            if val < 0: val = 0
            
            self.y_data = self.y_data[1:] + [val]
            self.curve.setData(self.x_data, self.y_data)
            
            # Update TOP-RIGHT Value Overlay
            self.lbl_graph_val.setText(f"EMG RAW: {raw}")

    def closeEvent(self, event):
        if hasattr(self, 'serial_thread'):
            self.serial_thread.stop()
        self.player.stop()
        super().closeEvent(event)

    def _play_sim_audio(self, index):
        """Internal helper for Simulation mode audio loading/playing."""
        if not (0 <= index < len(SONG_DB)): return
        song = SONG_DB[index]
        filename = f"{song['name']}.mp3"
        import os
        path = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(path):
            # Only set source if it's different to avoid restarting
            url = QUrl.fromLocalFile(path)
            if self.player.source() != url:
                self.player.setSource(url)
            self.player.play()
        else:
            print(f"File not found for simulation: {path}")

    # --- CONTROL BUTTON HANDLERS ---
    def on_play_pause(self):
        if self.is_hardware_available and not self.force_sim_mode:
            self.serial_thread.send_command("T")
        else:
            # Simulate Arduino Toggle
            self.sim.sim_state = "PAUSED" if self.sim.sim_state == "PLAYING" else "PLAYING"

    def on_next(self):
        if self.is_hardware_available and not self.force_sim_mode:
            self.serial_thread.send_command("N")
        else:
            self.sim.sim_song = (self.sim.sim_song + 1) % len(SONG_DB)
            self.player.stop() # Force restart track
            self._play_sim_audio(self.sim.sim_song)
            self.sim.sim_state = "PLAYING"

    def on_prev(self):
        if self.is_hardware_available and not self.force_sim_mode:
            self.serial_thread.send_command("P")
        else:
            self.sim.sim_song = (self.sim.sim_song - 1) % len(SONG_DB)
            self.player.stop()
            self._play_sim_audio(self.sim.sim_song)
            self.sim.sim_state = "PLAYING"

    def on_mute(self):
        self.is_muted = not self.is_muted
        if self.is_muted:
            self.btn_mute.setText("MUTED")
            self.btn_mute.setStyleSheet(f"color: {THEME_ACCENT}; border: 1px solid {THEME_ACCENT};")
            if self.is_hardware_available and not self.force_sim_mode:
                self.serial_thread.send_command("M")
            else:
                self.audio_output.setMuted(True)
        else:
            self.btn_mute.setText("UNMUTED")
            self.btn_mute.setStyleSheet("")
            if self.is_hardware_available and not self.force_sim_mode:
                self.serial_thread.send_command("U") # Requires 'U' logic on arduino to restore to dist level!
            else:
                self.audio_output.setMuted(False)

    def on_library_click(self, item):
        idx = self.playlist.row(item)
        if idx >= len(SONG_DB): return # Map to actual DB only
        if self.is_hardware_available and not self.force_sim_mode:
            self.serial_thread.send_command(f"S{idx}")
        else:
            self.sim.sim_song = idx
            self.player.stop()
            self._play_sim_audio(idx)
            self.sim.sim_state = "PLAYING"

    def on_sim_type_toggle(self, checked):
        # Checked = Auto, Unchecked = Manual
        self.sim.manual_mode = not checked
        
    def on_sim_dist_toggle(self, checked):
        target_w = 180 if checked else 0
        self.dist_anim = QPropertyAnimation(self.slider_dist, b"maximumWidth")
        self.dist_anim.setDuration(300)
        self.dist_anim.setEndValue(target_w)
        self.dist_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.dist_anim.valueChanged.connect(lambda x: self.slider_dist.setFixedWidth(x))
        self.dist_anim.start()

    def on_sim_flex(self, flexed):
        self.sim.manual_flex = flexed
        # Stylings are handled by CSS :checked

    def on_sim_dist_change(self, val):
        self.sim.manual_dist = val

    def init_ui(self):
        main = QWidget()
        self.setCentralWidget(main)
        main_layout = QVBoxLayout(main) # Main is now Vertical (Header + Content)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        
        # --- TITLE BAR (Frameless Custom) ---
        title_bar = QFrame()
        title_bar.setStyleSheet(f"background-color: {THEME_BG}; border-bottom: 1px solid #333;")
        title_bar.setFixedHeight(40)
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(15, 0, 0, 0)
        
        app_icon = QLabel("///")
        app_icon.setStyleSheet(f"color: {THEME_ACCENT}; font-weight: 900;")
        app_title = QLabel("EMG MUSIC CONTROLLER")
        app_title.setStyleSheet("color: #ccc; font-weight: 700; letter-spacing: 1px;")
        
        min_btn = QPushButton("_")
        min_btn.setProperty("class", "win-btn")
        min_btn.clicked.connect(self.showMinimized)
        
        max_btn = QPushButton("[]")
        max_btn.setProperty("class", "win-btn")
        max_btn.clicked.connect(self.toggle_maximize)

        close_btn = QPushButton("X")
        close_btn.setProperty("class", "win-btn")
        close_btn.setProperty("class", "close-btn") # Add extra class for hover red
        close_btn.clicked.connect(self.close)
        
        tb_layout.addWidget(app_icon)
        tb_layout.addSpacing(10)
        tb_layout.addWidget(app_title)
        tb_layout.addStretch()
        tb_layout.addWidget(min_btn)
        tb_layout.addWidget(max_btn)
        tb_layout.addWidget(close_btn)
        
        main_layout.addWidget(title_bar)
        
        # --- APP WRAPPER (Sidebar + Content) ---
        wrapper = QWidget()
        wrapper_layout = QHBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0,0,0,0)
        wrapper_layout.setSpacing(0)
        
        # --- SIDEBAR ---
        self.sidebar = QWidget()
        self.sidebar.setStyleSheet(f"background-color: {THEME_BG}; border-right: 1px solid #333;")
        self.sidebar.setFixedWidth(0)
        
        side_layout = QVBoxLayout(self.sidebar)
        side_layout.addWidget(self.create_label("MUSIC LIBRARY", "title"))
        self.playlist = QListWidget()
        # Ensure library matches exactly our DB
        for s in SONG_DB:
            self.playlist.addItem(f"{s['name']} - {s['artist']}")
        self.playlist.itemClicked.connect(self.on_library_click)

        side_layout.addWidget(self.playlist)
        wrapper_layout.addWidget(self.sidebar)
        
        # --- CONTENT AREA ---
        content = QWidget()
        c_layout = QVBoxLayout(content)
        c_layout.setContentsMargins(40, 20, 40, 30)
        c_layout.setSpacing(15)
        
        # 1. HEADER ROW (Lib + Mode Swtich + Status)
        header = QHBoxLayout()
        self.btn_lib_top = QPushButton("☰ LIBRARY")
        self.btn_lib_top.clicked.connect(self.toggle_sidebar)
        
        self.btn_mode = TechToggle()
        self.btn_mode.toggled.connect(self.toggle_mode)
        
        self.status = QLabel("SYSTEM INITIALIZING...")
        self.status.setStyleSheet("color: #666; font-size: 14px; font-weight: 700;")
        
        header.addWidget(self.btn_lib_top)
        header.addSpacing(20)
        header.addWidget(self.btn_mode)
        header.addSpacing(20)
        header.addWidget(self.status)
        header.addStretch()
        
        # --- NEW MANUAL CONTROLS OVERLAY ---
        self.sim_controls = QFrame()
        self.sim_controls.setObjectName("sim_panel")
        self.sim_controls.setFixedHeight(45)
        self.sim_controls.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.sim_controls.setStyleSheet(f"#sim_panel {{ background-color: rgba(20,0,0,0.5); border: 1px solid {THEME_ACCENT_DIM}; border-radius: 4px; }}")
        s_layout = QHBoxLayout(self.sim_controls)
        s_layout.setContentsMargins(10, 0, 10, 0)
        s_layout.setSpacing(10)
        
        lbl_sc = QLabel("SIM OVERRIDE:")
        lbl_sc.setStyleSheet("font-weight: bold; color: #aaa; font-size: 11px; background: transparent; border: none;")
        
        self.btn_sim_auto = TechToggle(left_text="MANUAL", right_text="AUTO")
        self.btn_sim_auto.setChecked(True) # True = Auto, False = Manual
        self.btn_sim_auto.toggled.connect(self.on_sim_type_toggle)
        
        self.btn_sim_baseline = QPushButton("BASELINE")
        self.btn_sim_flex = QPushButton("FLEX")
        self.btn_sim_baseline.setProperty("class", "sim-btn")
        self.btn_sim_flex.setProperty("class", "sim-btn")
        
        self.btn_sim_baseline.setCheckable(True)
        self.btn_sim_flex.setCheckable(True)
        self.btn_sim_baseline.setAutoExclusive(True)
        self.btn_sim_flex.setAutoExclusive(True)
        self.btn_sim_baseline.setChecked(True)
        self.btn_sim_baseline.toggled.connect(lambda checked: self.on_sim_flex(not checked))
        
        self.btn_dist_toggle = QPushButton("DIST")
        self.btn_dist_toggle.setProperty("class", "sim-btn")
        self.btn_dist_toggle.setCheckable(True)
        self.btn_dist_toggle.toggled.connect(self.on_sim_dist_toggle)
        
        self.slider_dist = QSlider(Qt.Orientation.Horizontal)
        self.slider_dist.setRange(0, 40)
        self.slider_dist.setValue(20)
        self.slider_dist.setFixedWidth(0) # Starts collapsed
        self.slider_dist.valueChanged.connect(self.on_sim_dist_change)
        
        s_layout.addWidget(lbl_sc)
        s_layout.addWidget(self.btn_sim_auto)
        s_layout.addSpacing(15)
        s_layout.addWidget(self.btn_sim_baseline)
        s_layout.addWidget(self.btn_sim_flex)
        s_layout.addSpacing(10)
        s_layout.addWidget(self.btn_dist_toggle)
        s_layout.addWidget(self.slider_dist)
        
        header.addWidget(self.sim_controls)
        
        c_layout.addLayout(header)
        
        # 2. GAUGES
        gauges = QHBoxLayout()
        gauges.setContentsMargins(0, 10, 0, 10)
        self.g_vol = AggressiveGauge("VOLUME", "%", 100)
        self.g_dist = AggressiveGauge("DISTANCE", "CM", 40)
        gauges.addStretch()
        gauges.addWidget(self.g_vol)
        gauges.addSpacing(150)
        gauges.addWidget(self.g_dist)
        gauges.addStretch()
        c_layout.addLayout(gauges)
        
        # 3. GRAPH (Above Controls)
        self.g_box = QFrame()
        self.g_box.setProperty("class", "panel")
        self.g_box.setFixedHeight(200)
        self.g_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # Graph Layout Overlay
        g_lyt = QGridLayout(self.g_box) # Use Grid to layer widgets
        g_lyt.setContentsMargins(0,0,0,0)
        
        # Plot
        self.plot = pg.PlotWidget()
        self.plot.setBackground(THEME_BG)
        self.plot.showAxis('left', False)
        self.plot.showAxis('bottom', False)
        
        # Lock Y-Axis so it doesn't auto-scale during flatlines
        self.plot.setYRange(0, 800, padding=0)
        
        self.curve = self.plot.plot(self.x_data, self.y_data, pen=pg.mkPen(THEME_ACCENT, width=2), brush=(255,0,0,30), fillLevel=0)
        g_lyt.addWidget(self.plot, 0, 0)
        
        # Overlay Value Label (Top Right)
        self.lbl_graph_val = QLabel("EMG RAW: --")
        self.lbl_graph_val.setStyleSheet("background-color: rgba(0,0,0,0.7); color: #fff; font-weight: 900; padding: 5px; border-bottom-left-radius: 5px;")
        g_lyt.addWidget(self.lbl_graph_val, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        
        c_layout.addWidget(self.g_box)
        
        from PyQt6.QtWidgets import QProgressBar
        
        # 4. COMMAND DECK (Bottom)
        deck = QFrame()
        deck.setProperty("class", "deck") 
        d_layout = QVBoxLayout(deck)
        d_layout.setContentsMargins(40, 20, 40, 20)
        
        # --- PLAYER METADATA UI ---
        meta_layout = QHBoxLayout()
        
        self.lbl_song_title = self.create_label("WAITING FOR DATA", "title")
        self.lbl_song_title.setStyleSheet("font-size: 18px; color: #fff;")
        
        self.lbl_song_artist = self.create_label("...", "title")
        self.lbl_song_artist.setStyleSheet(f"font-size: 12px; color: {THEME_ACCENT};")
        
        self.lbl_time = self.create_label("00:00 / 00:00", "title")
        self.lbl_time.setStyleSheet("font-size: 14px; color: #888; font-family: monospace;")
        
        info_col = QVBoxLayout()
        info_col.addWidget(self.lbl_song_title)
        info_col.addWidget(self.lbl_song_artist)
        
        meta_layout.addLayout(info_col)
        meta_layout.addStretch()
        meta_layout.addWidget(self.lbl_time, 0, Qt.AlignmentFlag.AlignBottom)
        
        d_layout.addLayout(meta_layout)
        
        # Seekbar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(0)
        d_layout.addWidget(self.progress_bar)
        
        d_layout.addSpacing(15)
        
        # Controls Row
        ctrls = QHBoxLayout()
        self.btn_lib_deck = QPushButton("LIBRARY")
        self.btn_lib_deck.setProperty("class", "control-btn")
        self.btn_lib_deck.clicked.connect(self.toggle_sidebar)
        
        self.btn_mute = QPushButton("UNMUTED")
        self.btn_mute.setProperty("class", "control-btn")
        self.btn_mute.clicked.connect(self.on_mute)
        
        self.btn_prev = QPushButton("PREV")
        self.btn_prev.setProperty("class", "control-btn")
        self.btn_prev.clicked.connect(self.on_prev)

        self.btn_play = QPushButton("PLAY")
        self.btn_play.setProperty("class", "play-btn")
        self.btn_play.clicked.connect(self.on_play_pause)

        self.btn_next = QPushButton("NEXT")
        self.btn_next.setProperty("class", "control-btn")
        self.btn_next.clicked.connect(self.on_next)
        
        self.btn_graph = QPushButton("GRAPH ON")
        self.btn_graph.setCheckable(True)
        self.btn_graph.setChecked(True)
        self.btn_graph.setProperty("class", "control-btn")
        self.btn_graph.clicked.connect(self.toggle_graph)
        
        ctrls.addWidget(self.btn_lib_deck)
        ctrls.addWidget(self.btn_mute)
        ctrls.addSpacing(40)
        ctrls.addWidget(self.btn_prev)
        ctrls.addWidget(self.btn_play)
        ctrls.addWidget(self.btn_next)
        ctrls.addSpacing(40)
        ctrls.addWidget(self.btn_graph)
        d_layout.addLayout(ctrls)
        
        c_layout.addWidget(deck)
        wrapper_layout.addWidget(content)
        main_layout.addWidget(wrapper)

    def toggle_graph(self, checked):
        if checked: 
            self.g_box.show()
            self.btn_graph.setText("GRAPH ON")
            self.resize(self.width(), self.height() + 200)
        else: 
            self.g_box.hide()
            self.btn_graph.setText("GRAPH OFF")
            self.resize(self.width(), self.height() - 200)

    def toggle_sidebar(self):
        end = 350 if self.sidebar.width() == 0 else 0
        self.anim = QPropertyAnimation(self.sidebar, b"maximumWidth")
        self.anim.setDuration(300)
        self.anim.setEndValue(end)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.valueChanged.connect(lambda x: self.sidebar.setFixedWidth(x))
        self.anim.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EMGMusicApp()
    window.show()
    sys.exit(app.exec())
