import pyaudio
import wave
import sys, time
import numpy as np
import tkinter, tkinter.scrolledtext, time
import pylab
from scipy.io.wavfile import read
from scipy.fftpack import fft
import matplotlib.pyplot as plt


def ende():
    main.destroy()

main = tkinter.Tk()



wf = wave.open("C:/Users/Jonas/Desktop/basssmth2.wav", "rb")

CHUNK = 1024
RATE =wf.getframerate()

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
sampwidth = wf.getsampwidth()
stream = p.open(format=p.get_format_from_width(sampwidth), channels=wf.getnchannels(), rate=wf.getframerate(), output=True)

# read data
data = bytearray(wf.readframes(CHUNK))


w = tkinter.Canvas(main,width=1000, height=800, bg="yellow", highlightthickness=0)
w.pack(fill="both", expand=True)

dataRect = []
d = 0

for i in range(200):
    dataRect.append(w.create_rectangle(d, 800, d+10, 800 , fill='red'))
    d+=10
main.update()


a = 3

while len(data) > 0:
    
	data = np.fromstring(wf.readframes(CHUNK), dtype=np.int16)
    
    # compute FFT and update line
    yf = fft(data)
  
    da = np.abs(yf[0:CHUNK])  / (128 * CHUNK)
    
    d = 20
        
    for i in range(200):
        if d < 200:
            w.coords(dataRect[i], d, 690-(da[i*2])*6, d+20, 700)
            d+=20
        else:
            w.coords(dataRect[i], d, 690-(da[i*2])*6, d+10, 700)
            d+=10

        main.update()

          
    stream.write(bytes(data))

    
	
# stop stream (4)
main.mainloop()
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()