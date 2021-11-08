
import math,re

# The character set used to encode the values.
LETTERS_LIST_LAT = 'ABDEFGKMNPRSUVWXYZ'
LETTERS_LIST_LON = 'NPRSUFGKMVWXYZABDE'

# The maximum value for latitude in degrees.
LAT_MIN = 13.00000000
LAT_MAX = 23.00000000

# The maximum value for longitude in degrees.
LON_MIN = 100.00000000
LON_MAX = 110.00000000

# The number of letters in [lettersletters] - [digits][digits]
LETTERS_LAT = 1
LETTERS_LON = 1

# The number of digits in [lettersletters] - [digits][digits]
DIGITS_LAT = 4
DIGITS_LON = 4

# The number of decimals in lat/lon.  (13.21609568, 107.82591049)
DECIMALS = 8

# The base to use to convert numbers to/from.
ENC_BASE_LAT = len(LETTERS_LIST_LAT)
ENC_BASE_LON = len(LETTERS_LIST_LON)

# The geo-resolution gained by letters.
LETTER_RES_LAT = (LAT_MAX - LAT_MIN) / pow(ENC_BASE_LAT, LETTERS_LAT)
LETTER_RES_LON = (LON_MAX - LON_MIN) / pow(ENC_BASE_LON, LETTERS_LON)

# The geo-resolution gained by digits.
DIGIT_RES_LAT = LETTER_RES_LAT / pow(10, DIGITS_LAT)
DIGIT_RES_LON = LETTER_RES_LON / pow(10, DIGITS_LON)


def lao_decode(code): # sample: "[MP] – [0013] [5590]"
    ret = True
    letters_lat = letters_lon = digits_lat = digits_lon = None

    if len(code) != 1 + LETTERS_LAT + LETTERS_LON + 5 + DIGITS_LAT + 3 + DIGITS_LON + 1:
        ret = False
    else:
        # parse "["
        start = 0; end = start + 1
        if code[start : end] != '[':
            ret = False

        # extract latitude letters
        if ret != False:
            start = end; end = start + LETTERS_LAT
            letters_lat = code[start : end]
            for i in range(len(letters_lat)):
                if LETTERS_LIST_LAT.find(letters_lat[i].upper()) < 0:
                    ret = False
                    break

        # extract longitude letters
        if ret != False:
            start = end; end = start + LETTERS_LON
            letters_lon = code[start : end]
            for i in range(len(letters_lon)):
                if LETTERS_LIST_LON.find(letters_lon[i].upper()) < 0:
                    ret = False
                    break

        # parse "] - ["
        start = end; end = start + 5
        if code[start : end] != '] - [':
            ret = False

        # extract latitude digits
        if ret != False:
            start = end; end = start + DIGITS_LAT
            digits_lat = code[start : end]
            for i in range(len(digits_lat)):
                if not digits_lat[i].isnumeric():
                    ret = False
                    break

        # parse "] ["
        if ret != False:
            start = end; end = start + 3
            if code[start : end] != '] [':
                ret = False

        # extract longitude digits
        if ret != False:
            start = end; end = start + DIGITS_LON
            digits_lon = code[start : end]
            for i in range(len(digits_lat)):
                if not digits_lon[i].isnumeric():
                    ret = False
                    break

        # parse "]"
        if ret != False:
            start = end; end = start + 1
            if code[start : end] != ']':
                ret = False
    
    if ret is True:
        lat, lon = _decode(letters_lat, digits_lat, letters_lon, digits_lon)
        lat = format(round(lat, DECIMALS), "." + str(DECIMALS) + "f")
        lon = format(round(lon, DECIMALS), "." + str(DECIMALS) + "f")

        return lat + '/' + lon
    else:
        return False


def _decode(letters_lat, digits_lat, letters_lon, digits_lon):
    lat_num = 0
    for i in range(len(letters_lat)):
        lat_num += pow(ENC_BASE_LAT, i) * LETTERS_LIST_LAT.find(letters_lat[i].upper())
    lon_num = 0
    for i in range(len(letters_lon)):
        lon_num += pow(ENC_BASE_LON, i) * LETTERS_LIST_LON.find(letters_lon[i].upper())
    
    lat = LAT_MIN + LETTER_RES_LAT * lat_num + DIGIT_RES_LAT * int(digits_lat) + DIGIT_RES_LAT / 2 #----- Know-how 1
    lon = LON_MIN + LETTER_RES_LON * lon_num + DIGIT_RES_LON * int(digits_lon) + DIGIT_RES_LON / 2 #----- Know-how 2

    return lat, lon


def lao_encode(latlon_string): # sample "16.88963889\100.86613889"
    ret = None

    lat = lon = None
    inputlist = latlon_string.split('/')
    if len(inputlist) == 2:
        if re.match(r'^-?\d+(?:\.\d+)$', inputlist[0]) is not None:
            if re.match(r'^-?\d+(?:\.\d+)$', inputlist[1]) is not None:
                [lat, lon] = [float(inputlist[0]), float(inputlist[1])]

                # Know-how
                lat = mitigate_borders(lat, LAT_MIN, LAT_MAX, DIGIT_RES_LAT/10)
                lon = mitigate_borders(lon, LON_MIN, LON_MAX, DIGIT_RES_LON/10)

                if lat < LAT_MIN or LAT_MAX <= lat or lon < LON_MIN or LON_MAX <= lon:
                    ret = "Error: Latitude or longitude is out of Laos range: [13.0, 23.0) x [100.0, 110.0)"
                else:
                    lat_letters, lon_letters, lat_digits, lon_digits = _encode(lat, lon)
                    ret = '[' + lat_letters + lon_letters + '] - [' + lat_digits + '] [' + lon_digits + ']'
            else:
                ret = "Error: Longitude is not a demical number."
        else:
            ret = "Error: Latitude is not a decimal number."
    else:
        ret = "Error: Format is wrong."

    return ret

def mitigate_borders(point, low_closed_border, high_open_border, tolerance):
    if point < low_closed_border and point + tolerance >= low_closed_border:
        point = point + tolerance
    if point >= high_open_border and point - tolerance < high_open_border:
        point = point - tolerance
    return point

def _encode(lat, lon):
    #lat += DIGIT_RES_LAT / 2 #----- Know-how 3
    #lon += DIGIT_RES_LON / 2 #----- Know-how 4
    (lat_letters, lat_digits) = \
    _lao_encode_tude(lat, LAT_MIN, LETTER_RES_LAT, DIGIT_RES_LAT, LETTERS_LAT, DIGITS_LAT, ENC_BASE_LAT, LETTERS_LIST_LAT)
    (lon_letters, lon_digits) = \
    _lao_encode_tude(lon, LON_MIN, LETTER_RES_LON, DIGIT_RES_LON, LETTERS_LON, DIGITS_LON, ENC_BASE_LON, LETTERS_LIST_LON)

    return lat_letters, lon_letters, lat_digits, lon_digits

def _lao_encode_tude(tude, min, letter_resolution, digit_resolution, letters, digits, encoding_base, code_alpahbet):
        _letters = ''
        tude -= min
        for i in range(letters-1, -1, -1):
            _num = math.floor( tude / letter_resolution )
            power = pow(encoding_base, i)
            _num = math.floor(_num / power)
            _letters = code_alpahbet[_num] + _letters
            tude = tude - power * letter_resolution * _num
        _digits = str(math.floor(tude / digit_resolution)).zfill(digits) #----- Know-how 5: round than floor

        return (_letters, _digits)

