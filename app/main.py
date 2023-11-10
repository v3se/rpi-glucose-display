
# importing required libraries
import sys
from datetime import datetime
from api_fetcher import ApiFetcher
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt

url = "https://vesegluco.whado.net/api/v1/entries.json?count=1&token=rpi-6db835066442effa"

direction_mapping = {
    'SingleUp': '↑',
    'SingleDown': '↓',
    'Flat': '→',  # Customize the character for "flat"
    'FortyFiveUp': '↗',  # Customize the character for "left"
    'FortyFiveDown': '↘',  # Customize the character for "right"
}


def custom_round(number):
    # Check if the absolute value is less than 0.5
    if abs(number) < 0.5:
        return 0
    else:
        return round(number)


def format_data(data):
    sgv_mmol = str(round(data[0]['sgv'] * 0.0555, 1))  # Convert to mmol
    # Assuming the timestamp is in milliseconds, so divide by 1000
    epoch_timestamp = data[0]['date'] / 1000
    timestamp_datetime = datetime.fromtimestamp(epoch_timestamp)
    # Get the current datetime
    current_datetime = datetime.now()
    # Calculate the time difference
    time_difference = current_datetime - timestamp_datetime
    sgv_with_arrow = f"<span style='font-size: 120px;'>{sgv_mmol}</span><span style='font-size: 100px; vertical-align: super;'>{direction_mapping[data[0]['direction']]}</span>"
    minutes_ago = custom_round(time_difference.total_seconds() / 60)

    return {
        'sgv': sgv_with_arrow,
        'date_delta': minutes_ago,
    }


class Window(QWidget):

    def __init__(self):
        super().__init__()

        # setting geometry of main window
        self.setGeometry(100, 100, 320, 240)

        # creating a vertical layout
        layout = QVBoxLayout()

        # creating font object
        font = QFont('Arial', 120, QFont.Bold)
        # Adjust the font size as needed
        font_smaller = QFont('Arial', 40, QFont.Bold)

        # creating a label object
        self.label_sgv = QLabel()
        self.label_date_delta = QLabel()

        # Set font and alignment for each label
        self.label_sgv.setFont(font)
        self.label_date_delta.setFont(font_smaller)

        self.label_sgv.setStyleSheet("color: white;")
        self.label_date_delta.setStyleSheet("color: white;")

        self.label_sgv.setAlignment(Qt.AlignCenter)
        self.label_date_delta.setAlignment(Qt.AlignCenter)

        # Add labels to the layout
        layout.addWidget(self.label_sgv)
        layout.addWidget(self.label_date_delta)

        # setting the layout to main window
        self.setLayout(layout)

        self.setStyleSheet("background-color: black;")

        # creating a timer object
        timer = QTimer(self)

        # adding action to timer
        timer.timeout.connect(self.showTime)

        # update the timer every second
        timer.start(1000)

    # method called by timer
    def showTime(self):
        apiFetcher = ApiFetcher(url)
        data = format_data(apiFetcher.fetch_nightscout_data())
        self.label_sgv.setText(f'<html>{data["sgv"]}</html>')
        self.label_date_delta.setText(str(data['date_delta']) + " min ago")


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# showing all the widgets
window.showMaximized()

# start the app
App.exit(App.exec_())
