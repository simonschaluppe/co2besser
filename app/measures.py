"""
CO2-Maßnahmen:
=============
Big Idea:   Create CO2-Saving measures as Database obejcts
            from the inhomogenous CO2-Emission Data
            provided by a number of excels on Christof
            Drexel's www.zwei-grad-eine-tonne.at

Topics:
=======
* Gather all Excels
"""

# Gathering the excels
excel_title = "Abschnitt%20I%20Verkehr"
file_name = f'static\{excel_title}.xlsx'
import requests
dls = "https://www.zwei-grad-eine-tonne.at/XooWebKit/bin/download.php/2cee1_22c27c0a42/Abschnitt%20I%20Verkehr.xlsx"
resp = requests.get(dls)
with open(file_name, 'wb') as output:
    output.write(resp.content)


if __name__ == "__main__":
    print("Hello World")