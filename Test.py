import re
from LaoCode import lao_decode, lao_encode
from LaoPlus import lao_to_plus, plus_to_lao

while True:
    print("===================== Test lao_to_latlon and reverse =================")
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

while True:
    print("===================== Test latlon_to_lao and reverse =================")

    latlon_string = str(input("Enter a 'Lat/Lon' value to convert into a Lao code, or 'q' to quit: "))
    if latlon_string == 'q': break

    lao_string = lao_encode(latlon_string)
    if lao_string.startswith("Error"):
        print('t' + lao_string)
    else:
        print("\tlao_encode({}) = {}".format(latlon_string, lao_string))
        latlon_string = lao_decode(lao_string)
        if latlon_string is False:
            print("\tWrong format.")
        else:
            print("\tlao_decode({}) = {}".format(lao_string, latlon_string))


while True:
    print("===================== Test lao_to_plus ==========================")

    lao_string = str(input("Enter a Lao code to convert into a Plus code, or 'q' to quit: "))
    if lao_string == 'q': break

    plus_string = lao_to_plus(lao_string)
    if plus_string is False:
        print("\tWrong format.")
    else:
        print("\tlao_to_plus({}) = {}".format(lao_string, plus_string))


while True:
    print("===================== Test plus_to_lao ==========================")

    plus_string = str(input("Enter a Plus code to convert into a Lao code, or 'q' to quit: "))
    if plus_string == 'q': break

    lao_string = plus_to_lao(plus_string)

    print("\tplus_to_lao({}) = {}".format(plus_string, lao_string))