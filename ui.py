from tkinter import Tk, Label, Button, filedialog, N, S, E, W, DISABLED

from PIL import ImageTk, Image

from tf_object_detection import run_cam_object_detection, detect_objects_image


class ObjectDetectionApp:
    def __init__(self, master):
        self.master = master
        master.title("Tensorflow Object Detection")

        self.label = Label(master, text="Tensorflow Object Detection")
        self.label.grid(row=0, columnspan=2, pady=60)

        self.webcam_btn = Button(master, text="Webcam", command=self.open_webcam, padx=5, pady=5, width=20)
        self.webcam_btn.grid(row=1, column=0, padx=30, pady=10, sticky=N)

        self.webcam_btn = Button(master, text="Open file", command=self.open_image, padx=5, pady=5, width=20)
        self.webcam_btn.grid(row=2, column=0, padx=10, pady=10, sticky=N)

        self.orig_btn = Button(self.master, text="Show original", state=DISABLED, command=self.show_orig_image, padx=5, pady=5, width=20)
        self.orig_btn.grid(row=3, column=0, padx=10, pady=10, sticky=N)

        self.close_button = Button(master, text="Close", command=master.quit, padx=5, pady=5, width=20)
        self.close_button.grid(row=4, column=0, rowspan=11, padx=10, pady=10, sticky=N)

        self.img_lbl = Label(master, text="Open image", width=200, height=50)
        self.img_lbl.configure(background='#2a323a')
        self.img_lbl.grid(row=1, column=1, rowspan=14, sticky=(W, N, E, S))

        self.label.config(font=(None, 30))
        self.image = None
        self.filename = ""

    def open_image(self):
        self.filename = filedialog.askopenfilename(initialdir="./", title="Select file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        if not self.filename:
            return

        self.image = ImageTk.PhotoImage(detect_objects_image(self.filename))
        self.img_lbl = Label(self.master, image=self.image, height=600)
        self.img_lbl.grid(row=1, column=1, rowspan=14, padx=40, pady=40)
        self.orig_btn.config(state='normal', text="Show original")
        self.orig_btn.config(text="Show original", command=self.show_orig_image)

    def show_orig_image(self):
        if not self.filename:
            return
        self.label.image_dec = ImageTk.PhotoImage(Image.open(self.filename))
        self.img_lbl.config(image=self.label.image_dec)

        self.orig_btn.config(text="Detect objects", command=self.show_detection_image)

    def show_detection_image(self):
        self.img_lbl.config(image=self.image)
        self.orig_btn.config(text="Show original", command=self.show_orig_image)

    @staticmethod
    def open_webcam():
        run_cam_object_detection()


root = Tk()
my_gui = ObjectDetectionApp(root)
root.mainloop()
