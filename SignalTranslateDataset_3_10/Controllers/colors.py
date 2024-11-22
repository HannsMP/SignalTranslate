codes = {
    "reset": [0, 0],

    "bold": [1, 22],
    "dim": [2, 22],
    "italic": [3, 23],
    "underline": [4, 24],
    "inverse": [7, 27],
    "hidden": [8, 28],
    "strikethrough": [9, 29],

    "black": [30, 39],
    "red": [31, 39],
    "green": [32, 39],
    "yellow": [33, 39],
    "blue": [34, 39],
    "magenta": [35, 39],
    "cyan": [36, 39],
    "white": [37, 39],
    "gray": [90, 39],
    "grey": [90, 39],

    "brightRed": [91, 39],
    "brightGreen": [92, 39],
    "brightYellow": [93, 39],
    "brightBlue": [94, 39],
    "brightMagenta": [95, 39],
    "brightCyan": [96, 39],
    "brightWhite": [97, 39],

    "bgBlack": [40, 49],
    "bgRed": [41, 49],
    "bgGreen": [42, 49],
    "bgYellow": [43, 49],
    "bgBlue": [44, 49],
    "bgMagenta": [45, 49],
    "bgCyan": [46, 49],
    "bgWhite": [47, 49],
    "bgGray": [100, 49],
    "bgGrey": [100, 49],

    "bgBrightRed": [101, 49],
    "bgBrightGreen": [102, 49],
    "bgBrightYellow": [103, 49],
    "bgBrightBlue": [104, 49],
    "bgBrightMagenta": [105, 49],
    "bgBrightCyan": [106, 49],
    "bgBrightWhite": [107, 49],

    "blackBG": [40, 49],
    "redBG": [41, 49],
    "greenBG": [42, 49],
    "yellowBG": [43, 49],
    "blueBG": [44, 49],
    "magentaBG": [45, 49],
    "cyanBG": [46, 49],
    "whiteBG": [47, 49],
}


def styleText(code="reset", text=""):
    c = codes[code]
    return f"\u001b[{c[0]}m{text}\u001b[{c[1]}m"

def bold(text):
    return styleText("bold", text)


def dim(text):
    return styleText("dim", text)


def italic(text):
    return styleText("italic", text)


def underline(text):
    return styleText("underline", text)


def inverse(text):
    return styleText("inverse", text)


def hidden(text):
    return styleText("hidden", text)


def strikethrough(text):
    return styleText("strikethrough", text)

def black(text):
    return styleText("black", text)


def red(text):
    return styleText("red", text)


def green(text):
    return styleText("green", text)


def yellow(text):
    return styleText("yellow", text)


def blue(text):
    return styleText("blue", text)


def magenta(text):
    return styleText("magenta", text)


def cyan(text):
    return styleText("cyan", text)


def white(text):
    return styleText("white", text)


def gray(text):
    return styleText("gray", text)


def grey(text):
    return styleText("grey", text)


def brightRed(text):
    return styleText("brightRed", text)


def brightGreen(text):
    return styleText("brightGreen", text)


def brightYellow(text):
    return styleText("brightYellow", text)


def brightBlue(text):
    return styleText("brightBlue", text)


def brightMagenta(text):
    return styleText("brightMagenta", text)


def brightCyan(text):
    return styleText("brightCyan", text)


def brightWhite(text):
    return styleText("brightWhite", text)


def bgBlack(text):
    return styleText("bgBlack", text)


def bgRed(text):
    return styleText("bgRed", text)


def bgGreen(text):
    return styleText("bgGreen", text)


def bgYellow(text):
    return styleText("bgYellow", text)


def bgBlue(text):
    return styleText("bgBlue", text)


def bgMagenta(text):
    return styleText("bgMagenta", text)


def bgCyan(text):
    return styleText("bgCyan", text)


def bgWhite(text):
    return styleText("bgWhite", text)


def bgGray(text):
    return styleText("bgGray", text)


def bgGrey(text):
    return styleText("bgGrey", text)


def bgBrightRed(text):
    return styleText("bgBrightRed", text)


def bgBrightGreen(text):
    return styleText("bgBrightGreen", text)


def bgBrightYellow(text):
    return styleText("bgBrightYellow", text)


def bgBrightBlue(text):
    return styleText("bgBrightBlue", text)


def bgBrightMagenta(text):
    return styleText("bgBrightMagenta", text)


def bgBrightCyan(text):
    return styleText("bgBrightCyan", text)


def bgBrightWhite(text):
    return styleText("bgBrightWhite", text)


def blackBG(text):
    return styleText("blackBG", text)


def redBG(text):
    return styleText("redBG", text)


def greenBG(text):
    return styleText("greenBG", text)


def yellowBG(text):
    return styleText("yellowBG", text)


def blueBG(text):
    return styleText("blueBG", text)


def magentaBG(text):
    return styleText("magentaBG", text)


def cyanBG(text):
    return styleText("cyanBG", text)


def whiteBG(text):
    return styleText("whiteBG", text)