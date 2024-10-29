from fit_tool.fit_file import FitFile
from fit_tool.fit_file_builder import FitFileBuilder
from fit_tool.profile.messages.record_message import RecordMessage
from fit_tool.profile.messages.session_message import SessionMessage
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

def correct_averages(input_file,output_file):
    """The following program reads all the bytes from a FIT formatted file and then
        decodes these bytes to create a FIT file object. We then build a modified FIT file
        based on a variety of criteria (see comments below). Finally we output
        the modified data to a new FIT file.
    """
    
    fit_file = FitFile.from_file(input_file)

    builder = FitFileBuilder(auto_define=False)

    heart_rate_values = []
    cadence_values = []
    power_values = []
    speed_values = []
    for record in fit_file.records:
        message = record.message
        if isinstance(message, RecordMessage):
            heart_rate_values.append(message.heart_rate)
            cadence_values.append(message.cadence)
            power_values.append(message.power)
            speed_values.append(message.speed)

    for record in fit_file.records:
        message = record.message
        if isinstance(message, SessionMessage):
            message.avg_heart_rate = np.round(np.mean(heart_rate_values))
            message.avg_cadence = np.round(np.mean(cadence_values))
            message.avg_power = np.round(np.mean(power_values))
            message.avg_speed = np.round(np.mean(speed_values))
        builder.add(message)


    modified_file = builder.build()
    modified_file.to_file(output_file)

def select_input_file():
    input_file = filedialog.askopenfilename(filetypes=[("FIT Files", "*.fit")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, input_file)

def process_files():
    input_file = input_file_entry.get()
    output_file = os.path.splitext(input_file)[0] + "_AveragesCorrected.fit"

    # Call your existing correct_averages function here
    correct_averages(input_file, output_file)

    # Display a success message
    success_label.config(text="Processing completed successfully!")

# Create the main window
window = tk.Tk()
window.title("FIT File Average Correction")

# Input file label and entry
input_file_label = tk.Label(window, text="Input File:")
input_file_label.grid(row=0, column=0)
input_file_entry = tk.Entry(window)
input_file_entry.grid(row=0, column=1)
input_file_button = tk.Button(window, text="Browse", command=select_input_file)
input_file_button.grid(row=0, column=2)

# Process button
process_button = tk.Button(window, text="Process", command=process_files)
process_button.grid(row=1, columnspan=3)

# Success message label
success_label = tk.Label(window, text="")
success_label.grid(row=2, columnspan=3)

window.mainloop()