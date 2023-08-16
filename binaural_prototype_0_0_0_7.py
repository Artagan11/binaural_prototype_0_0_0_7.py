import numpy as np
import sounddevice as sd
import threading
import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QPushButton, QInputDialog, QMessageBox, QTextEdit
from PyQt5.QtCore import Qt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Configure logging
logging.basicConfig(filename='binaural_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from PyQt5.QtWidgets import QTextEdit

class LogViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.logTextEdit = QTextEdit(self)
        self.logTextEdit.setReadOnly(True)
        self.setCentralWidget(self.logTextEdit)
        self.loadLogs()

    def loadLogs(self):
        with open('binaural_log.log', 'r') as file:
            self.logTextEdit.setText(file.read())

# Global base frequency
global_base_frequency = 73  # Set the base frequency to 73 Hz
stop_tone = False

import numpy as np

class BinauralBeatGenerator:
    def __init__(self):
        pass

    def play_binaural_beat(self, beat_frequency, duration):
        global stop_tone
        stop_tone = False

        fs = 44100  # Sampling frequency
        left_freq = global_base_frequency  # Frequency for left ear
        right_freq = global_base_frequency + beat_frequency  # Frequency for right ear

        t = np.arange(0, duration * 60, 1/fs)  # Time array for given duration in minutes
        left_wave = np.cos(2 * np.pi * left_freq * t)
        right_wave = np.cos(2 * np.pi * right_freq * t)

        stereo_wave = np.column_stack((left_wave, right_wave)).astype(np.float32)

        with sd.OutputStream(samplerate=fs, channels=2, blocksize=1024) as stream:
            for i in range(0, len(stereo_wave), fs):
                if stop_tone:
                    break
                chunk = stereo_wave[i:i + fs]  # Send one second of audio at a time
                stream.write(chunk)

    def stop_binaural_beat(self):
        global stop_tone
        stop_tone = True
        logging.info('Stopping binaural beat.')            

    def play_solfeggio_frequency(self, frequency, duration):
        global stop_tone
        stop_tone = False

        fs = 44100  # Sampling frequency

        t = np.arange(0, duration * 60, 1/fs)  # Time array for given duration in minutes
        wave = np.cos(2 * np.pi * frequency * t)
        stereo_wave = np.column_stack((wave, wave)).astype(np.float32)  # Create stereo sound

        with sd.OutputStream(samplerate=fs, channels=2, blocksize=1024) as stream:
            for i in range(0, len(stereo_wave), fs):
                if stop_tone:
                    break
                chunk = stereo_wave[i:i + fs]  # Send one second of audio at a time
                stream.write(chunk)

class UserProfile:
    PROFILES = {
        "CaptainKirk": 28,
        "Spock": 37,
        "McCoy": 19,
        "Exploration": 4,  # Default frequency for Exploration profile
    }

    def load_profile(self, user_name):
        logging.info(f'Loading profile for user: {user_name}')
        return UserProfile.PROFILES.get(user_name, UserProfile.PROFILES["Exploration"])


class FeedbackMechanism:
    def submit_feedback(self, feedback):
        logging.info(f'Submitting feedback: {feedback}')
        pass

class PredictiveEngine:
    def __init__(self, user_data):
        self.user_data = user_data
        self.model = None

    def train_model(self):
        features, labels = self.prepare_data()
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)
        self.model = RandomForestRegressor()
        self.model.fit(X_train, y_train)
        logging.info('Training predictive model.')

    def prepare_data(self):
        pass

    def predict(self, input_data):
        return self.model.predict(input_data)

class SessionManagement:
    def start_session(self, session_type):
        logging.info(f'Starting session of type: {session_type}')
        pass

    def stop_session(self):
        logging.info('Stopping session.')
        pass

