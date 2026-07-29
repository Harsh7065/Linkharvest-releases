import sys
import webbrowser
import customtkinter as ctk
from tkinter import messagebox

RELEASES_URL = "https://github.com/Harsh7065/Linkharvest-releases/releases/latest"

def check_remote_control(control_data: dict, current_version: str):
    active = control_data.get("active", True)
    min_version = control_data.get("min_version", "v1.6.1")
    message = control_data.get("message", "")

    # Kill switch check first
    if not active:
        messagebox.showerror(
            "App Disabled",
            message or "You are not able to use this app right now."
        )
        sys.exit()

    # Version check
    if version_tuple(current_version) < version_tuple(min_version):
        result = messagebox.askyesno(
            "New Version Available",
            f"{message}\n\nDownload the new version now?"
        )
        if result:  # Yes
            webbrowser.open(RELEASES_URL)
            sys.exit()
        else:  # No
            sys.exit()

def version_tuple(v: str):
    return tuple(int(x) for x in v.split("."))
