import json
from io import BytesIO
from contextlib import suppress
import tkinter as tk
from tkinter import filedialog
import seaborn as sns
import matplotlib.pyplot as plt
import torch
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def custom_build_print_options(options=None):
    
    if options and isinstance(options, dict):
        
        pass
    else:
     
        options = {"default_option": "default_value"}
    
    return options

def custom_generate_pdf(source, print_options):
   
    buffer = BytesIO()
    with canvas.Canvas(buffer, pagesize=letter) as pdf:
        pdf.drawString(100, 100, f"Source: {source}")
        pdf.drawString(100, 80, f"Print Options: {print_options}")

    return buffer.getvalue()

def select_file():
    file_selected = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_selected:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_selected)

def handle_and_display():
    file_path = entry_path.get()
    if not file_path.endswith('.json'):
        status_label.config(text="Selected file is not a JSON file.")
        return

    with open(file_path, 'r') as file:
        event_data = {"body": file.read()}

    params = {}
    with suppress(Exception):
        parsed = json.loads(event_data["body"])
        params = parsed if isinstance(parsed, dict) else {}

    source = params.get("source")
    if source is None:
        status_label.config(text="Source is required.")
        return

    print_options = custom_build_print_options(params.get("print_options"))
    pdf_content = custom_generate_pdf(source, print_options)

    
    status_label.config(text=f"Generated PDF content: {pdf_content[:50]}...")


root = tk.Tk()
root.title("PDF Generation with GUI")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=20, pady=20)

label_path = tk.Label(frame, text="Select JSON File:")
label_path.grid(row=0, column=0, sticky='e')

entry_path = tk.Entry(frame, width=50)
entry_path.grid(row=0, column=1, padx=5)

button_browse = tk.Button(frame, text="Browse", command=select_file)
button_browse.grid(row=0, column=2, padx=5)

button_generate = tk.Button(frame, text="Generate PDF", command=handle_and_display)
button_generate.grid(row=1, column=1, pady=10)

status_label = tk.Label(frame, text="")
status_label.grid(row=2, column=0, columnspan=3, pady=10)


sns.set(style="whitegrid")


torch_tensor = torch.randn(100)


sns.lineplot(x=range(len(torch_tensor)), y=torch_tensor.numpy())
plt.title('Seaborn Plot of Torch Tensor')
plt.show()

root.mainloop()
