from tkinter import *
from tkinter import filedialog
from tkinter import ttk  # Use themed widgets
from pygame import mixer
mixer.init()
import datetime
from mutagen.mp3 import MP3

# --- Move this function here ---
def draw_gradient(canvas, color1, color2):
    '''Draws a vertical gradient from color1 to color2 on the given canvas.'''
    width = canvas.winfo_reqwidth()
    height = canvas.winfo_reqheight()
    limit = height
    (r1, g1, b1) = canvas.winfo_rgb(color1)
    (r2, g2, b2) = canvas.winfo_rgb(color2)
    r_ratio = float(r2 - r1) / limit
    g_ratio = float(g2 - g1) / limit
    b_ratio = float(b2 - b1) / limit
    for i in range(limit):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = "#%04x%04x%04x" % (nr, ng, nb)
        canvas.create_line(0, i, width, i, fill=color)
# --- End move ---

#Global var
totalsonglength=0

def musicUrl():
	try:
		dd=filedialog.askopenfilename(initialdir='C:/Users/Mausam/Music/Songs',
			title='select audio file',
			filetype=(('MP3','*mp3'),('WAV','*wav')))
		#print(dd)
	except:
		dd=filedialog.askopenfilename(filetype=(('MP3','*mp3'),('WAV','*wav')))
	audiotrack.set(dd)
def playMusic():
	ad=audiotrack.get()
	mixer.music.load(ad)
	mixer.music.play()
	audioStatusLabel.configure(text='Playing')
	ProgressbarLabel.grid()
	root.muteButton.grid()
	mixer.music.set_volume(0.4)
	ProgressbarVolume['value']=40
	ProgressbarVolumeLabel['text']='40%'
	ProgressbarMusicLabel.grid()

	Song=MP3(ad)
	totalsonglength=int(Song.info.length)
	ProgressbarMusic['maximum']=totalsonglength
	ProgressbarMusicEndTimeLabel.configure(text='{}'.format(str(datetime.timedelta(seconds=totalsonglength))))
	def Progressbarmusictick():
		CurrentSongLength=mixer.music.get_pos()//1000
		ProgressbarMusic['value']=CurrentSongLength
		ProgressbarMusicStartTimeLabel.configure(text='{}'.format(str(datetime.timedelta(seconds=CurrentSongLength))))
		ProgressbarMusic.after(2,Progressbarmusictick)
	Progressbarmusictick()
def pauseMusic():
	mixer.music.pause()
	root.PauseButton.grid_remove()
	root.ResumeButton.grid()
	audioStatusLabel.configure(text='Resuming')
def resumeMusic():
	mixer.music.unpause()
	root.ResumeButton.grid_remove()
	root.PauseButton.grid()
	audioStatusLabel.configure(text='Playing')
def volumeUp():
	vol=mixer.music.get_volume()
	if(vol>=vol*100):
		mixer.music.set_volume(vol+0.1)
	else:
		mixer.music.set_volume(vol+0.05)
	ProgressbarVolumeLabel.configure(text='{}%'.format(int(mixer.music.get_volume()*100)))
	ProgressbarVolume['value']=mixer.music.get_volume()*100
def volumeDown():
	vol=mixer.music.get_volume()
	if(vol<=vol*100):
		mixer.music.set_volume(vol-0.1)
	else:
		mixer.music.set_volume(vol-0.05)
	ProgressbarVolumeLabel.configure(text='{}%'.format(int(mixer.music.get_volume()*100)))
	ProgressbarVolume['value']=mixer.music.get_volume()*100
def unmuteMusic():
	global currentvol
	root.unmuteButton.grid_remove()
	root.muteButton.grid()
	mixer.music.set_volume(currentvol)
def muteMusic():
	global currentvol
	root.muteButton.grid_remove()
	root.unmuteButton.grid()
	currentvol=mixer.music.get_volume()
	mixer.music.set_volume(0)

def stopMusic():
	mixer.music.stop()
	audioStatusLabel.configure(text='Stopping')
