We are looking for a bright software engineer that could develop an Algorithm to encode and decode the longitude and latitude into a digital address that in a format below.

1. Format
[MP] – [0013] [5590]

[Letter#1 Letter#2] - [Number #1] [Number #2]

With two-letter prefix (English alphabet) - and 2 sets of 4 numbers.

Letter #1: ABDEFGKMNPRSUVWXYZ [18 character available]
Letter #2: NPRSUFGKMVWXYZABDE [18 character available]

Note: The use of Letter #1 and Letter # must base on the order character set above. It can be change or shuffle the order later.

[number #2]: 0000 to 9999
[number #2]: 0000 to 9999


2. Range of the latitude/longitude we will cover only (Laos):
-Latitude of 13 Degree North to 23 Degree North
OR: 13.00000000 to 23.00000000
(1 billion different numbers)
-Longitude of 100degree East to 110 degrees East
Or: 100.00000000 to 110.00000000
(1 billion of different number)

3. Resolution of the longitude and latitude

For Radian Format:
17°58'38.911"N 102°37'35.442"E

Need 3 decimal points for seconds unit for radian format

For decimal format
17.17631315, 104.89793213

Need 8 decimal points for decimal




Available Address:

We know that with this the format we want, we will have about 32.4 billion addresses to cover.

18*18*10^4*10^4 = 32,400,000,000

With longitude/latitude range we need to cover, and with the resolution 8 decimal point we required only 2 billion addresses.

 
Requirement for the address:

Digital Address generation:

Encode:
> Given latitude and longitude as input (must contain 8 decimal points)
> Output as digital address
>If out of the range coverage
>give error message address is not found

Decode:
>Given the Digital Address as input
>Output as longitude and latitude with the same resolution (8 decimal points)

Working with Google Plus code:
Google Plus code is opensource project. You can find the code here

https://github.com/google/open-location-code

https://github.com/google/open-location-code/tree/main/python


Trytobeyou1!
