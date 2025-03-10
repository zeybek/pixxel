"""
Dark themed message boxes for the application.
"""
import tkinter as tk
from tkinter import messagebox as mb

class DarkMessageBox:
    """
    A class to create dark themed message boxes.
    This overrides the default tkinter messagebox with a custom dark themed version.
    """
    
    @staticmethod
    def _create_dark_dialog(parent, title, message, icon=None, buttons=None, default=None):
        """Create a custom dark themed dialog box"""
        # Colors
        bg_color = "#2e2e2e"
        fg_color = "#e0e0e0"
        button_bg = "#4a6ea9"
        button_fg = "#ffffff"
        
        # Create dialog window
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.configure(bg=bg_color)
        dialog.resizable(False, False)
        dialog.transient(parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        dialog_width = 300
        dialog_height = 150
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # Icon and message
        frame = tk.Frame(dialog, bg=bg_color, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        if icon:
            icon_label = tk.Label(frame, image=icon, bg=bg_color)
            icon_label.grid(row=0, column=0, padx=(0, 10))
            
        msg_label = tk.Label(frame, text=message, bg=bg_color, fg=fg_color, 
                            wraplength=250, justify=tk.LEFT, font=("Arial", 10))
        msg_label.grid(row=0, column=1, sticky="w")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=bg_color, padx=10, pady=10)
        button_frame.pack(fill=tk.X)
        
        result = [None]  # Use a list to store the result
        
        def set_result(value):
            result[0] = value
            dialog.destroy()
        
        if not buttons:
            buttons = [("OK", 1)]
            
        for i, (text, value) in enumerate(buttons):
            btn = tk.Button(button_frame, text=text, bg=button_bg, fg=button_fg,
                          activebackground="#5a7eb9", activeforeground=button_fg,
                          relief=tk.RAISED, bd=1, padx=10, pady=2,
                          command=lambda v=value: set_result(v))
            btn.pack(side=tk.RIGHT, padx=5)
            
            if value == default:
                btn.focus_set()
        
        # Handle window close
        dialog.protocol("WM_DELETE_WINDOW", lambda: set_result(None))
        
        # Wait for the dialog to be closed
        dialog.wait_window()
        return result[0]
    
    @staticmethod
    def showinfo(parent, title, message):
        """Show an information message box"""
        return DarkMessageBox._create_dark_dialog(
            parent, title, message, 
            buttons=[("OK", 1)], default=1
        )
    
    @staticmethod
    def showwarning(parent, title, message):
        """Show a warning message box"""
        return DarkMessageBox._create_dark_dialog(
            parent, title, message, 
            buttons=[("OK", 1)], default=1
        )
    
    @staticmethod
    def showerror(parent, title, message):
        """Show an error message box"""
        return DarkMessageBox._create_dark_dialog(
            parent, title, message, 
            buttons=[("OK", 1)], default=1
        )
    
    @staticmethod
    def askquestion(parent, title, message):
        """Ask a question with Yes/No buttons"""
        result = DarkMessageBox._create_dark_dialog(
            parent, title, message, 
            buttons=[("No", 0), ("Yes", 1)], default=1
        )
        return "yes" if result == 1 else "no"
    
    @staticmethod
    def askyesno(parent, title, message):
        """Ask a question with Yes/No buttons, return boolean"""
        result = DarkMessageBox._create_dark_dialog(
            parent, title, message, 
            buttons=[("No", 0), ("Yes", 1)], default=1
        )
        return result == 1
    
    @staticmethod
    def askokcancel(parent, title, message):
        """Ask a question with OK/Cancel buttons"""
        result = DarkMessageBox._create_dark_dialog(
            parent, title, message, 
            buttons=[("Cancel", 0), ("OK", 1)], default=1
        )
        return result == 1

# Override the default messagebox functions
def patch_messagebox(parent_window):
    """Patch the messagebox module to use dark themed message boxes"""
    mb.showinfo = lambda title, message: DarkMessageBox.showinfo(parent_window, title, message)
    mb.showwarning = lambda title, message: DarkMessageBox.showwarning(parent_window, title, message)
    mb.showerror = lambda title, message: DarkMessageBox.showerror(parent_window, title, message)
    mb.askquestion = lambda title, message: DarkMessageBox.askquestion(parent_window, title, message)
    mb.askyesno = lambda title, message: DarkMessageBox.askyesno(parent_window, title, message)
    mb.askokcancel = lambda title, message: DarkMessageBox.askokcancel(parent_window, title, message) 