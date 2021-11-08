from LaoCode import lao_decode, lao_encode
from openlocationcode import decode, encode

def lao_to_plus(lao_string):
    ret = None

    latlon_string = lao_decode(lao_string)
    if latlon_string is False:
        ret = False
    else:
        latlon_list = latlon_string.split('/');
        lat, lon = float(latlon_list[0]), float(latlon_list[1])
        ret = encode(lat, lon)

    return ret


def plus_to_lao(plus_string):
    ret = None

    code_area = decode(plus_string)
    lat = code_area.latitudeLo # latitudeCenter
    lon = code_area.longitudeLo # longitudeCenter

    lao_string = lao_encode(str(lat) + '/' + str(lon))
    ret = lao_string
    
    return ret
