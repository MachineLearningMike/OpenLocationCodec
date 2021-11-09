
import math,re

'''
The lao geo-coding system encode/decode geographical corrdinates, comprising of latitude and longitute 
of a point on the Earch surface, to/from alphanumeric code in the format of LETTERS - DIGITS1 - DIGITS2. 
(See the file 'requirement.md' for more.)
LETTERS: a number of pre-defined alphanumeric symbols.
DIGITS: a number of pre-defined digits.

e.g.: A lao geo-code 'MP-1234-5678' has 'MP' as LETTERS, '1234' as DIGITS1, and '5678' as DIGITS2.

A lao geo-code Letters is used to name the squair tiles that divide the 2-dimensional coordinate system.
Let's call it the Lao tile system.
'''

'''
LETTERS is composed, or inter-woven, of two lists of letters: latitude letters and longitude leters.
Below are defined the two ordered character sets for the latitude letters and longitude letters, respectively.
Each character is important only in the meaning of its position in the set.
- The length of the sets cannot be zero.
- The length of the sets can different with each other.
- A character cannot appear twice in a set.
- The sets can have shared characters.
'''
LETTERS_LIST_LAT = 'ABDEFGKMNPRSUVWXYZ' # 'VWXYZFGKMNPRSUABDE'
LETTERS_LIST_LON = 'NPRSUFGKMVWXYZABDE' # 'NPRSUFGKMVWXYZABDE'

'''
The latitude boundary and the longitude boundary of the square region that the lao geo-coding system will work on.
A lao geo-code, this, represent a square tile that lies on this regeon.
- LAT_MIN: The lower closed (inclusive) boundary of latitude.
- LAT_MAX: The upper open (exclusive) boundary of latitude.
- LON_MIN: The lower closed (inclusive) boundary of longitude.
- LON_MAX: The upper open (exclusive) boundaty of longitufe.
- Latitude ranges (-80, 90), while longitude ranges [-180, 180).
- 80 here is a recommendation. You can choose 90.
'''
LAT_MIN = 13.00000000
LAT_MAX = 23.00000000

LON_MIN = 100.00000000
LON_MAX = 110.00000000

'''
The number of characters in latitude letters and longitude letters, respectively.
If they are each set to 2, then a lao geo-code will looks like, for example, [MPSD] - ...
- They can be set independently.
- They cannot be zero.
'''
LETTERS_LAT = 1
LETTERS_LON = 1

'''
The numbers of digits in DIGIST1 and DIGITS2, respectively.
They are now set to 4, and the Lao geo-code should look like ...-[1234][5678]
- They can be set independently.
- They canot be zero.
'''
DIGITS_LAT = 4
DIGITS_LON = 4

'''
Latitude and longitude values produced by the lao geo-code system will have DECIMALS decimals.
E.g.: 13.12345678 has 8 decimals.
- It cannot be 0.
'''
DECIMALS = 8

'''
Latitude value is enocded by letters with the base ENC_BASE_LAT, before it is further encoded by digits.
Longitude value is enocded by letters with the base ENC_BASE_LON, before it is further encoded by digits.
E.g. One more letter will encode latitude ENC_BASE_LAT times more precisely.
E.g. 1 letter will divide the range into 18 tiles, and 2 letters will into 18 x 18 tiles, if the length of the set is 18.
'''
ENC_BASE_LAT = len(LETTERS_LIST_LAT)
ENC_BASE_LON = len(LETTERS_LIST_LON)

'''
There are all pow(ENC_BASE_LAT, LETTERS_LAT) possible combinations of letters in the place of latitude letters.
E.g. There are (18, 1) = 18 combinations in the place of latitude letters, 1st character, of [MP], if LETTRS_LAT == 1.
E.g. There are (18, 2) combinations in the place of latitude letters, 1st and 3rd characters, of [MPAS], if LETTRS_LAT == 2.
Each combination is responsible, or represents, LETTER_RES_LAT-wide latitude range.
The whole range (LAT_MAX - LAT_MIN) is divided into pow(ENC_BASE_LAT, LETTERS_LAT) tiles, on latitudal axis.
LETTER_RES_LON is to longitude what LETTER_RES_LAT is to latitude.
'''
LETTER_RES_LAT = (LAT_MAX - LAT_MIN) / pow(ENC_BASE_LAT, LETTERS_LAT)
LETTER_RES_LON = (LON_MAX - LON_MIN) / pow(ENC_BASE_LON, LETTERS_LON)

'''
After the region is tiled, or divided, by letters, each of the tiles is further divided, or tiles, by digits.
If there are 4 possible digits, then pow(10, 4) digit combinations will divide the tile into smaller tiles.
Each combination is responsible and represents DIGIT_RES_LAT-wide latitude, and DIGIT_RES_LON-wide longitude.
'''
DIGIT_RES_LAT = LETTER_RES_LAT / pow(10, DIGITS_LAT)
DIGIT_RES_LON = LETTER_RES_LON / pow(10, DIGITS_LON)

'''
print("MAX", DIGIT_RES_LAT, DIGIT_RES_LON)
Go to this place: https://www.movable-type.co.uk/scripts/latlong.html
Input (13.0, 110.0) and (13.0 + DIGIT_RES_LAT, 110.0 + DIGIT_RES_LON) to find the max error,
'''

'''
lao_decode(code)
- Decodes a lao geo-code to output a geo-coordinate point.
- code: a lao geo-code.
- The output is the geo-coordinates of the bottom-left point on the tile represented by the code.
- If th
'''
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
        
        # The core of the decoding function.
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
                    # The core of the encodeing funciton.
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

