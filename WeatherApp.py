import requests
import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit

###NOTRE GUI !!!!!!
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # setting title
        self.setWindowTitle("WeatherApp ")

        # setting geometry
        self.setGeometry(100, 100, 500, 200)
        #calling method
        self.UIcomponents()
        #showing all the widgets
        self.show()

    def UIcomponents(self):
        self.label = QLabel('Tapez le nom d\'une ville : ', self)
        self.label.setGeometry(10,0,250,40)

        self.label2 = QLabel('', self)
        self.label2.setGeometry(0,70,250,40)

        self.label3 = QLabel('', self)
        self.label3.setGeometry(0,90,250,40)
        
        self.label4 = QLabel('', self)
        self.label4.setGeometry(0,110,250,40)

        self.label5 = QLabel('', self)
        self.label5.setGeometry(0, 130, 250, 40)

        self.line = QLineEdit(self)
        self.line.setGeometry(160, 10, 250, 25)

        button = QPushButton("Valider", self)
        button.setGeometry(160, 50, 100, 25)

        # adding action to a button
        button.clicked.connect(self.findCity)

    def findCity(self):
        city = self.line.text()
        cityInfo = requests.get('http://api.openweathermap.org/geo/1.0/direct?q=' + city +'&limit=1&appid={APPID}').json()
        lat = []
        lon = []
        #On a besoin de la latitude et de la longitude de la ville
        for i in cityInfo:
            lat.append(i['lat'])
            lon.append(i['lon']) 
        
        #On convertit ces listes récupérées en float !!
        lat = float(''.join(map(str, lat)))
        lon = float(''.join(map(str, lon)))
        #On appelle la fonction qui nous permettra de récupérer la température de la ville
        self.findTemperature(lat,lon)

    def findTemperature(self, lat, lon):

        #On arrondit la latitude et la longitude
        round_lat = round(lat, 2)
        round_lon = round(lon, 2)
        
        weather = []
        temp = []
        humidity = []
        windspeed = []
        temperature = requests.get('https://api.openweathermap.org/data/2.5/weather?lat='+ str(round_lat) + '&lon=' + str(round_lon) + '&appid={APPID}').json()
        
       # print(temperature)
        
        temp.append(temperature['main']['temp'])      
        humidity.append(temperature['main']['humidity'])
        weather.append(temperature['weather'][0]['description'])

        windspeed.append(temperature['wind']['speed'])
        
        #On transforme la description en variable globale sous forme de chaîne
        strweather = ''.join(weather)
        

        #A convertir en celsius
        
        tempkelvin = float(''.join(map(str, temp)))
        tempcelsius = round((tempkelvin - 273.15), 1 )
        
        strtemp =str(tempcelsius)

        print(temperature)
        #Rajouter pourcentage
        strhumidity = str(''.join(map(str, humidity)))


        #On convertir en km heure
        intwindspeed = float(''.join(map(str, windspeed)))
        windspeedkilometers = round((intwindspeed * 1.609),2)
        strwindspeed = str(windspeedkilometers)


        self.label2.setText("Description : " + strweather)
        self.label3.setText("Temperature : " + strtemp+ " C° ")
        self.label4.setText("Humidity : " + strhumidity + " %")
        self.label5.setText("Windspeed : " + strwindspeed + " KM/Heure")
        
        




#Création de l'application
app = QApplication(sys.argv)
#On instancie la classe que l'on vient de créer
win = Window()
 
#Démarrage de l'app
sys.exit(app.exec_())