#creating this function to add buttons and other important modules
def createwidthes():
	global audiotrack
	audiotrack = StringVar()
	global currentvol
	currentvol = 0
	global playIcon, pauseIcon, browseIcon, volumeUpIcon, volumeDownIcon, muteIcon, unmuteIcon, stopIcon, resumeIcon
	global audioStatusLabel, ProgressbarLabel, ProgressbarVolume, ProgressbarVolumeLabel, ProgressbarMusicLabel, ProgressbarMusicStartTimeLabel, ProgressbarMusicEndTimeLabel, ProgressbarMusic

	# Modern color palette
	main_bg = "#22223b"        # deep blue for frame
	accent_bg = "#9d4edd"      # purple accent
	button_bg = "#f2e9e4"      # light for buttons
	button_fg = "#22223b"      # dark text for buttons
	label_fg = "#f2e9e4"       # light text for labels
	entry_bg = "#4a4e69"       # muted blue for entry

	playIcon=PhotoImage(file='play-button.png')
	pauseIcon=PhotoImage(file='pause.png')
	browseIcon=PhotoImage(file='search-engine.png')
	volumeUpIcon=PhotoImage(file='volume-up.png')
	volumeDownIcon=PhotoImage(file='volume-down.png')
	muteIcon=PhotoImage(file='mute.png')
	unmuteIcon=PhotoImage(file='unmute.png')
	stopIcon=PhotoImage(file='stop.png')
	resumeIcon=PhotoImage(file='resume.png')

	playIcon=playIcon.subsample(12,12)
	pauseIcon=pauseIcon.subsample(12,12)
	browseIcon=browseIcon.subsample(12,12)
	volumeUpIcon=volumeUpIcon.subsample(12,12)
	volumeDownIcon=volumeDownIcon.subsample(12,12)
	muteIcon=muteIcon.subsample(12,12)
	unmuteIcon=unmuteIcon.subsample(12,12)
	stopIcon=stopIcon.subsample(12,12)
	resumeIcon=resumeIcon.subsample(12,12)

	style = ttk.Style()
	style.theme_use('clam')
	style.configure('TButton',
		font=('Segoe UI', 12, 'bold'),
		padding=10,
		background=button_bg,
		foreground=button_fg,
		borderwidth=0,
		focusthickness=3,
		focuscolor=accent_bg)
	style.map('TButton',
		background=[('active', accent_bg)],
		foreground=[('active', '#fff')])
	style.configure('TLabel',
		font=('Segoe UI', 12, 'bold'),
		background=main_bg,
		foreground=label_fg)
	style.configure('TEntry',
		font=('Segoe UI', 12),
		fieldbackground=entry_bg,
		background=entry_bg,
		foreground="#fff")
	style.configure('TProgressbar',
		thickness=12,
		background=accent_bg,
		troughcolor="#4a4e69",
		bordercolor=main_bg,
		lightcolor=accent_bg,
		darkcolor=accent_bg)


	main_frame.grid_rowconfigure((0,1,2,3), weight=1)
	main_frame.grid_columnconfigure((0,1,2,3), weight=1)

	TrackLabel=ttk.Label(main_frame,text='🎵 Audio Track Menu',style='TLabel')
	TrackLabel.grid(row=0, column=0, padx=12, pady=12, sticky='nsew')

	TrackLabelEntry=ttk.Entry(main_frame,font=('Segoe UI', 12),width=35,textvariable=audiotrack)
	TrackLabelEntry.grid(row=0, column=1, padx=12, pady=12, sticky='nsew')

	BrowseButton=ttk.Button(main_frame,text='Search',image=browseIcon,compound=LEFT,command=musicUrl)
	BrowseButton.grid(row=0, column=2, padx=12, pady=12, sticky='nsew')

	PlayButton=ttk.Button(main_frame,text='Play',image=playIcon,compound=LEFT,command=playMusic)
	PlayButton.grid(row=1, column=0, padx=12, pady=12, sticky='nsew')

	StopButton=ttk.Button(main_frame,text='Stop',image=stopIcon,compound=LEFT,command=stopMusic)
	StopButton.grid(row=2, column=0, padx=12, pady=12, sticky='nsew')

	root.PauseButton=ttk.Button(main_frame,text='Pause',image=pauseIcon,compound=LEFT,command=pauseMusic)
	root.PauseButton.grid(row=1, column=1, padx=12, pady=12, sticky='nsew')

	root.ResumeButton=ttk.Button(main_frame,text='Resume',image=resumeIcon,compound=LEFT,command=resumeMusic)
	root.ResumeButton.grid(row=1, column=1, padx=12, pady=12, sticky='nsew')
	root.ResumeButton.grid_remove()

	VolumeUpButton=ttk.Button(main_frame,text='Vol +',image=volumeUpIcon,compound=LEFT,command=volumeUp)
	VolumeUpButton.grid(row=1, column=2, padx=12, pady=12, sticky='nsew')

	VolumeDownButton=ttk.Button(main_frame,text='Vol -',image=volumeDownIcon,compound=LEFT,command=volumeDown)
	VolumeDownButton.grid(row=2, column=2, padx=12, pady=12, sticky='nsew')

	root.muteButton=ttk.Button(main_frame,text='Mute',image=muteIcon,compound=LEFT,command=muteMusic)
	root.muteButton.grid(row=3, column=2, padx=12, pady=12, sticky='nsew')
	root.muteButton.grid_remove()

	root.unmuteButton=ttk.Button(main_frame,text='UnMute',image=unmuteIcon,compound=LEFT,command=unmuteMusic)
	root.unmuteButton.grid(row=3, column=2, padx=12, pady=12, sticky='nsew')
	root.unmuteButton.grid_remove()

	audioStatusLabel=ttk.Label(main_frame,text='',style='TLabel')
	audioStatusLabel.grid(row=2, column=1, padx=12, pady=12, sticky='nsew')

	# Progress-bar
	ProgressbarLabel=ttk.Label(main_frame,text='',background=main_bg)
	ProgressbarLabel.grid(row=0,column=3,rowspan=3,padx=12,pady=12, sticky='nsew')
	ProgressbarLabel.grid_remove()

	ProgressbarVolume=ttk.Progressbar(ProgressbarLabel,orient=VERTICAL,mode='determinate',value=0,length=190,style='TProgressbar')
	ProgressbarVolume.grid(row=0,column=0,ipadx=5, sticky='nsew')

	ProgressbarVolumeLabel=ttk.Label(ProgressbarLabel,text='0%',background=main_bg,foreground=accent_bg,width=3)
	ProgressbarVolumeLabel.grid(row=0,column=0, sticky='s')

	ProgressbarMusicLabel=ttk.Label(main_frame,text='',background=main_bg)
	ProgressbarMusicLabel.grid(row=3,column=0,columnspan=3,padx=12,pady=12, sticky='nsew')

	ProgressbarMusicStartTimeLabel=ttk.Label(ProgressbarMusicLabel,text='0:00:0',background=main_bg,foreground=accent_bg,width=8)
	ProgressbarMusicStartTimeLabel.grid(row=0,column=0, sticky='w')

	ProgressbarMusicEndTimeLabel=ttk.Label(ProgressbarMusicLabel,text='0:00:0',background=main_bg,foreground=accent_bg,width=8)
	ProgressbarMusicEndTimeLabel.grid(row=0,column=2, sticky='e')

	ProgressbarMusic=ttk.Progressbar(ProgressbarMusicLabel,orient=HORIZONTAL,mode='determinate',value=0,style='TProgressbar')
	ProgressbarMusic.grid(row=0,column=1,ipadx=300,ipady=3, sticky='nsew')
	ProgressbarMusicLabel.grid_remove()

root=Tk()
root.geometry('1050x500+100+100')
root.title('Corona Music App Player')
root.iconbitmap('kingbondl.ico')
root.resizable(False, False)

# Create a canvas for the gradient background
gradient_canvas = Canvas(root, width=1050, height=500, highlightthickness=0)
gradient_canvas.pack(fill="both", expand=True)
root.update()
draw_gradient(gradient_canvas, "#a1c4fd", "#c2e9fb")  # blue gradient

# Place a frame in the center for all widgets
main_frame = Frame(gradient_canvas, bg="#22223b", bd=0, relief=FLAT, highlightthickness=0)
main_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=820, height=420)

createwidthes()
StringText=''
count=0
text=''
SliderLabel = ttk.Label(root, text=StringText, background='#c2e9fb', font=('Segoe UI', 15, 'italic'))
SliderLabel.place(relx=0.5, rely=0.95, anchor=CENTER)
def StringTextSliderShow():
	global count,text
	if(count>=len(StringText)):
		count=-1
		text=''
		SliderLabel.configure(text=text)
	else:
		text=text+StringText[count]
		SliderLabel.configure(text=text)
	count+=1
	SliderLabel.after(200,StringTextSliderShow)
StringTextSliderShow()

root.mainloop()
