import tkinter
import PIL.Image
import PIL.ImageTk
import cv2
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import doctest
doctest.testmod()
data = np.genfromtxt("logAngles.txt", delimiter=",", names=["date&time","raw_yaw" ,"filter_yaw","smooth_yaw" , "raw_pitch","filter_pitch","smooth_pitch" ])
BUFFERSIZE = 15
dataBuffer = [0]*BUFFERSIZE
print(type(data))

class App:
    def __init__(self, window, video_source1, video_source2):
        self.window = window
        self.window.title("DUAL MEDIA PLAYER")
        self.video_source1 = video_source1
        self.video_source2 = video_source2
        self.photo1 = ""
        self.photo2 = ""

        # open video source
        self.vid1 = MyVideoCapture(self.video_source1, self.video_source2)

        # Create a canvas that can fit the above video source size
        self.canvas1 = tkinter.Canvas(window, width=500, height=500)
        self.canvas2 = tkinter.Canvas(window, width=500, height=500)
        self.canvas1.pack(padx=5, pady=5, side="left")
        self.canvas2.pack(padx=5, pady=5, side="left")
        figure1 = plt.Figure(figsize=(5,4), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self)
        bar1.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        ax1.plot(data['raw_yaw'])
        ax1.set_xlabel("Time(in Seconds)")
        ax1.set_ylabel("Changes in Angles(in Degree)")
        ax1.legend("Raw Data")
        ax1.set_title('Raw Data')
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret1, frame1, ret2, frame2 = self.vid1.get_frame

        if ret1 and ret2:
                self.photo1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
                self.photo2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame2))
                self.canvas1.create_image(0, 0, image=self.photo1, anchor=tkinter.NW)
                self.canvas2.create_image(0, 0, image=self.photo2, anchor=tkinter.NW)
                
                
        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source1, video_source2):
        # Open the video source
        self.vid1 = cv2.VideoCapture(video_source1)
        self.vid2 = cv2.VideoCapture(video_source2)

        if not self.vid1.isOpened():
            raise ValueError("Unable to open video source", video_source1)

    @property
    def get_frame(self):
        ret1 = ""
        ret2 = ""
        if self.vid1.isOpened() and self.vid2.isOpened():
            ret1, frame1 = self.vid1.read()
            ret2, frame2 = self.vid2.read()
            frame1 = cv2.resize(frame1, (500, 500))
            frame2 = cv2.resize(frame2, (500, 500))
            if ret1 and ret2:
                # Return a boolean success flag and the current frame converted to BGR
                return ret1, cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB), ret2, cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            else:
                return ret1, None, ret2, None
        else:
            return ret1, None, ret2, None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid1.isOpened():
            self.vid1.release()
        if self.vid2.isOpened():
            self.vid2.release()


def callback():
    global v1,v2
    v1=E1.get()
    v2=E2.get()
    if v1 == "" or v2 == "":
        L3.pack()
        return
    initial.destroy()


v1 = ""
v2 = ""

initial = tkinter.Tk()
initial.title("KEC MEDIA PLAYER")
L0 = tkinter.Label(initial, text="Enter the full path")
L0.pack()
L1 = tkinter.Label(initial, text="Video 1")
L1.pack()
E1 = tkinter.Entry(initial, bd =5)
E1.pack()
L2 = tkinter.Label(initial, text="Video 2")
L2.pack()
E2 = tkinter.Entry(initial, bd =5)
E2.pack()
B = tkinter.Button(initial, text ="Next", command = callback)
B.pack()
L3 = tkinter.Label(initial, text="Enter both the names")



initial.mainloop()
# Create a window and pass it to the Application object
App(tkinter.Tk(),v1, v2)

