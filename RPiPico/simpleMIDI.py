import time
import random
import usb_midi
import adafruit_midi
import time
import board
import digitalio

from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.control_change import ControlChange

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

print('MIDI Test')
print(f'Default output MIDI channel: {midi.out_channel + 1}')

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

buttons_prev = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
button_pins = [board.GP0,board.GP1,board.GP2,board.GP3,board.GP4,board.GP5,board.GP6,board.GP7,
               board.GP8,board.GP9,board.GP10,board.GP11,board.GP12,board.GP13,board.GP14,board.GP15,
               board.GP16,board.GP17,board.GP18,board.GP19,board.GP20,board.GP21,board.GP22,board.GP26,
               board.GP27,board.GP28]
note_mapping = [
        [36, ], # GP0
        [37, ], # GP1
        [38, ], # GP2
        [39, ], # GP3
        [40, ], # GP4
        [41, ], # GP5
        [42, ], # GP6
        [43, ], # GP7
        [44, ], # GP8
        [45, ], # GP9
        [46, ], # GP10
        [47, ], # GP11
        [48, ], # GP12
        [49, ], # GP13
        [50, ], # GP14
        [51, ], # GP15
        [52, ], # GP16
        [53, ], # GP17
        [54, ], # GP18
        [55, ], # GP19
        [56, ], # GP20
        [57, ], # GP21
        [58, ], # GP22
        [59, ], # GP26
        [60, ], # GP27
        [61, ]  # GP28
    ]
buttons = [digitalio.DigitalInOut(bp) for bp in button_pins]

for btn in buttons:
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP

while True:
    for i, button in enumerate(buttons):
        if button.value != buttons_prev[i]:
            buttons_prev[i] = button.value
            if button.value == 0:
                midi.send([NoteOn(note, 60) for note in note_mapping[i]])
                print(f'Note {note_mapping[i]} On')
                led.value = 1
            else:
                midi.send([NoteOff(note, 60) for note in note_mapping[i]])
                print(f'Note {note_mapping[i]} Off')
                led.value = 0
    time.sleep(0.005)
