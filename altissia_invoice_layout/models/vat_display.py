import re

#Create a fancy display for vat with "space" between dgiits and letter (request #1944)
def vat_display(vat):
    if len(vat) > 3 and vat[0:3] == 'ESB':
        return vat[0:2] + " " + vat[2:]
    else:
        return " ".join(re.split('(\d+)',vat))


