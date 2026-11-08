"""Character set definitions for ASCII rendering"""

CHARSETS = {
    'standard': {
        'name': 'Standard',
        'chars': ' .:-=+*#%@',
        'description': 'Standard ASCII density characters'
    },
    'blocks': {
        'name': 'Blocks',
        'chars': ' ░▒▓█',
        'description': 'Block characters'
    },
    'dots': {
        'name': 'Dots',
        'chars': ' .·∙○●',
        'description': 'Dot matrix pattern'
    },
    'binary': {
        'name': 'Binary',
        'chars': ' 01',
        'description': 'Binary 01'
    },
    'donut': {
        'name': 'Donut',
        'chars': ' .\'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$',
        'description': 'Donut optimized charset'
    },
    'photo': {
        'name': 'Photo',
        'chars': ' .\'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$',
        'description': 'Photographic rendering'
    },
    'bars': {
        'name': 'Bars',
        'chars': ' ▏▎▍▌▋▊▉█',
        'description': 'Bar graph style'
    },
    'shade': {
        'name': 'Shade',
        'chars': ' ░▒▓█',
        'description': 'Shading characters'
    },
    'braille': {
        'name': 'Braille',
        'chars': '⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿',
        'description': 'Braille patterns'
    },
    'stars': {
        'name': 'Stars',
        'chars': ' .·*+xX*★',
        'description': 'Star characters'
    },
    'circles': {
        'name': 'Circles',
        'chars': ' .○◐◑◒◓◔◕●',
        'description': 'Circle characters'
    }
}

def get_charset(name: str):
    """Get charset by name"""
    return CHARSETS.get(name.lower(), CHARSETS['standard'])

def list_charsets():
    """Return list of available charsets"""
    return list(CHARSETS.keys())
