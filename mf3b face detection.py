import customtkinter as ctk
import tkinter as tk
import cv2
from PIL import Image, ImageTk

app = ctk.CTk()


class Camera:
    def __init__(self, content):

        self.master = content

        self.webcam = cv2.VideoCapture(1)
        self.width, self.height = 200, 150
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self.is_running = False
        self.detect_faces = False

        self.frontal_face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        self.instructions = ctk.CTkLabel(master=content, font=('Eina01-Bold', 12), text_color='White',
                                         text='To start, select < Open Camera >\n'
                                              'To toggle frontal face detection, select < Face Detection >',
                                         justify='left')
        self.instructions.grid(column=0, row=0, padx=20, pady=10, sticky='w')

        self.instructions2 = ctk.CTkLabel(master=content, font=('Eina01-Bold', 12, 'bold'), text_color='#FEF375',
                                          text='[YELLOW]')
        self.instructions2.grid(column=0, row=1, padx=20, sticky='w')

        self.instructions3 = ctk.CTkLabel(master=content, font=('Eina01-Bold', 12, 'bold'), text_color='white',
                                          text='means that the function is running.')
        self.instructions3.grid(column=0, row=1, padx=100, sticky='w')

        self.newFrame = ctk.CTkFrame(master=content, fg_color='transparent', width=470, height=250,
                                     bg_color='transparent')
        self.newFrame.grid(column=0, columnspan=10, row=2)

        self.videoframefeed = tk.Label(master=self.newFrame, bg='#242424')
        self.videoframefeed.grid(column=1, row=0, rowspan=3, pady=10, sticky='nw')

        self.buttonFrame = ctk.CTkFrame(master=self.newFrame, fg_color='transparent', bg_color='transparent')
        self.buttonFrame.grid(column=0, row=0, sticky='nw')

        def on_enterOC(event):
            self.open_cam_button.configure(fg_color='#FEF37B')
            self.open_cam_button.configure(text_color='black')

        def on_leaveOC(event):
            self.open_cam_button.configure(text_color='white')
            self.open_cam_button.configure(fg_color='#424449')

        self.open_cam_button = ctk.CTkButton(master=self.buttonFrame, text="Open Camera", command=self.openCam,
                                             font=('Eina01-Bold', 12),
                                             fg_color='#424449', bg_color='transparent')
        self.open_cam_button.bind('<Enter>', on_enterOC)
        self.open_cam_button.bind('<Leave>', on_leaveOC)
        self.open_cam_button.grid(column=0, row=0, padx=20, pady=10)

        def on_enter(event):
            self.face_detect_button.configure(fg_color='#FEF37B')
            self.face_detect_button.configure(text_color='black')

        def on_leave(event):
            self.face_detect_button.configure(text_color='white')
            self.face_detect_button.configure(fg_color='#424449')

        self.face_detect_button = ctk.CTkButton(master=self.buttonFrame, text='Face Detection', command=self.toggle_fd,
                                                font=('Eina01-SemiBold', 12),
                                                fg_color='#424449', bg_color='transparent')
        self.face_detect_button.bind('<Enter>', on_enter)
        self.face_detect_button.bind('<Leave>', on_leave)
        self.face_detect_button.grid(column=0, row=1, padx=20, pady=10)

        def on_enterCC(event):  # event; connected to CTkButton bind: when the cursor is on the button
            self.close_cam_button.configure(fg_color='#FEF37B')  # button color becomes yellow
            self.close_cam_button.configure(text_color='black')  # button text becomes black

        def on_leaveCC(event):  # event; connected to CTkButton bind: when the cursor leaves the button
            self.close_cam_button.configure(text_color='white')  # the text color becomes white
            self.close_cam_button.configure(fg_color='#424449')  # button color becomes gray

        self.close_cam_button = ctk.CTkButton(master=self.buttonFrame, text="Stop Camera", command=self.stop_camera,
                                              font=('Eina01-Bold', 12), fg_color='#424449', bg_color='transparent')
        self.close_cam_button.bind('<Enter>', on_enterCC)  # '<Enter>' is when the cursor collides with shape
        self.close_cam_button.bind('<Leave>',
                                   on_leaveCC)  # '<'Leave>' is when the cursor exits collision with button shape
        self.close_cam_button.grid(column=0, row=2, padx=20, pady=10)

    def openCam(self):
        if not self.is_running:
            self.webcam = cv2.VideoCapture(1)
            self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.is_running = True
            self.show_frame()

    def show_frame(self):

        app.geometry('525x500')

        if self.is_running:
            ret, frame = self.webcam.read()
            self.open_cam_button.configure(fg_color='#FEF37B', text_color='black')

            if ret:
                frame = cv2.flip(frame, 1)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                if self.detect_faces:
                    self.face_detect_button.configure(fg_color='#FEF37B', text_color='black')
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = self.frontal_face.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), color=[254, 243, 123], thickness=2)  # bounding box
                        cv2.putText(frame, 'Frontal Face', (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, [254, 243, 123])

                captured_image = Image.fromarray(frame)
                photo_image = ImageTk.PhotoImage(image=captured_image)
                self.videoframefeed.photo_image = photo_image
                self.videoframefeed.configure(image=photo_image)
            else:
                self.stop_camera()

            self.master.after(10, self.show_frame)

    def stop_camera(self):
        app.geometry('435x390')
        self.is_running = False
        self.videoframefeed.configure(image='')
        if self.webcam.isOpened():
            self.webcam.release()
            app.geometry('435x390')
        cv2.destroyAllWindows()

    def toggle_fd(self):
        self.detect_faces = not self.detect_faces

    def __del__(self):
        if self.webcam.isOpened():
            self.webcam.release()
        cv2.destroyAllWindows()


app_header = ctk.CTkFrame(master=app, height=200, width=400, bg_color='transparent', fg_color='transparent')
app_header.grid(column=0, columnspan=10, row=0, sticky='w')
app_logo = ctk.CTkImage(light_image=Image.open('eyes.png'), size=(35, 35))
app_logo = ctk.CTkLabel(master=app_header, text="LOOK AHEAD", font=('Eina01-Bold', 25), image=app_logo,
                        compound=ctk.LEFT, padx=20, pady=10)
app_logo.grid(column=0, row=1, sticky='w')

content = ctk.CTkFrame(master=app, bg_color='transparent', fg_color='transparent')
content.grid(column=0, row=2, columnspan=10, sticky='w')

app_description = ctk.CTkLabel(content,
                               text="This is a software created for video capture and frontal face detection\n"
                                    "as part of the course requirements for LBYMF3B.\n\n"
                                    "Logo by Royyan Wijaya | Flaticon", text_color='white',
                               font=('Eina01-SemiBold', 12), justify=ctk.LEFT, padx=20, pady=10)
app_description.grid(column=0, columnspan=10, row=5, sticky='w')

app.title('LOOK AHEAD: Frontal Face Detection System')
app.geometry('435x390')
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app.iconbitmap('eyes (1).ico')
camera_app = Camera(content)
app.mainloop()
