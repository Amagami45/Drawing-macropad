import time
import board
import digitalio
import rotaryio
import usb_hid
import busio
import adafruit_ssd1306

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)

i2c = busio.I2C(board.GP9, board.GP8) 
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

def update_oled(text):
    oled.fill(0)
    oled.text(text, 0, 0, 1)
    oled.show()

update_oled("Macropad Ready")

ENC_A = board.GP0
ENC_B = board.GP1
ENC_BTN = board.GP2

KEY_PINS = [
    board.GP3,  
    board.GP4,  
    board.GP5,  
    board.GP6,  
    board.GP7,  
]

encoder = rotaryio.IncrementalEncoder(ENC_A, ENC_B)
last_pos = encoder.position

enc_btn = digitalio.DigitalInOut(ENC_BTN)
enc_btn.switch_to_input(pull=digitalio.Pull.UP)
enc_btn_last = enc_btn.value

keys = []
for pin in KEY_PINS:
    k = digitalio.DigitalInOut(pin)
    k.switch_to_input(pull=digitalio.Pull.UP)
    keys.append(k)

keys_last = [k.value for k in keys]

def key_action(i):
    if i == 0:
        update_oled("Undo")
        kbd.press(Keycode.CONTROL, Keycode.Z)
        kbd.release_all()

    elif i == 1:
        update_oled("Redo")
        kbd.press(Keycode.CONTROL, Keycode.SHIFT, Keycode.Z)
        kbd.release_all()

    elif i == 2:
        update_oled("Brush")
        kbd.press(Keycode.B)
        kbd.release_all()

    elif i == 3:
        update_oled("Eraser")
        kbd.press(Keycode.E)
        kbd.release_all()

    elif i == 4:
        update_oled("Picker")
        kbd.press(Keycode.I)
        kbd.release_all()


def encoder_turn(delta):
    if delta > 0:
        update_oled("Zoom +")
        kbd.press(Keycode.CONTROL, Keycode.EQUALS)
        kbd.release_all()
    else:
        update_oled("Zoom -")
        kbd.press(Keycode.CONTROL, Keycode.MINUS)
        kbd.release_all()

def encoder_button():
    update_oled("Reset Zoom")
    kbd.press(Keycode.CONTROL, Keycode.ZERO)
    kbd.release_all()

while True:
    pos = encoder.position
    delta = pos - last_pos
    if delta != 0:
        encoder_turn(delta)
        last_pos = pos

    enc_now = enc_btn.value
    if enc_btn_last and not enc_now:
        encoder_button()
    enc_btn_last = enc_now

    for i, key in enumerate(keys):
        now = key.value
        if keys_last[i] and not now:
            key_action(i)
        keys_last[i] = now

    time.sleep(0.01)
