# importing required libraries
import sys
import os
from datetime import datetime
from api_fetcher import ApiFetcher
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt
from jinja2 import Template  # Install Jinja2 using pip

# Set the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.realpath(__file__)))

url = "https://vesegluco.whado.net/api/v1/entries.json?count=1&token=rpi-6db835066442effa"

direction_mapping = {
    'SingleUp': '↑',
    'SingleDown': '↓',
    'Flat': '→',
    'FortyFiveUp': '↗',
    'FortyFiveDown': '↘',
}


def custom_round(number):
    # Check if the absolute value is less than 0.5
    return 0 if abs(number) < 0.5 else round(number)


def format_data(data):
    sgv_mmol = str(round(data[0]['sgv'] * 0.0555, 1))  # Convert to mmol
    epoch_timestamp = data[0]['date'] / 1000
    timestamp_datetime = datetime.fromtimestamp(epoch_timestamp)
    current_datetime = datetime.now()
    time_difference = current_datetime - timestamp_datetime
    minutes_ago = str(custom_round(time_difference.total_seconds() / 60))

    return {
        'sgv': sgv_mmol,
        'minutes_ago': minutes_ago,
        'direction': direction_mapping[data[0]["direction"]]
    }


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # setting geometry of the main window
        self.setFixedWidth(320)
        self.setFixedHeight(240)

        # creating a vertical layout
        main_layout = QVBoxLayout()

        # creating font object
        font_sgv = QFont('Arial', 85, QFont.Bold)  # Increase font size for label_sgv
        font_direction = QFont('Arial', 50)  # Adjust font size for label_direction
        font_smaller = QFont('Arial', 20, QFont.Bold)

        # creating a horizontal layout for sgv and direction
        sgv_direction_layout = QHBoxLayout()

        # creating a label object for sgv_mmol
        self.label_sgv = QLabel()
        self.label_sgv.setFont(font_sgv)
        self.label_sgv.setStyleSheet("color: white;")
        self.label_sgv.setAlignment(Qt.AlignCenter)  # Center the label text

        # creating a label object for direction_mapping
        self.label_direction = QLabel()
        self.label_direction.setFont(font_direction)
        self.label_direction.setStyleSheet("color: white; margin-left: -10px;")  # Adjust margin for closer spacing
        sgv_direction_layout.addWidget(self.label_sgv)
        sgv_direction_layout.addWidget(self.label_direction)
        sgv_direction_layout.setAlignment(Qt.AlignCenter)

        # creating a label object for minutes_ago
        self.label_minutes_ago = QLabel()
        self.label_minutes_ago.setFont(font_smaller)
        self.label_minutes_ago.setStyleSheet("color: white;")
        self.label_minutes_ago.setAlignment(Qt.AlignCenter)

        self.setContentsMargins(0, 20, 0, 0)  # Adjust the top margin value
        # Add the horizontal layout and minutes_ago label to the vertical layout
        main_layout.addStretch(1)  # Add stretch to center widgets vertically
        main_layout.addLayout(sgv_direction_layout)
        main_layout.addWidget(self.label_minutes_ago)
        main_layout.addStretch(1)  # Add stretch to center widgets vertically
        # setting the main layout to the main window
        self.setLayout(main_layout)

        self.setStyleSheet("background-color: black;")

        # creating a timer object
        timer = QTimer(self)

        # adding action to timer
        timer.timeout.connect(self.showTime)

        # update the timer every second
        timer.start(1000)

    # method called by the timer
    def showTime(self):
        apiFetcher = ApiFetcher(url)
        data = format_data(apiFetcher.fetch_nightscout_data())
        self.label_sgv.setText(f'<html>{data["sgv"]}</html>')
        self.label_direction.setText(f'<html>{data["direction"]}</html>')

        # Only display minutes_ago if the delta is over 5 minutes
        delta_minutes = int(data["minutes_ago"])
        if delta_minutes > 5:
            self.label_minutes_ago.setText(f'<html>Readings late {delta_minutes} mins</html>')
        else:
            self.label_minutes_ago.clear()  # Clear the label if delta is not over 5 minutes


# create PyQt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# showing all the widgets
window.showFullScreen()

# start the app
App.exit(App.exec_())
