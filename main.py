import os, json, tkinter as tk, ctypes, threading
from tkinter import filedialog, ttk

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.ffmpeg_path = tk.StringVar()
        self.video_path = tk.StringVar()
        self.audio_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.file_name = tk.StringVar()
        
        if os.path.exists("ffmpeg_path.json"):
            with open("ffmpeg_path.json", "r") as f:
                try:
                    data = json.load(f)
                    self.ffmpeg_path.set(data.get("ffmpeg_path", ""))
                    self.video_path.set(data.get("video_path", ""))
                    self.audio_path.set(data.get("audio_path", ""))
                    self.output_path.set(data.get("output_path", ""))
                    self.file_name.set(data.get("file_name", "output.mp4"))
                except json.JSONDecodeError:
                    self.ffmpeg_path.set("")
                    self.video_path.set("")
                    self.audio_path.set("")
                    self.output_path.set("")
                    self.file_name.set("output.mp4")

        # Frame for FFmpeg path
        ffmpeg_frame = tk.Frame(self)
        ffmpeg_frame.pack(pady=10, anchor="w", padx=10)
        tk.Label(ffmpeg_frame, text="FFmpeg Path, leave blank if in PATH").pack(anchor="w")
        self.ffmpeg_path_entry = tk.Entry(ffmpeg_frame, textvariable=self.ffmpeg_path, width=50)
        self.ffmpeg_path_entry.pack(side=tk.LEFT)
        self.ffmpeg_browse_button = tk.Button(ffmpeg_frame, text="Browse", command=self.browse_ffmpeg, borderwidth=0, highlightthickness=0, background="#3C3C3C", cursor="hand2")
        self.ffmpeg_browse_button.pack(side=tk.LEFT, padx=10)

        # Frame for Video path
        video_frame = tk.Frame(self)
        video_frame.pack(pady=10, anchor="w", padx=10)
        tk.Label(video_frame, text="Video Path").pack(anchor="w")
        self.video_path_entry = tk.Entry(video_frame, textvariable=self.video_path, width=50)
        self.video_path_entry.pack(side=tk.LEFT)
        self.video_browse_button = tk.Button(video_frame, text="Browse", command=self.browse_video, borderwidth=0, highlightthickness=0, background="#3C3C3C", cursor="hand2")
        self.video_browse_button.pack(side=tk.LEFT, padx=10)

        # Frame for Audio path
        audio_frame = tk.Frame(self)
        audio_frame.pack(pady=10, anchor="w", padx=10)
        tk.Label(audio_frame, text="Audio Path").pack(anchor="w")
        self.audio_path_entry = tk.Entry(audio_frame, textvariable=self.audio_path, width=50)
        self.audio_path_entry.pack(side=tk.LEFT)
        self.audio_browse_button = tk.Button(audio_frame, text="Browse", command=self.browse_audio, borderwidth=0, highlightthickness=0, background="#3C3C3C", cursor="hand2")
        self.audio_browse_button.pack(side=tk.LEFT, padx=10)
        

        # Output path
        output_frame = tk.Frame(self)
        output_frame.pack(pady=10, anchor="w", padx=10)
        tk.Label(output_frame, text="Output Path").pack(anchor="w")
        self.output_path_entry = tk.Entry(output_frame, textvariable=self.output_path, width=50)
        self.output_path_entry.pack(side=tk.LEFT)
        self.output_browse_button = tk.Button(output_frame, text="Browse", command=self.browse_output, borderwidth=0, highlightthickness=0, background="#3C3C3C", cursor="hand2")
        self.output_browse_button.pack(side=tk.LEFT, padx=10)

        output_file_frame = tk.Frame(self)
        output_file_frame.pack(pady=10, anchor="w", padx=10)
        tk.Label(output_file_frame, text="Output File Name").pack(anchor="w")
        self.output_file_name_entry = tk.Entry(output_file_frame, textvariable=self.file_name, width=50)
        self.output_file_name_entry.pack(side=tk.LEFT)
        self.output_browse_button = tk.Button(output_file_frame, text="Browse", command=self.browse_output_file)
        self.output_browse_button.pack(side=tk.LEFT, padx=10)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10, anchor="w", padx=10)
        self.save_button = tk.Button(button_frame, text="Save Paths", command=self.save_paths, borderwidth=0, highlightthickness=0, background="#3C3C3C", cursor="hand2")
        self.save_button.pack(side=tk.LEFT)
        self.run_button = tk.Button(button_frame, text="Merge", command=self.thread_run_ffmpeg, borderwidth=0, highlightthickness=0, background="#3C3C3C", cursor="hand2")
        self.run_button.pack(side=tk.LEFT, padx=10)
        self.clear_paths_button = tk.Button(button_frame, text="Clear Paths", command=self.clear_paths, borderwidth=0, highlightthickness=0, background="#3C3C3C", cursor="hand2")
        self.clear_paths_button.pack(side=tk.LEFT, padx=(0,10))
        
        # note
        note_frame = tk.Frame(self)
        note_frame.pack(pady=10, anchor="w", padx=10)
        tk.Label(note_frame, text="Note: If ffmpeg path is blank, it will be searched in PATH.", foreground="#5E5E5E").pack(anchor="w")
        tk.Label(note_frame, text="Note: If output path is blank, it will be saved in app directory.", foreground="#5E5E5E").pack(anchor="w")
        tk.Label(note_frame, text="Note: If ffmpeg asks you something in the terminal, please do as it says.", foreground="#5E5E5E").pack(anchor="w")
        
    def display_notification(self, title, message):
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x40000)
    def clear_paths(self):
        self.ffmpeg_path.set("")
        self.video_path.set("")
        self.audio_path.set("")
        self.output_path.set("")
        self.file_name.set("output.mp4")
        with open("ffmpeg_path.json", "w") as f:
            json.dump({"ffmpeg_path": "", "video_path": "", "audio_path": "", "output_path": "", "file_name": "output.mp4"}, f)
    def browse_ffmpeg(self):
        path = filedialog.askdirectory()
        if path:
            self.ffmpeg_path.set(os.path.join(path, "ffmpeg"))

    def browse_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mkv;*.avi;*.mov;*.webm")])
        if path:
            self.video_path.set(path)

    def browse_audio(self):
        path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.aac;*.wav;*.flac;*.opus;*.m4a;*.webm")])
        if path:
            self.audio_path.set(path)
    
    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)
    
    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(filetypes=[("Video Files", "*.mp4;*.mkv;*.avi;*.mov;*.webm")])
        if file_path:
            self.file_name.set(os.path.basename(file_path))

    
    def save_paths(self):
        paths = {
            "ffmpeg_path": self.ffmpeg_path.get(),
            "video_path": self.video_path.get(),
            "audio_path": self.audio_path.get(),
            "output_path": self.output_path.get(),
            "file_name": self.file_name.get()
        }
        with open("ffmpeg_path.json", "w") as f:
            json.dump(paths, f)
    
    def run_ffmpeg(self):
        with open("ffmpeg_path.json", "r") as f:
            try:
                data = json.load(f)
                self.ffmpeg_path.set(data.get("ffmpeg_path", ""))
                self.video_path.set(data.get("video_path", ""))
                self.audio_path.set(data.get("audio_path", ""))
                self.output_path.set(data.get("output_path", ""))
                self.file_name.set(data.get("file_name", ""))
            except json.JSONDecodeError:
                self.ffmpeg_path.set("")
                self.video_path.set("")
                self.audio_path.set("")
                self.output_path.set("")
                self.file_name.set("")
        
        ffmpeg_path = self.ffmpeg_path.get()
        video_path = self.video_path.get()
        audio_path = self.audio_path.get()
        output_path = self.output_path.get().replace("/", "\\")
        file_name = self.file_name.get()

        if video_path and audio_path:
            if not ffmpeg_path:
                ffmpeg_path = "ffmpeg"
            if not output_path:
                output_path = os.getcwd()
            #print(f'{ffmpeg_path} -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac "{output_path}\\{file_name}"')
            os.system(f'{ffmpeg_path} -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac "{output_path}\\{file_name}"')
            self.display_notification("FFmpeg Audio and Video Merger", f"Video and audio merged successfully\n {output_path}\\{file_name}")
        else:
            print("Please make sure all paths are set.")
            
    def thread_run_ffmpeg(self):
        threading.Thread(target=self.run_ffmpeg).start()

if __name__ == "__main__":
    app = MyApp()
    app.title("FFmpeg Audio and Video Merger")
    app.minsize(400, 400)
    app.resizable(False, False)
    app.tk_setPalette(background='#2b2b2b', foreground='white')
    try: 
        app.iconphoto(False, tk.PhotoImage(file='ffmpeg_icon.png'))
    except tk.TclError:
        print("Icon not found, using default icon")

    app.mainloop()