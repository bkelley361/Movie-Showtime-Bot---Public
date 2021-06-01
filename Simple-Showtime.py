from bs4 import BeautifulSoup
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

######################################################################################################
#
# Logs the user into their email address. Assuming they have everything turned on to do so
#
######################################################################################################

MY_ADDRESS = "Your Email Here"
MY_PASSWORD = "Your Password Here"
s = smtplib.SMTP(host="Your Host Here", port="Your Port Here")
s.starttls()
s.login(MY_ADDRESS, MY_PASSWORD)


######################################################################################################
#
# Gets the request for the cinema website
#
######################################################################################################

url = requests.get('https://ticketing.useast.veezi.com/sessions/?siteToken=1c87j5nqqtncrv1gzbwver3fx8')
html = url.content

soup = BeautifulSoup(html, 'html')

findShows = soup.find('div', class_="date")

findFilms = findShows.find_all('div', class_="film")

######################################################################################################
#
# Finds the rigth sections for movie showtimes. Then loops through them and formats it correctly.
# Since it is only using 1 website the format is very specific.
#
######################################################################################################

finalMsg = ""

for findFilms in findFilms:
    nameShow = findFilms.find('h3', class_="title")
    ratingShow = findFilms.find('span', class_="censor")
    dateShow = findFilms.find('h4', class_="date")
    timeShow = findFilms.find('ul', class_="session-times")
    name = nameShow.text
    rating = ratingShow.text
    date = dateShow.text
    times = timeShow.text

    nameFilm = name.replace(" ", "", 16)
    nameFinal = nameFilm.replace("\n", " ")
    timesFilm = times.replace("\n", "", 3)
    timesFilm = timesFilm.replace("\n", "", 4)
    timesFilm = timesFilm.replace("\n", ", ", 1)
    timesFilm = timesFilm.replace("\n", "", 4)
    timesFilm = timesFilm.replace("\n", ", ", 1)
    timesFilm = timesFilm.replace("\n", "", 4)
    timesFilm = timesFilm.replace("\n", ", ", 1)
    timesFilm = timesFilm.replace("\n", "", 4)
    timesFilm = timesFilm.replace("\n", ", ", 1)
    finalMsg += "Title:" + nameFinal + "\n"
    finalMsg += "Rating: " + rating + "\n"
    finalMsg += "Date: " + date + "\n"
    finalMsg += "Times: " + timesFilm + "\n"
    finalMsg += "\n"


print(finalMsg)

######################################################################################################
#
# Prints the message before it sends.
# Then it sends the message.
#
######################################################################################################

msg = MIMEMultipart()

msg['From'] = MY_ADDRESS
msg['To'] = "Your Email Here"
msg['Subject'] = "Your Message Here"
msg.attach(MIMEText(finalMsg, 'plain'))

s.send_message(msg)

s.quit()

