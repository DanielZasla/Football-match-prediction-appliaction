import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd


teams = pd.read_csv("teams.csv")
teams = teams[['team_api_id', 'team_long_name']]
id2name = {}
name2id = {}
for i in teams.iterrows():
    id2name[i[1][0]] = i[1][1]
    name2id[i[1][1]] = i[1][0]


##### GUI

# Create a new Tkinter window
window = tk.Tk()
# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
# Calculate the desired window width and height
window_width = int(screen_width * 0.8)  # 80% of the screen width
window_height = int(screen_height * 0.6)  # 60% of the screen height
window.geometry(f"{window_width}x{window_height}")
# Set the window title
window.title("Soccer Prediction")
# Create a label widget
label = tk.Label(window, text="No file selected.")
# Pack the label widget into the window
label.pack()

test_f, test_l = None, None


def upload_file():
    """
    Prompts a file dialog for the user and attempts to load the file into the program.
    Prints the result (success / fail) in the program, specifically in `output_text`.
    """
    file_path = filedialog.askopenfilename()
    label.config(text="Selected File: " + file_path)
    try:
        load_file(file_path)
        output_text.insert(tk.END, "File loaded successfully.\n")
    except:
        output_text.insert(tk.END, "Failed to load file. Make sure file is in the correct format.\n")


def load_file(file):
    """
    Loads file from the given path and extracts the data into global variables `test_f` and `test_l`.

    :param str file: Path to the file.
    :raise Exception: If data extraction from the file fails.
    """
    global test_f, test_l
    temp = pd.read_csv(file)
    test_l = temp["label"]
    test_f = temp.drop("label", axis=1)
    output_text.see(tk.END)


load_button = tk.Button(window, text="Load File", command=upload_file)
load_button.pack()

button_frame = tk.Frame(window)
button_frame.pack()

# Create an array of buttons
buttons = []
button_texts = ["Load KNN", "Load GNB", "Load HGB", "Load RF"]


knn = pickle.load(open('KNN.sav', 'rb'))
gnb = pickle.load(open('GNB.sav', 'rb'))
hgb = pickle.load(open('HGB.sav', 'rb'))
rf = pickle.load(open('RF.sav', 'rb'))
curr_model = None


def load_model(model):
    """
    Loads one of the preloaded models (knn, gnb, hgb, or rf) into the system and inserts explanatory
    text into output_text.
    :param model: One of the preloaded models (knn, gnb, hgb, or rf).
    """

    global curr_model
    curr_model = model
    name = str(type(model)).split(".")[-1][:-2]
    output_text.insert(tk.END, f"Loaded model:\t{name}\n")
    output_text.see(tk.END)


b_knn = tk.Button(button_frame, text=button_texts[0], command=lambda: load_model(knn))
b_gnb = tk.Button(button_frame, text=button_texts[1], command=lambda: load_model(gnb))
b_hgb = tk.Button(button_frame, text=button_texts[2], command=lambda: load_model(hgb))
b_rf = tk.Button(button_frame, text=button_texts[3], command=lambda: load_model(rf))
b_knn.pack(side=tk.LEFT, padx=5)
b_gnb.pack(side=tk.LEFT, padx=5)
b_hgb.pack(side=tk.LEFT, padx=5)
b_rf.pack(side=tk.LEFT, padx=5)

output_frame = tk.Frame(window)
output_frame.pack(fill=tk.BOTH, expand=True)

# Create a text widget for displaying output
output_text = tk.Text(output_frame)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the scrollbar to scroll the text widget
scrollbar.config(command=output_text.yview)
output_text.config(yscrollcommand=scrollbar.set)

idHome, idAway = None, None


def predict():
    """
    Performs the prediction between two teams with the selected model and outputs the result to
    `output_text`. If instead any of the information required isn't yet provided, outputs a request to load the model
    and the dataset.
    """
    if test_l is None or test_l is None:
        output_text.insert(tk.END, f"Select dataset before predicting.\n")
        return
    if curr_model is None:
        output_text.insert(tk.END, f"Select model before predicting.\n")
        return
    if idHome is None or idAway is None:
        output_text.insert(tk.END, f"Select teams before predicting.\n")
        return

    mask_f = (test_f['home_team_api_id'].isin([idHome])) & (test_f['away_team_api_id'].isin([idAway]))
    matching_rows = test_f[mask_f]
    if len(matching_rows.index) < 1:
        output_text.insert(tk.END, "The selected teams don't have a match between them. Please select different "
                                   "teams.\n")
        return

    row = matching_rows.index[0]
    selected_label = test_l.iloc[row]
    pred_result = curr_model.predict(matching_rows)[0]
    output_text.insert(tk.END, f"Predicted: {pred_result}  --  Actual: {selected_label}\n")
    output_text.see(tk.END)


predict_button = tk.Button(window, text="Predict", command=predict)
predict_button.pack()

popWindow = False

def open_dropdown_window():
    """
    Opens and manages the `Teams Selection` window.
    """
    # Create a new window
    global popWindow
    if popWindow:
        return
    popWindow = True

    dropdown_window = tk.Toplevel()
    dropdown_window.title("Teams Selection")

    # Create a label widget
    label1 = tk.Label(dropdown_window, text="Select an option:")
    label1.pack()

    # Create a list of options for the first dropdown
    mapper = pickle.load(open("mapper.dict", "rb"))
    options1 = list(mapper.keys())

    # Create a StringVar to store the selected option for the first dropdown
    selected_option1 = tk.StringVar()

    label2 = tk.Label(dropdown_window, text="Select another option:")
    label2.pack()

    # Create a list of options for the second dropdown
    options2 = []

    def option_selected(event):
        dropdown2.set("")
        selected_value = dropdown1.get()
        dropdown2.config(values=mapper[selected_value])
    # Create the first dropdown list (combobox)
    dropdown1 = ttk.Combobox(dropdown_window, values=options1, textvariable=selected_option1)
    dropdown1.pack()
    dropdown1.bind("<<ComboboxSelected>>", option_selected)

    # Create a StringVar to store the selected option for the second dropdown
    selected_option2 = tk.StringVar()

    # Create the second dropdown list
    dropdown2 = ttk.Combobox(dropdown_window, values=options2, textvariable=selected_option2)
    dropdown2.pack()

    # Function to be executed when the button is clicked
    def select_button_clicked():
        selected_value1 = selected_option1.get()
        selected_value2 = selected_option2.get()
        if selected_value1 and selected_value2:
            output_text.insert(tk.END, f"{selected_value1} vs. {selected_value2}.\n")
            global idHome, idAway, popWindow
            idHome, idAway = name2id[selected_value1], name2id[selected_value2]
            popWindow = False
            dropdown_window.destroy()
        else:
            output_text.insert(tk.END, f"Two teams weren't selected.\n")

    # Create a button to perform an action
    button = tk.Button(dropdown_window, text="Select", command=select_button_clicked)
    button.pack()

    def close_selection_window():
        global popWindow
        popWindow = False
        dropdown_window.destroy()

    dropdown_window.protocol("WM_DELETE_WINDOW", close_selection_window)

    dropdown_width = window.winfo_screenwidth()
    dropdown_height = window.winfo_screenheight()
    dropdown_width = int(dropdown_width * 0.15)
    dropdown_height = int(dropdown_height * 0.15)
    dropdown_window.geometry(f"{dropdown_width}x{dropdown_height}")


open_button = tk.Button(window, text="Select Teams", command=open_dropdown_window)
open_button.pack()

# Run the Tkinter event loop
window.mainloop()
