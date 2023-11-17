# importing required libraries
import sys
import os
from datetime import datetime
from api_fetcher import ApiFetcher
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
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
    minutes_ago = custom_round(time_difference.total_seconds() / 60)

    with open('template.html', 'r') as template_file:
        template_content = template_file.read()

    template = Template(template_content)
    sgv_with_arrow = template.render(sgv_mmol=sgv_mmol, direction_mapping=direction_mapping[data[0]['direction']], data=data, minutes_ago=minutes_ago)

    return {
        'sgv': sgv_with_arrow
    }


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # setting geometry of the main window
        self.setGeometry(100, 100, 320, 240)

        # creating a vertical layout
        layout = QVBoxLayout()

        # creating font object
        font = QFont('Arial', 120, QFont.Bold)
        font_smaller = QFont('Arial', 20, QFont.Bold)

        # creating a label object
        self.label_sgv = QLabel()

        # Set font and alignment for the label
        self.label_sgv.setFont(font)
        self.label_sgv.setStyleSheet("color: white;")
        self.label_sgv.setAlignment(Qt.AlignCenter)

        # Add label to the layout
        layout.addWidget(self.label_sgv)

        # setting the layout to the main window
        self.setLayout(layout)

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


# create PyQt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# showing all the widgets
window.showFullScreen()

# start the app
App.exit(App.exec_())
