import sys
import webbrowser
import customtkinter as ctk
from tkinter import messagebox

DEFAULT_RELEASES_URL = "https://github.com/Harsh7065/Linkharvest-releases/releases/latest"
APP_VERSION = "1.6.0"  # bump this on every release

def check_remote_control(control_data: dict, current_version: str = APP_VERSION):
    active = control_data.get("active", True)
    min_version = control_data.get("min_version", "1.6.0")
    message = control_data.get("message", "")
    download_url = control_data.get("download_url", DEFAULT_RELEASES_URL)

    # Kill switch check first
    if not active:
        messagebox.showerror(
            "App Disabled",
            message or "You are not able to use this app right now."
        )
        sys.exit()

    # Version check
    if version_tuple(current_version) < version_tuple(min_version):
        show_update_dialog(message, download_url)

def show_update_dialog(message: str, download_url: str):
    import tkinter as tk
    has_root = tk._default_root is not None

    dialog = ctk.CTkToplevel() if has_root else ctk.CTk()
    dialog.title("New Version Available")
    dialog.resizable(False, False)
    dialog.attributes("-topmost", True)

    label = ctk.CTkLabel(
        dialog,
        text=message,
        wraplength=340,
        justify="left",
    )
    label.pack(padx=24, pady=(24, 16), fill="both", expand=False)

    button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
    button_frame.pack(pady=(0, 20))

    def on_download():
        webbrowser.open(download_url)
        sys.exit()

    def on_cancel():
        sys.exit()

    ctk.CTkButton(button_frame, text="Download", command=on_download, width=110).pack(side="left", padx=8)
    ctk.CTkButton(button_frame, text="Cancel", command=on_cancel, width=110, fg_color="gray40", hover_color="gray30").pack(side="left", padx=8)

    dialog.update_idletasks()  # force layout so winfo_width/height are accurate
    w = dialog.winfo_reqwidth()
    h = dialog.winfo_reqheight()
    dialog.geometry(f"{w}x{h}")
    dialog.grab_set()
    dialog.protocol("WM_DELETE_WINDOW", sys.exit)

    if has_root:
        dialog.wait_window()  # blocks without starting a second mainloop
    else:
        dialog.mainloop()

def version_tuple(v: str):
    return tuple(int(x) for x in v.lstrip("vV").split("."))
