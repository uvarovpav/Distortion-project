from scipy import signal
import matplotlib.pyplot as plt
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
from scipy.fftpack import fft, fftfreq
from math import e, pow
import librosa
import librosa.display
from pygame import mixer
import soundfile as sf


root = tkinter.Tk()

menubar = Menu(root)
root.config(menu=menubar)

global dist_fl, sr, n, time, amp, th, gain, dist_amp, panel1, panel2, panel3, panel4, DistType, clr_fl
clr_fl = True
th = IntVar()
gain = IntVar()


def open_file():
    global n, amp, time, dist_fl, sr
    dist_fl = False
    file = filedialog.askopenfilename()
    amp, sr = librosa.load(file)
    mixer.init(frequency=sr, channels=2)
    sf.write('sound.wav', amp, samplerate=sr)
    n = np.size(amp)
    total = n/sr
    time = np.linspace(0, total, n)
    fileinf['text'] = "Choose the Distortion type"
    ApplyPlotAllBtn.config(state=NORMAL)


def sine_wave():
    global n, amp, time, dist_fl, sr
    dist_fl = False
    sr = 0
    time = np.linspace(0, 50, 1000)
    amp = np.sin(time)
    n = np.size(time)
    fileinf['text'] = "Choose the Distortion type"
    ApplyPlotAllBtn.config(state=NORMAL)


def square_wave():
    global n, amp, time, dist_fl, sr
    dist_fl = False
    sr = 0
    time = np.linspace(0, 50, 1000)
    amp = signal.square(time)
    n = np.size(time)
    fileinf['text'] = "Choose the Distortion type"
    ApplyPlotAllBtn.config(state=NORMAL)


def sawtooth():
    global n, amp, time, dist_fl, sr
    dist_fl = False
    sr = 0
    time = np.linspace(0, 50, 1000)
    amp = signal.sawtooth(time)
    n = np.size(time)
    fileinf['text'] = "Choose the Distortion type"
    ApplyPlotAllBtn.config(state=NORMAL)


def apply_distortion(t):
    if t == 0:
        apply_hard()
    elif t == 1:
        apply_soft()
    elif t == 2:
        apply_fuzz()
    elif t == 3:
        apply_cubic()


def count(start, end, step):
    while start <= end:
        yield start
        start += step


def apply_hard():
    global dist_amp
    t = int(th_scale.get())/10
    g = int(gain_scale.get())/10
    dist_amp = np.zeros(n)
    for i in count(0, n-1, 1):
        if np.abs(amp[i]) < t:
            dist_amp[i] = g*amp[i]
        else:
            if amp[i] > t:
                dist_amp[i] = g*t
            else:
                dist_amp[i] = -(g*t)
    if sr > 0:
        sf.write('dist.wav', dist_amp, samplerate=sr)


def apply_soft():
    global dist_amp
    t = int(th_scale.get())/10
    g = int(gain_scale.get())/10
    dist_amp = np.zeros(n)
    for i in count(0, n - 1, 1):
        if np.abs(amp[i]) < t:
            dist_amp[i] = g * (amp[i] - (amp[i] ** 3) / 3)
        else:
            if amp[i] > t:
                dist_amp[i] = g * 2 / 3
            else:
                dist_amp[i] = -g * 2 / 3
    if sr > 0:
        sf.write('dist.wav', dist_amp, samplerate=sr)


def apply_fuzz():
    global dist_amp
    g = int(gain_scale.get())
    dist_amp = np.zeros(n)
    for i in count(0, n - 1, 1):
        if amp[i] == 0:
            dist_amp[i] = 0
        else:
            a = amp[i]/np.abs(amp[i])
            b = a*amp[i]*g/10
            c = pow(e, b)
            dist_amp[i] = a*(1-c)
    if sr > 0:
        sf.write('dist.wav', dist_amp, samplerate=sr)


def apply_cubic():
    global dist_amp
    t = int(th_scale.get())/10
    g = int(gain_scale.get())/10
    dist_amp = np.zeros(n)
    for i in count(0, n-1, 1):
        if amp[i] >= 0:
            dist_amp[i] = g*(pow(amp[i]-1, 3) - 0.5*(amp[i]-1) + t)
        else:
            dist_amp[i] = -g*(pow(-amp[i]-1, 3) - 0.5*(-amp[i]-1) + t)
    if sr > 0:
        sf.write('dist.wav', dist_amp, samplerate=sr)


def hard_clipping():
    global dist_fl, DistType
    dist_fl = True
    th_scale.set(3)
    gain_scale.set(11)
    DistType = 0
    fileinf['text'] = "Adjust controllers and press Apply & Plot"


def fuzz():
    global dist_fl, DistType
    dist_fl = True
    th_scale.set(0)
    gain_scale.set(15)
    DistType = 2
    fileinf['text'] = "Adjust controllers and press Apply & Plot"


def soft_clipping():
    global dist_fl, DistType
    dist_fl = True
    th_scale.set(4)
    gain_scale.set(11)
    DistType = 1
    fileinf['text'] = "Adjust controllers and press Apply & Plot"


