import os
import subprocess
import sys
import time
import tkinter as tk
from tkinter.messagebox import askyesno, showinfo, askokcancel, showerror
import customtkinter
from ppadb.client import Client as AdbClient

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AdbConnection:
    currentDevices = []

    def initConnection():
        try :
            client = AdbClient(host="127.0.0.1", port=5037)
            devices = client.devices()
        except:
            subprocess.Popen([resource_path('adb.exe'), 'start-server'], shell=True).wait()
            devices = client.devices()

        if devices.__len__() > 0:
            AdbConnection.currentDevices = devices

class App(customtkinter.CTk):
        def __init__(self):
                AdbConnection.initConnection()
                super().__init__()
                customtkinter.set_appearance_mode("dark")
                self.title("Push Text")
                self.sendText_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Send Text", command=self.click)
                self.sendText_button.grid(row=1, column=0, sticky="ew")
                self.inputText = tk.Text(self, height=20, width=60)
                self.inputText.grid(row=2, column=0, sticky="ew")

        def click(self):
            commandlist = []
            for line in self.inputText.get("1.0",tk.END).splitlines():
                commandlist.append("am broadcast -a ADB_INPUT_TEXT --es msg '"+line+"'")
                commandlist.append("am broadcast -a ADB_INPUT_CODE --ei code 66")
            
            commandlist.pop()

            try:
                for device in AdbConnection.currentDevices:
                    device.shell("ime enable com.android.adbkeyboard/.AdbIME")
                    time.sleep(0.1)
                    device.shell("ime set com.android.adbkeyboard/.AdbIME")
                    for command in commandlist:
                        time.sleep(0.1)
                        device.shell(command)
                    time.sleep(0.1)    
                    device.shell("ime reset")        
            except: 
                AdbConnection.initConnection()
                if AdbConnection.currentDevices.__len__ != 0:
                    for device in AdbConnection.currentDevices:
                        device.shell("ime enable com.android.adbkeyboard/.AdbIME")
                        time.sleep(0.1)
                        device.shell("ime set com.android.adbkeyboard/.AdbIME")
                        for command in commandlist:
                            time.sleep(0.1)
                            device.shell(command)
                        time.sleep(0.1)    
                        device.shell("ime reset")
                else:
                    showerror(title="Failed", message="No device connected!\nPlease make sure that your devices are connected properly.")
            

if __name__ == "__main__":
        def on_closing():
            if askokcancel("Quit", "Do you want to quit?"):
                app.destroy()
                try:
                    os.remove("Data/temp.png")
                except:
                    pass

        app = App()
        app.protocol("WM_DELETE_WINDOW", on_closing)
        app.mainloop()
