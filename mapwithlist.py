from codecs import latin_1_decode
from fileinput import filename
import json
import folium
import geopy.distance
import math
import webbrowser
from geopy.geocoders import ArcGIS
from urllib.request import urlopen
import pymongo
nom = ArcGIS()
def generate_mapwithlist():

    # client = pymongo.MongoClient("mongodb://localhost:27017/")
    client = pymongo.MongoClient("mongodb+srv://hiimanshu:himanshu@fastlance.fmvuepr.mongodb.net/test")
    mydb = client["ambulance"]
    mycol = mydb["hospital"]


    loc = "19.2063, 72.8746"

    s = loc.split(',')
    lat = s[0]
    lon = s[1]
    coords_1 = (lat, lon)

    li1 = []
    li2 = []

    filcol = mycol.find()
    for z in filcol:
        if(math.isnan(z['latitude']) == False and math.isnan(z['longitude']) == False):
            coords_2 = (z['latitude'], z['longitude'])
            dis = geopy.distance.geodesic(coords_1, coords_2).km
            if(dis < 100):
                li1.append({'longitude': z['longitude'],
                        'latitude': z['latitude'],'Name': z['Health Facility Name']})
                li2.append(
                    {'Name': z['Health Facility Name'], 'Distance': int(int(dis)*1.12)})


    # Map ka code
    hos_map = folium.Map(location=[lat, lon], zoom_start=12)

    fg = folium.FeatureGroup(name='Himanshu')

    for i in li1:

        fg.add_child(folium.Marker(
            location=[i['latitude'], i['longitude']],popup=i['Name'], icon=folium.Icon(color='red', icon='hospital', prefix='fa'))) 

    fg.add_child(folium.Marker(
        location=[lat, lon], icon=folium.Icon(color='blue'),popup="Your Location"))


    hos_map.add_child(fg)

    hos_map.save('hos1map.html')

    # MAP END

    # List Ka Code
    li2.sort(key=lambda x: x["Distance"])
    tbl = ""
    c=0
    for y in li2:
        if c==8:
            break

        c=c+1
        a = "<tr onclick=window.location='confirmation.html';><td class='hfn'>%s<td>" %y['Name']
        b = "<td>%s</td></tr>" %y['Distance']
        tbl = tbl+a+b


    contents = '''<!DOCTYPE html>
    <html lang="en">
    <html>
    <head>
    <script src="https://kit.fontawesome.com/de9d45e1c6.js" crossorigin="anonymous"></script>
    <meta http-equiv="content-type">
    <link rel="stylesheet" href="mapliststyle.css">
    <title>Hospital</title>
    </head>
    <body>
    <div class="twoparts">
        <div class="container">
            <div class="containerhead">
                <label for="Search" class="label1">Choose a Hospital</label>
                    <form action="" class="searchbar">
                    <input type="text" id="myinput" placeholder="Search Nearby Hospitals....." onkeyup="searchFun()">
                    </form>
                <label for="mention" class="label2">Nearby Hospitals</label>
            </div>
    <table  id="mytable">
    %s
    </table>
    <div class="button">
        <a type="button" onclick=window.location='confirmation.html' class="btn">BOOK AMBULANCE</a>
    </div>    
        </div>
        <div class = container2>
            <iframe src="hos1map.html" width="1700px" height="900" >
        </iframe>
        </div>

        </div>
        <script>
            const searchFun = () => {
                let filter = document.getElementById('myinput').value.toUpperCase();

                let myTable = document.getElementById('mytable');

                let tr = myTable.getElementsByTagName('tr');

                for (var i = 0; i < tr.length; i++) {
                    let td = tr[i].getElementsByTagName('td')[0];

                    if (td) {
                        let textvalue = td.textContent || td.innerHTML;

                        if (textvalue.toUpperCase().indexOf(filter) > -1) {
                            tr[i].style.display = "";
                        }
                        else 
                        {
                            tr[i].style.display = "none";
                        }
                    }
                }
            }
            </script>
            <script>
             $("tr").click
             (
             window.location = "confirmation.html"
             );
            </script>
    </body>
    </html>
    ''' % (tbl)

    filename = 'info.html'

    # List Code End


    def main(contents, filename):
        output = open(filename, "w")
        output.write(str(contents))
        output.close()


    main(contents, filename)

    webbrowser.open(filename)
    # webbrowser.open('info.html')

# generate_mapwithlist()

# window.location = "confirmation.html";