def cubic_func():
    global dist_fl, DistType
    dist_fl = True
    th_scale.set(5)
    gain_scale.set(8)
    DistType = 3
    fileinf['text'] = "Adjust controllers and press Apply & Plot"


open_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Open", menu=open_menu)
open_menu.add_command(labe="Open file", command=open_file)
submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Generate", menu=submenu)
submenu.add_command(label="Sine wave", command=sine_wave)
submenu.add_command(label="Square wave", command=square_wave)
submenu.add_command(label="Sawtooth wave", command=sawtooth)
distortion_types = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Choose distortion type", menu=distortion_types)
distortion_types.add_command(label="Hard clipping", command=hard_clipping)
distortion_types.add_command(label="Soft clipping", command=soft_clipping)
distortion_types.add_command(label="Fuzz", command=fuzz)
distortion_types.add_command(label="Cubic Function", command=cubic_func)

root.title("Player")
root.iconbitmap(r'icon.ico')

fileinf = Label(root, text='Generate a function or open a file')
fileinf.pack(pady=10)


def plot_wave(t, am):
    global panel1
    fig1 = plt.figure(figsize=[4.5, 4.0])
    plt.plot(t, am)
    plt.title('Wave')
    fig1.savefig('wave.png')
    path = "wave.png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel1 = Label(leftframe, image=img)
    panel1.image = img
    panel1.pack(side=TOP, fill="both", expand="yes")


def plot_sa(num, am):
    global panel2
    fig2 = plt.figure(figsize=[4.5, 4.0])
    x = fft(am)

    fr1 = fftfreq(num)
    fr = fr1 > 0
    ps = 2.0 * (np.abs(x / n) ** 2)
    pslog = librosa.power_to_db(ps, ref=1.0)

    plt.plot(fr1[fr], pslog[fr])
    plt.title('Power spectrum without the distortion')
    fig2.savefig('sa.png')
    path = "sa.png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel2 = Label(rightframe, image=img)
    panel2.image = img
    panel2.pack(side=TOP, fill="both", expand="yes")


def plot_diswave(t, am):
    global panel3
    fig3 = plt.figure(figsize=[4.5, 4.0])
    plt.plot(t, am)
    plt.title('Distorted waveform')
    fig3.savefig('diswave.png')
    path = "diswave.png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel3 = Label(leftframe, image=img)
    panel3.image = img
    panel3.pack(side=BOTTOM, fill="both", expand="yes")


def plot_sad(num, am):
    global panel4
    fig4 = plt.figure(figsize=[4.5, 4.0])
    x = fft(am)

    fr1 = fftfreq(num)
    fr = fr1 > 0
    ps = 2.0*(np.abs(x/n)**2)
    pslog = librosa.power_to_db(ps, ref=1.0)

    plt.plot(fr1[fr], pslog[fr])
    plt.title('Power spectrum with the distortion')
    fig4.savefig('sad.png')
    path = "sad.png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel4 = Label(rightframe, image=img)
    panel4.image = img
    panel4.pack(side=BOTTOM, fill="both", expand="yes")


def clear():
    global clr_fl
    clr_fl = True
    panel1.destroy()
    panel2.destroy()
    if dist_fl:
        panel3.destroy()
        panel4.destroy()
    fileinf['text'] = "Generate function or open a file"
    ClearBtn.config(state=DISABLED)


def play():
    while mixer.get_busy():
        time.sleep(1)
    if sr > 0:
        if dist_fl:
            mixer.music.load('dist.wav')
            mixer.music.play()
        else:
            mixer.music.load('sound.wav')
            mixer.music.play()


def apply_plot():
    global panel1, panel2, panel3, panel4, time, amp, dist_amp, n, dist_fl, clr_fl
    if not clr_fl:
        clear()
    clr_fl = False
    if dist_fl:
        apply_distortion(DistType)
    plot_wave(time, amp)
    plot_sa(n, amp)
    if dist_fl:
        plot_diswave(time, dist_amp)
        plot_sad(n, dist_amp)
    fileinf['text'] = "Press Clear to start over"
    ClearBtn.config(state=NORMAL)


rightframe = Frame(root)
rightframe.pack(side=RIGHT)
leftframe = Frame(root)
leftframe.pack(side=LEFT)


PlayBtn = Button(root, text='Play', command=play)
PlayBtn.pack(pady=5, padx=10)

ApplyPlotAllBtn = Button(root, text='Apply & Plot', command=apply_plot, state=DISABLED)
ApplyPlotAllBtn.pack(pady=5, padx=10)

ClearBtn = Button(root, text='Clear', command=clear, state=DISABLED)
ClearBtn.pack(pady=5)

th_scale = Scale(root, from_=0, to=20, variable=th, label='Threshold', orient=HORIZONTAL)
th_scale.pack()

gain_scale = Scale(root, from_=0, to=100, variable=gain, label='Gain', orient=HORIZONTAL)
gain_scale.pack()

root.mainloop()
