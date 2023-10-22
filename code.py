import board
import busio
from digitalio import DigitalInOut, Direction, Pull

from adafruit_mcp230xx.mcp23017 import MCP23017
from kmk.hid import HIDModes
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.layers import Layers
from kmk.scanners import DiodeOrientation
from kmk.scanners.digitalio import MatrixScanner
from kmk.modules.mouse_keys import MouseKeys
# from kmk.modules.pmw3360 import PMW3360
import gc

gc.collect()
print(str(gc.mem_free())+"        ")

i2c = busio.I2C(scl=board.D1, sda=board.D0, frequency=100000)

from kmk.extensions.peg_oled_Display import Oled,OledDisplayMode,OledReactionType,OledData
oled_ext = Oled(
    OledData(
        corner_one={0:OledReactionType.STATIC,1:["layer"]},
        corner_two={0:OledReactionType.LAYER,1:["1","2","3","4"]},
        corner_three={0:OledReactionType.LAYER,1:["base","raise","lower","adjust"]},
        corner_four={0:OledReactionType.LAYER,1:["qwerty","nums","shifted","leds"]}
        ),
        toDisplay=OledDisplayMode.TXT,flip=False)


# DEBUG_ENABLE = True
print("starting")


mcp = MCP23017(i2c, address=0x20)
class MyKeyboard(KMKKeyboard):
    def __init__(self):
        # create and register the scanner
        self.matrix = MatrixScanner(
            cols=(mcp.get_pin(0), mcp.get_pin(1), mcp.get_pin(2), mcp.get_pin(3), mcp.get_pin(4), mcp.get_pin(5), mcp.get_pin(6), mcp.get_pin(7), mcp.get_pin(8), mcp.get_pin(9), mcp.get_pin(10)),
            rows=(mcp.get_pin(11), mcp.get_pin(12), mcp.get_pin(13), mcp.get_pin(14)),
            diode_orientation=DiodeOrientation.COLUMNS,
            pull=Pull.UP,
            rollover_cols_every_rows=None, # optional
        )

keyboard = MyKeyboard()
keyboard.SCL = board.SCL
keyboard.SDA = board.SDA
layer_ext = Layers()

# gc.collect()
# print(str(gc.mem_free())+" gc before pmw3360       ")

# pmw3360 = PMW3360(cs=board.D7, miso=board.MISO, mosi=board.MOSI, sclk=board.SCK, invert_x=True, invert_y=True, flip_xy=True)

# gc.collect()
# print(str(gc.mem_free())+" gc AFTER pmw3360       ")

# if str(getmount('/').label).endswith('R'):
keyboard.modules = [layer_ext, oled_ext, MouseKeys()]

_______ = KC.TRNS
XXXXXXX = KC.NO

FN = KC.MO(1)

keyboard.debug_enabled = True
#]keyboard.col_pins = (board.D0, board.D1)
# keyboard.row_pins = (board.D2, board.D3)
keyboard.diode_orientation = DiodeOrientation.COLUMNS

keyboard.keymap = [
    # Qwerty
    # ,--------------------------------------------------------------------------------------------------------.
    # |   `  |   1  |   2  |   3  |   4  |   5  |   6  |   7  |   8  |   9  |   0  |   -  |   =  | Bksp | Del  |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Tab  |   Q  |   W  |   E  |   R  |   T  |   Y  |   U  |   I  |   O  |   P  |   [  |   ]  |   \  | PgUp |
    # |------+------+------+------+------+-------------+------+------+------+------+------+------+------+------|
    # | Esc  |   A  |   S  |   D  |   F  |   G  |   H  |   J  |   K  |   L  |   ;  |   '  |      |Enter | PgDn |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Shift|   Z  |   X  |   C  |   V  |   B  |   N  |   M  |   ,  |   .  |   /  |Shift |      |  Up  | Ins  |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Ctrl | GUI |  Alt  |      |      |Space |      |      |  Fn  | Alt  | Ctrl | Left |      | Down | Right|
    # `------------------------------------------------------------------------------------------+------+------'
    [
        KC.GRV,  KC.N1,   KC.N2,   KC.N3,   KC.N4,     KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,
        KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,      KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,
        KC.ESC,  KC.A,    KC.S,    KC.D,    KC.F,      KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN,
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,      KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH
    ],
        # Qwerty
    # ,--------------------------------------------------------------------------------------------------------.
    # |   `  |   1  |   2  |   3  |   4  |   5  |   6  |   7  |   8  |   9  |   0  |   -  |   =  | Bksp | Del  |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Tab  |   Q  |   W  |   E  |   R  |   T  |   Y  |   U  |   I  |   O  |   P  |   [  |   ]  |   \  | PgUp |
    # |------+------+------+------+------+-------------+------+------+------+------+------+------+------+------|
    # | Esc  |   A  |   S  |   D  |   F  |   G  |   H  |   J  |   K  |   L  |   ;  |   '  |      |Enter | PgDn |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Shift|   Z  |   X  |   C  |   V  |   B  |   N  |   M  |   ,  |   .  |   /  |Shift |      |  Up  | Ins  |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Ctrl | GUI |  Alt  |      |      |Space |      |      |  Fn  | Alt  | Ctrl | Left |      | Down | Right|
    # `------------------------------------------------------------------------------------------+------+------'
    [
        KC.GRV,  KC.N1,   KC.N2,   KC.N3,   KC.N4,     KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,
        KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,      KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,
        KC.ESC,  KC.A,    KC.S,    KC.D,    KC.F,      KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN,
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,      KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH
    ]
]

if __name__ == '__main__':
    print("In Main")
    gc.collect()
    print(str(gc.mem_free())+" after init       ")
    keyboard.go(hid_type=HIDModes.BLE, ble_name='KMKeyboard')

