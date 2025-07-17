import tkinter as tk
from tkinter import ttk, messagebox
import inspect
import function1
import function2
import OC
import obejctivePrio

# Combine all functions
FUNCTION_MAP = {
    # **{f.__name__: f for f in vars(function1).values() if callable(f)},
    # **{f.__name__: f for f in vars(function2).values() if callable(f)},
    **{f.__name__: f for f in vars(OC).values() if callable(f)},
    **{f.__name__: f for f in vars(obejctivePrio).values() if callable(f)},
    
}

class FunctionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Analysis App")
        self.geometry("400x400")

        # Function selector
        self.function_var = tk.StringVar()
        ttk.Label(self, text="Select a Function:").pack()
        self.function_dropdown = ttk.Combobox(self, textvariable=self.function_var, values=list(FUNCTION_MAP.keys()))
        self.function_dropdown.pack()
        self.function_dropdown.bind("<<ComboboxSelected>>", self.show_inputs)

        # Frame for input fields
        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(pady=10)

        # Run button
        self.run_button = ttk.Button(self, text="Run", command=self.run_function)
        self.run_button.pack()

        # Output box
        self.output_text = tk.Text(self, height=10)
        self.output_text.pack(fill="both", expand=True)

        self.inputs = {}

    def show_inputs(self, event=None):
        # Clear existing inputs
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.inputs.clear()

        func_name = self.function_var.get()
        func = FUNCTION_MAP[func_name]
        sig = inspect.signature(func)

        for param in sig.parameters.values():
            lbl = ttk.Label(self.input_frame, text=f"{param.name}:")
            lbl.pack()
            entry = ttk.Entry(self.input_frame)
            entry.pack()
            self.inputs[param.name] = entry

    def run_function(self):
        func_name = self.function_var.get()
        func = FUNCTION_MAP[func_name]
        sig = inspect.signature(func)
        kwargs = {}

        try:
            for name, entry in self.inputs.items():
                param_type = sig.parameters[name].annotation
                raw_value = entry.get()

                # Convert to proper type
                if param_type == int:
                    value = int(raw_value)
                elif param_type == float:
                    value = float(raw_value)
                else:
                    value = raw_value  # assume string

                kwargs[name] = value

            result = func(**kwargs)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, str(result))
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = FunctionApp()
    app.mainloop()