class BinauralBeatExplorerUI(QMainWindow):
    def __init__(self, beat_generator, user_profile, feedback_mechanism, predictive_engine, session_management):
        super().__init__()
        self.beat_generator = beat_generator
        self.user_profile = user_profile
        self.feedback_mechanism = feedback_mechanism
        self.predictive_engine = predictive_engine
        self.session_management = session_management
        self.initUI()

    def initUI(self):
        # Main layout
        mainLayout = QVBoxLayout()

        # Binaural Beats Slider
        binauralSliderLayout = QHBoxLayout()
        binauralLabel = QLabel('Binaural Beats Frequency (Hz):')
        self.binauralFrequencySlider = QSlider(Qt.Horizontal)
        self.binauralFrequencySlider.setRange(1, 50)  # Example range for binaural beats
        self.binauralFrequencySlider.valueChanged.connect(self.updateBinauralFrequency)
        binauralSliderLayout.addWidget(binauralLabel)
        binauralSliderLayout.addWidget(self.binauralFrequencySlider)
        mainLayout.addLayout(binauralSliderLayout)

        # Solfeggio Frequencies Slider
        solfeggioSliderLayout = QHBoxLayout()
        solfeggioLabel = QLabel('Solfeggio Frequencies (Hz):')
        self.solfeggioFrequencySlider = QSlider(Qt.Horizontal)
        self.solfeggioFrequencySlider.setRange(396, 852)  # Example range for solfeggio frequencies
        self.solfeggioFrequencySlider.valueChanged.connect(self.updateSolfeggioFrequency)
        solfeggioSliderLayout.addWidget(solfeggioLabel)
        solfeggioSliderLayout.addWidget(self.solfeggioFrequencySlider)
        mainLayout.addLayout(solfeggioSliderLayout)

        # Buttons for play, stop, and load profile
        self.playBinauralButton = QPushButton('Play Binaural Beats')
        self.playBinauralButton.clicked.connect(self.start_binaural_session)
        self.playSolfeggioButton = QPushButton('Play Solfeggio Frequencies')
        self.playSolfeggioButton.clicked.connect(self.start_solfeggio_session)
        self.stopButton = QPushButton('Stop')
        self.stopButton.clicked.connect(self.stopTone)
        #self.loadProfileButton = QPushButton('Load Profile')
        #self.loadProfileButton.clicked.connect(self.loadProfile)
        self.infoButton = QPushButton('Frequency Info')
        self.infoButton.clicked.connect(self.showFrequencyInfo)
        #self.viewLogsButton = QPushButton('View Logs')
        #self.viewLogsButton.clicked.connect(self.viewLogs)
        mainLayout.addWidget(self.playBinauralButton)
        mainLayout.addWidget(self.playSolfeggioButton)
        mainLayout.addWidget(self.stopButton)
        #mainLayout.addWidget(self.loadProfileButton)
        mainLayout.addWidget(self.infoButton)
        #mainLayout.addWidget(self.viewLogsButton)

        # Status display
        self.statusLabel = QLabel('Status: Ready')
        mainLayout.addWidget(self.statusLabel)

        # Set layout
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    def updateBinauralFrequency(self):
        frequency = self.binauralFrequencySlider.value()
        self.selected_binaural_frequency = frequency
        self.statusLabel.setText(f'Selected Binaural Frequency: {frequency} Hz')

    def updateSolfeggioFrequency(self):
        frequency = self.solfeggioFrequencySlider.value()
        self.selected_solfeggio_frequency = frequency
        self.statusLabel.setText(f'Selected Solfeggio Frequency: {frequency} Hz')

    def start_binaural_session(self):
        beat_frequency = getattr(self, 'selected_binaural_frequency', 10)  # Default to 10 if not set
        duration = 5  # Example duration in minutes
        threading.Thread(target=self.beat_generator.play_binaural_beat, args=(beat_frequency, duration)).start()
        self.session_management.start_session("binaural_beats")
        logging.info(f'Starting binaural session with frequency: {beat_frequency} Hz')

    def start_solfeggio_session(self):
        frequency = getattr(self, 'selected_solfeggio_frequency', 396)  # Default to 396 Hz if not set
        duration = 5  # Example duration in minutes
        threading.Thread(target=self.beat_generator.play_solfeggio_frequency, args=(frequency, duration)).start()
        self.session_management.start_session("solfeggio")
        self.statusLabel.setText(f'Playing Solfeggio Frequency: {frequency} Hz')

    
    def stopTone(self):
        global stop_tone
        stop_tone = True  # Signal to stop the tone    

    def loadProfile(self):
        user_names = list(UserProfile.PROFILES.keys())
        user_name, ok = QInputDialog.getItem(self, "Select Profile", "Choose a user profile:", user_names, 0, False)
        if ok and user_name:
            frequency = self.user_profile.load_profile(user_name)
            self.statusLabel.setText(f'Profile loaded: {user_name}')
            self.current_user_name = user_name  # Save the selected username
        
            # Disable the slider if a predefined profile is selected, enable it for Exploration
            if user_name != "Exploration":
                self.frequencySlider.setEnabled(False)
                self.selected_frequency = frequency
            else:
                self.frequencySlider.setEnabled(True)
                self.selected_frequency = self.frequencySlider.value()

    def showFrequencyInfo(self):
        info_text = (
            "0.5 to 4 Hz:\nDelta pattern. Linked to dreamless sleep, deep sleep, and relaxation.\n\n"
        "4 to 7 Hz:\nTheta pattern. Improves meditation, REM sleep, creativity.\n\n"
        "7 to 13 Hz:\nAlpha waves. Decreases anxiety, promotes relaxation, encourages positivity.\n\n"
        "13 to 30 Hz:\nBeta pattern. Promotes concentration and alertness, improved memory, problem-solving.\n\n"
        "30 to 50 Hz:\nGamma pattern. Enhances training and learning.\n\n"
        "396 Hz:\nRemoves fears, worries, anxiety, unblocks beliefs stopping personal goals.\n\n"
        "432 Hz:\nFills mind with peace and well-being, great for meditation or yoga.\n\n"
        "528 Hz:\nMay heal and repair the body, reduces stress in endocrine and autonomic systems.\n\n"
        "639 Hz:\nBalances emotions, elevates moods, promotes love, communication, understanding.\n\n"
        "741 Hz:\nAids problem-solving, self-expression, cleansing of the body.\n\n"
        "852 Hz:\nReplaces negative thoughts with positive ones, improves intuition, inner strength."
    )
        QMessageBox.information(self, "Frequency Information", info_text)
            
    def viewLogs(self):
        self.logViewer = LogViewer()
        self.logViewer.show()            

    def start_session(self):
        if hasattr(self, 'current_user_name'):
            user_name = self.current_user_name
        else:
            user_name = "Exploration"  # Default user name if none selected

        beat_frequency = getattr(self, 'selected_frequency', 10)  # Use the selected frequency, default to 10 if not set
        duration = 5  # Example duration in minutes
        threading.Thread(target=self.beat_generator.play_binaural_beat, args=(beat_frequency, duration)).start()
        self.session_management.start_session("exploration")

    def closeEvent(self, event):
        global stop_tone
        stop_tone = True  # Signal to stop the tone
        event.accept()
        sys.exit(0)  # Terminate the Python process    

# Main application
if __name__ == '__main__':
    logging.info('Starting Binaural Beat Explorer application.')
    beat_generator = BinauralBeatGenerator()
    user_profile = UserProfile()
    feedback_mechanism = FeedbackMechanism()
    predictive_engine = PredictiveEngine(user_data={})  # Example user data
    session_management = SessionManagement()
    app = QApplication(sys.argv)
    ui = BinauralBeatExplorerUI(beat_generator, user_profile, feedback_mechanism, predictive_engine, session_management)
    ui.show()  # Show the main window
    sys.exit(app.exec_())
