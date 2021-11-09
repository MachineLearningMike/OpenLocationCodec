from LaoCode import lao_decode, lao_encode
from LaoPlus import lao_to_plus, plus_to_lao
import haversine as hs

print("===================== Test lao_to_latlon and reverse =================")
while True:
    lao_string = str(input("Enter a Lao code to convert into Lat/Lon, or 'q' to quit: "))
    if lao_string == 'q': break

    latlon_string = lao_decode(lao_string)
    if latlon_string is False:
        print("\tWrong format.")
    else:
        # Call LaoCode.decode
        print("\tlao_decode({}) = {}".format(lao_string, latlon_string))
        lao_string = lao_encode(latlon_string)
        if lao_string.startswith("Error"):
            print('\t' + lao_string)
        else:
            print("\tlao_encode({}) = {}".format(latlon_string, lao_string))

print("===================== Test latlon_to_lao and reverse =================")
while True:
    latlon_string = str(input("Enter a 'Lat/Lon' value to convert into a Lao code, or 'q' to quit: "))
    if latlon_string == 'q': break

    lao_string = lao_encode(latlon_string)
    if lao_string.startswith("Error"):
        print('t' + lao_string)
    else:
        print("\tlao_encode({}) = {}".format(latlon_string, lao_string))
        latlon_string2 = lao_decode(lao_string)
        if latlon_string2 is False:
            print("\tWrong format.")
        else:
            print("\tlao_decode({}) = {}".format(lao_string, latlon_string2))
        
            strlist, strlist2 = latlon_string.split('/'), latlon_string2.split('/')
            lat, lon, lat2, lon2 = float(strlist[0]), float(strlist[1]), float(strlist2[0]), float(strlist2[1])
            error_meter = hs.haversine( (lat, lon), (lat2, lon2) )
            print("Error_meter = ", error_meter)

print("===================== Test lao_to_plus and reverse ==========================")
while True:
    lao_string = str(input("Enter a Lao code to convert into a Plus code, or 'q' to quit: "))
    if lao_string == 'q': break

    plus_string = lao_to_plus(lao_string)
    if plus_string is False:
        print("\tWrong format.")
    else:
        print("\tlao_to_plus({}) = {}".format(lao_string, plus_string))

        (lao_string_lo, lao_string_hi) = plus_to_lao(plus_string)
        plus_string_lo = lao_to_plus(lao_string_lo)
        plus_string_hi = lao_to_plus(lao_string_hi)
        print("\tplus_to_lao({}) = {}".format(plus_string, lao_string_lo + " to " + lao_string_hi))
        print("\tlao_to_plus({}) = {}".format(lao_string_lo, lao_to_plus(lao_string_lo)))
        print("\tlao_to_plus({}) = {}".format(lao_string_hi, lao_to_plus(lao_string_hi)))


print("===================== Test plus_to_lao and reverse ==========================")
while True:
    plus_string = str(input("Enter a Plus code to convert into a Lao code, or 'q' to quit: "))
    if plus_string == 'q': break

    (lao_string_lo, lao_string_hi) = plus_to_lao(plus_string)
    plus_string_lo = lao_to_plus(lao_string_lo)
    plus_string_hi = lao_to_plus(lao_string_hi)
    print("\tplus_to_lao({}) = {}".format(plus_string, lao_string_lo + " to " + lao_string_hi))
    print("\tlao_to_plus({}) = {}".format(lao_string_lo, lao_to_plus(lao_string_lo)))
    print("\tlao_to_plus({}) = {}".format(lao_string_hi, lao_to_plus(lao_string_hi)))


from openlocationcode import decode, encode

print("===================== Test plus_to_latlon and reverse ==============")
while True:
    plus_string = str(input("Enter a Plus code to convert into Lat/Lon, or 'q' to quit: "))
    if plus_string == 'q': break

    area = decode(plus_string)
    lat, lon = area.latitudeLo, area.longitudeLo
    print("\tdecode({} = {}/{}".format(plus_string, lat, lon))
    print("\tencode({}, {}) = {}".format(lat, lon, encode(lat, lon, 11))) # Know-how: 11 not the dafault = 10.