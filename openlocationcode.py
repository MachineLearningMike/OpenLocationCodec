
import math

# The character set used to encode the values.
LETTERS_LIST_LAT = 'ABDEFGKMNPRSUVWXYZ'
LETTERS_LIST_LON = 'NPRSUFGKMVWXYZABDE'

# The maximum value for latitude in degrees.
LAT_MIN = 13.00000000
LATITUDE_MAX = 23.00000000

# The maximum value for longitude in degrees.
LON_MIN = 100.00000000
LONGITUDE_MAX = 110.00000000

# The number of letters in [lettersletters] - [digits][digits]
LETTERS_LAT = 2
LETTERS_LON = 2

# The number of digits in [lettersletters] - [digits][digits]
DIGITS_LAT = 3
DIGITS_LON = 3

# The number of decimals in lat/lon.  (13.21609568, 107.82591049)
DECIMALS = 8

# The base to use to convert numbers to/from.
ENC_BASE_LAT = len(LETTERS_LIST_LAT)
ENC_BASE_LON = len(LETTERS_LIST_LON)

# The geo-resolution gained by letters.
LETTER_RES_LAT = (LATITUDE_MAX - LAT_MIN) / pow(ENC_BASE_LAT, LETTERS_LAT)
LETTER_RES_LON = (LONGITUDE_MAX - LON_MIN) / pow(ENC_BASE_LON, LETTERS_LON)

# The geo-resolution gained by digits.
DIGIT_RES_LAT = LETTER_RES_LAT / pow(10, DIGITS_LAT)
DIGIT_RES_LON = LETTER_RES_LON / pow(10, DIGITS_LON)


def decode(code):
    # "[MP] – [0013] [5590]"
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
        lat_num = 0
        for i in range(len(letters_lat)):
            lat_num += pow(ENC_BASE_LAT, i) * LETTERS_LIST_LAT.find(letters_lat[i].upper())
        lon_num = 0
        for i in range(len(letters_lon)):
            lon_num += pow(ENC_BASE_LON, i) * LETTERS_LIST_LON.find(letters_lon[i].upper())
        
        lat = LAT_MIN + LETTER_RES_LAT * lat_num + DIGIT_RES_LAT * int(digits_lat) + DIGIT_RES_LAT / 2
        lon = LON_MIN + LETTER_RES_LON * lon_num + DIGIT_RES_LON * int(digits_lon) + DIGIT_RES_LON / 2

        lat = round(lat, DECIMALS)
        lon = round(lon, DECIMALS)

        return (lat, lon)
    else:
        return False


def encode(lat, lon):
    ret = None

    if lat < LAT_MIN or LATITUDE_MAX <= lat or lon < LON_MIN or LONGITUDE_MAX <= lon:
        ret = False
    else:
        (lat_letters, lat_digits) = \
        encode_tude(lat, LAT_MIN, LETTER_RES_LAT, DIGIT_RES_LAT, LETTERS_LAT, DIGITS_LAT, ENC_BASE_LAT, LETTERS_LIST_LAT)
        (lon_letters, lon_digits) = \
        encode_tude(lon, LON_MIN, LETTER_RES_LON, DIGIT_RES_LON, LETTERS_LON, DIGITS_LON, ENC_BASE_LON, LETTERS_LIST_LON)

        ret = '[' + lat_letters + lon_letters + '] - [' + lat_digits + '] [' + lon_digits + ']'

    return ret

def encode_tude(tude, min, letter_resolution, digit_resolution, letters, digits, encoding_base, code_alpahbet):
        _letters = ''
        tude -= min
        for i in range(letters-1, -1, -1):
            _num = math.floor( tude / letter_resolution )
            power = pow(encoding_base, i)
            _num = math.floor(_num / power)
            _letters = code_alpahbet[_num] + _letters
            tude = tude - power * letter_resolution * _num
        _digits = str(math.floor(tude / digit_resolution)).zfill(digits)

        return (_letters, _digits)


code = "[AANN] - [000] [000]"
print("code = ", code)

latlon = decode(code)
print("decode(code) = ", latlon)

(lat, lon) = latlon
code = encode(lat, lon)
print("encode(decode(code)) = ", code)

latlon = decode(code)
print("decode(encode(decode(code))) = ", latlon)
