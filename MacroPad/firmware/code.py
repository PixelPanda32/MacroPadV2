import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DirectPinsScanner
from kmk.extensions.peg_oled_display import Oled, OLedData, OledDisplayMode
from kmk.exstensions.rgb import RGB
from kmk.modules.encode import EncoderHandler
from kkmk.modules.layers import Layers

keyboard = KMKKeyboard()

layers_module = Layers()
keyboard.modules.append(layers_module)
encoder_handler = EncoderHandler()
keyboard.module.append(encoder_handler)

keyboard.matrix = DirectPinsScanner(
    pins=[board.GP26, board.GP27, board.GP3, board.GP4, board.GP3]
)

encoder_handler.pins = (
    (board.GP28, board.GP29, none ),
    (board.GP2, board.GP1, none ), 

)
rgb = RGB(pixel_pin=board.GP1, num_pixels=6, val_limit=150, hue=0, sat=255)
keyboard.extension.append(rgb)

i2c_bus = busio.I2C(board.GP6, board.GP7)
oled_display = Oled(
    i2c_bus,
    device_address=0x3C,
    width=128,
    height=32,
    display_mode=OledDisplayMode.TXT
    #im gonna change this in the future to prolly image or video js cus coooler 
)
keyboard.extensions.append(oled_display)


LAYER_DISCORD = 0
LAYER_SPOTIFY = 1
LAYER_PRODUCTIVITY = 2
LAYER_CUSTOM = 3

LAYER_COLORS = {
    LAYER_DISCORD: (0, 0, 255),
    LAYER_SPOTIFY: (0, 255, 0),
    LAYER_PRODUCTIVITY: (255,0,0), #I will change this to better suit what the colors of the neopixels look like when on 
    LAYER_CUSTOM: (128,0,128)
}
DISCORD_MUTE = KC.LALT(KC.LSHIFT(KC.M))
DISCORD_DEAFEN = KC.KALT(KC.LSHIFT(KC.D))

keyboard.keymap = [
    [DISCORD_MUTE, DISCORD_DEAFEN, KC.MNXT, KC.MPRV],
    [KC.MPLY, KC.MUTE, KC.VOLD, KC.VOLU],
    [KC.LCTL(KC.X), KC.LCTL(KC.LSHIFT(KC.T)), KC.LTCTL(KC.V), KC.LTCTL(KC.C)]
    [KC.NO, KC.NO, KC.NO, KC.NO]#dunnno what to do for these but will think of smth

]
encoder_handler.map = [
    ((KC.VOLD,KC.VOLU, KC.NO), (KC.TG(LAYER_SPOTIFY), KC.TG(LAYER_CUSTOM), KC.NO)),
    ((KC.VOLD,KC.VOLU, KC.NO), (KC.TG(LAYER_PRODUCTIVITY), KC.TG(LAYER_DISCORD), KC.NO)),
    ((KC.VOLD,KC.VOLU, KC.NO), (KC.TG(LAYER_CUSTOM), KC.TG(LAYER_CUSTOM), KC.NO)),
    ((KC.VOLD,KC.VOLU, KC.NO), (KC.TG(LAYER_DISCORD), KC.TG(LAYER_PRODUCTIVITY), KC.NO)),    

]

last_layer = -1

def layer_led_sentinel():
    global last_layer
    current_layer = layers_module.current_layer
    if current_layer != last_layer:
        color = LAYER_COLORS.get(current_layer, (255, 255, 255))
        for i in range(6):
            rgb.set_rgb_fill(color, color, color)
        last_layer = current_layer

keyboard.before_matrix_scan_functions.append(layer_led_sentinel)

if __name__ == '__main__':
    keyboard.go()