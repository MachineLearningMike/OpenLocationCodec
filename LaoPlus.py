from LaoCode import lao_decode, lao_encode
from openlocationcode import decode, encode

def lao_to_plus(lao_string):
    ret = None

    latlon_string = lao_decode(lao_string)
    if latlon_string.startswith('Error'):
        ret = latlon_string
    else:
        latlon_list = latlon_string.split('/');
        lat, lon = float(latlon_list[0]), float(latlon_list[1])

        # Know-how: use 11, which gives appr. 2.8x3.5 meter precision,
        # rather than the default = 10, which gives appr. 13.5x13.5 meter precision.
        # A 13.5x13.5 tile covers/overlaps multiple Lao tiles, complicating things.
        ret = encode(lat, lon, 11) 

    return ret


def plus_to_lao(plus_string):
    ret = None

    code_area = decode(plus_string)
    lat = code_area.latitudeLo # latitudeCenter
    lon = code_area.longitudeLo # longitudeCenter

    lao_string = lao_encode(str(lat) + '/' + str(lon))

    if lao_string.startswith('Error'):
        ret = lao_string
    else:   
        parcel_lo = lao_string

        lat = code_area.latitudeHi # latitudeCenter
        lon = code_area.longitudeHi # longitudeCenter

        lao_string = lao_encode(str(lat) + '/' + str(lon))
        parcel_hi = lao_string

        ret = (parcel_lo, parcel_hi)
    
    return ret
