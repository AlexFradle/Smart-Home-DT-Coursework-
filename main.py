import pyglet
from pyglet.window import key, mouse
from pyglet.image.codecs.png import PNGImageDecoder
from pyglet.gl import *
import pyglet.clock
from datetime import datetime
from time import sleep
import speech_recognition as sr
import pyttsx3
import requests
import shutil
import json
from PIL import Image

home = True
weather = False
news = False
check_time = False
counter = 0
imgs = ["border_1.png", "geometric_1.png"]
listen_counter = 0
window = pyglet.window.Window(height=480, width=800, resizable=False)

check = pyglet.resource.image("not_listening.png")

time_ = pyglet.text.Label(text=str(datetime.now().strftime("%H:%M")),
                          font_name="arial",
                          font_size=100,
                          color=(255, 255, 255, 255),
                          x=window.width//2, y=window.height//1.5,
                          anchor_x="center", anchor_y="center")

date = pyglet.text.Label(text=str(datetime.now().strftime("%A %d/%m/%Y")),
                         font_name="arial",
                         font_size=50,
                         color=(255, 255, 255, 255),
                         x=window.width//2, y=window.height//3,
                         anchor_x="center", anchor_y="center")


back = pyglet.resource.image(imgs[0])
weather_img = None

main_temp = pyglet.text.Label(text="", font_name="arial", font_size=30, color=(0, 0, 0, 255),
                              x=165, y=200, anchor_x="center", anchor_y="center")
temp_desc = pyglet.text.Label(text="", font_name="arial", font_size=20, color=(0, 0, 0, 255),
                              x=165, y=150, anchor_x="center", anchor_y="center")
sunrise = pyglet.text.Label(text="", font_name="arial", font_size=13, color=(0, 0, 0, 255),
                            x=125, y=44, anchor_x="center", anchor_y="center")
sunset = pyglet.text.Label(text="", font_name="arial", font_size=13, color=(0, 0, 0, 255),
                           x=250, y=44, anchor_x="center", anchor_y="center")


day_1_icon = None
day_2_icon = None
day_3_icon = None
day_4_icon = None
day_5_icon = None
day_6_icon = None
day_7_icon = None


day_1_desc = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                               x=415, y=420, anchor_x="center", anchor_y="center")
day_2_desc = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                               x=415, y=360, anchor_x="center", anchor_y="center")
day_3_desc = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                               x=415, y=300, anchor_x="center", anchor_y="center")
day_4_desc = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                               x=415, y=240, anchor_x="center", anchor_y="center")
day_5_desc = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                               x=415, y=180, anchor_x="center", anchor_y="center")
day_6_desc = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                               x=415, y=120, anchor_x="center", anchor_y="center")
day_7_desc = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                               x=415, y=60, anchor_x="center", anchor_y="center")


day_1_max = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                              x=500, y=420, anchor_x="center", anchor_y="center")
day_2_max = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                              x=500, y=360, anchor_x="center", anchor_y="center")
day_3_max = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                              x=500, y=300, anchor_x="center", anchor_y="center")
day_4_max = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                              x=500, y=240, anchor_x="center", anchor_y="center")
day_5_max = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                              x=500, y=180, anchor_x="center", anchor_y="center")
day_6_max = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                              x=500, y=120, anchor_x="center", anchor_y="center")
day_7_max = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                              x=500, y=60, anchor_x="center", anchor_y="center")


day_1_min = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                              x=565, y=420, anchor_x="center", anchor_y="center")
day_2_min = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                              x=565, y=360, anchor_x="center", anchor_y="center")
day_3_min = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                              x=565, y=300, anchor_x="center", anchor_y="center")
day_4_min = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                              x=565, y=240, anchor_x="center", anchor_y="center")
day_5_min = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                              x=565, y=180, anchor_x="center", anchor_y="center")
day_6_min = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                              x=565, y=120, anchor_x="center", anchor_y="center")
day_7_min = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                              x=565, y=60, anchor_x="center", anchor_y="center")


day_1_humid = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                                x=630, y=420, anchor_x="center", anchor_y="center")
day_2_humid = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                                x=630, y=360, anchor_x="center", anchor_y="center")
day_3_humid = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                                x=630, y=300, anchor_x="center", anchor_y="center")
day_4_humid = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                                x=630, y=240, anchor_x="center", anchor_y="center")
day_5_humid = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                                x=630, y=180, anchor_x="center", anchor_y="center")
day_6_humid = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                                x=630, y=120, anchor_x="center", anchor_y="center")
day_7_humid = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                                x=630, y=60, anchor_x="center", anchor_y="center")


day_1_precip = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                                 x=700, y=420, anchor_x="center", anchor_y="center")
day_2_precip = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                                 x=700, y=360, anchor_x="center", anchor_y="center")
day_3_precip = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                                 x=700, y=300, anchor_x="center", anchor_y="center")
day_4_precip = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                                 x=700, y=240, anchor_x="center", anchor_y="center")
day_5_precip = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                                 x=700, y=180, anchor_x="center", anchor_y="center")
day_6_precip = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                                 x=700, y=120, anchor_x="center", anchor_y="center")
day_7_precip = pyglet.text.Label(text="", font_name="arial", font_size=15, color=(0, 0, 0, 255),
                                 x=700, y=60, anchor_x="center", anchor_y="center")


news_1_title = pyglet.text.document.FormattedDocument("PLACEHOLDER")
news_1_title.set_style(start=0, end=len(news_1_title.text),
                       attributes=dict(color=(0, 0, 0, 255), font_name="arial", font_size=25))
news_1_title_layout = pyglet.text.layout.TextLayout(news_1_title, 490, 50, multiline=True)
news_1_title_layout.x, news_1_title_layout.y = 10, 480
news_1_title_layout.anchor_y = "top"

news_2_title = pyglet.text.document.FormattedDocument("PLACEHOLDER")
news_2_title.set_style(start=0, end=len(news_2_title.text),
                       attributes=dict(color=(0, 0, 0, 255), font_name="arial", font_size=25))
news_2_title_layout = pyglet.text.layout.TextLayout(news_2_title, 490, 50, multiline=True)
news_2_title_layout.x, news_2_title_layout.y = 10, 315
news_2_title_layout.anchor_y = "top"

news_3_title = pyglet.text.document.FormattedDocument("PLACEHOLDER")
news_3_title.set_style(start=0, end=len(news_3_title.text),
                       attributes=dict(color=(0, 0, 0, 255), font_name="arial", font_size=25))
news_3_title_layout = pyglet.text.layout.TextLayout(news_3_title, 490, 50, multiline=True)
news_3_title_layout.x, news_3_title_layout.y = 10, 160
news_3_title_layout.anchor_y = "top"


news_1_body = pyglet.text.document.FormattedDocument("PLACEHOLDER")
news_1_body.set_style(start=0, end=len(news_1_body.text),
                      attributes=dict(color=(0, 0, 0, 255), font_name="arial", font_size=12))
news_1_body_layout = pyglet.text.layout.TextLayout(news_1_body, 490, 150, multiline=True)
news_1_body_layout.x, news_1_body_layout.y = 10, 400
news_1_body_layout.anchor_y = "top"

news_2_body = pyglet.text.document.FormattedDocument("PLACEHOLDER")
news_2_body.set_style(start=0, end=len(news_2_body.text),
                      attributes=dict(color=(0, 0, 0, 255), font_name="arial", font_size=12))
news_2_body_layout = pyglet.text.layout.TextLayout(news_2_body, 490, 150, multiline=True)
news_2_body_layout.x, news_2_body_layout.y = 10, 235
news_2_body_layout.anchor_y = "top"

news_3_body = pyglet.text.document.FormattedDocument("PLACEHOLDER")
news_3_body.set_style(start=0, end=len(news_3_body.text),
                      attributes=dict(color=(0, 0, 0, 255), font_name="arial", font_size=12))
news_3_body_layout = pyglet.text.layout.TextLayout(news_3_body, 490, 150, multiline=True)
news_3_body_layout.x, news_3_body_layout.y = 10, 80
news_3_body_layout.anchor_y = "top"


news_1_img = None
news_2_img = None
news_3_img = None


def get_news():
    global news_1_title, news_2_title, news_3_title
    global news_1_body, news_2_body, news_2_body
    global news_1_img, news_2_img, news_3_img

    request = requests.get("https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=API-KEY")
    text = request.text
    file = json.loads(text)
    titles = []

    for i in range(len(file["articles"])):
        if i == 3:
            break
        title = file["articles"][i]["title"]
        descr = file["articles"][i]["description"]
        url = file["articles"][i]["urlToImage"]
        titles.append((title, descr))

        img = requests.get(f"{url}", stream=True)
        img_bin = img.raw
        with open(f"news_{i+1}_img.png", "wb") as f:
            shutil.copyfileobj(img_bin, f)

        img = Image.open(f"news_{i+1}_img.png")
        img = img.resize((300, 150), Image.ANTIALIAS)
        img.save(f"news_{i+1}_img.png", quality=95)

    news_1_title.text = titles[0][0]
    news_2_title.text = titles[1][0]
    news_3_title.text = titles[2][0]

    news_1_body.text = titles[0][1]
    news_2_body.text = titles[1][1]
    news_3_body.text = titles[2][1]

    news_1_img = pyglet.resource.image("news_1_img.png")
    news_2_img = pyglet.resource.image("news_2_img.png")
    news_3_img = pyglet.resource.image("news_3_img.png")

    return titles


def get_weather():
    global weather_img, main_temp, temp_desc, sunrise, sunset
    global day_1_icon, day_2_icon, day_3_icon, day_4_icon, day_5_icon, day_6_icon, day_7_icon
    global day_1_desc, day_2_desc, day_3_desc, day_4_desc, day_5_desc, day_6_desc, day_7_desc
    global day_1_max, day_2_max, day_3_max, day_4_max, day_5_max, day_6_max, day_7_max
    global day_1_min, day_2_min, day_3_min, day_4_min, day_5_min, day_6_min, day_7_min
    global day_1_humid, day_2_humid, day_3_humid, day_4_humid, day_5_humid, day_6_humid, day_7_humid
    global day_1_precip, day_2_precip, day_3_precip, day_4_precip, day_5_precip, day_6_precip, day_7_precip

    request_w = requests.get("https://api.weatherbit.io/v2.0/forecast/daily?city=Stourbridge&country=GB&days=7&key=API-KEY")
    print("REQUESTED WEEK")
    request_d = requests.get("https://api.weatherbit.io/v2.0/current?city=Stourbridge&country=GB&key=API-KEY")
    print("REQUESTED DAY")
    data = json.loads(request_w.text)
    data_day = json.loads(request_d.text)

    cur_temp = data_day["data"][0]["temp"]
    sunris = data_day["data"][0]["sunrise"]
    sunst = data_day["data"][0]["sunset"]
    desc = data_day["data"][0]["weather"]["description"]

    icon = requests.get(f"https://www.weatherbit.io/static/img/icons/{data_day['data'][0]['weather']['icon']}.png", stream=True)
    icon_bin = icon.raw
    with open(f"{data_day['data'][0]['weather']['icon']}.png", "wb") as f:
        shutil.copyfileobj(icon_bin, f)

    weather_img = pyglet.image.load(f"{data_day['data'][0]['weather']['icon']}.png", decoder=PNGImageDecoder())
    main_temp.text = str(cur_temp) + "°C"
    temp_desc.text = desc
    sunrise.text = str(sunris)
    sunset.text = str(sunst)
    print("ALL CURRENT SETTINGS CHANGED")
    days = []
    for i in data["data"]:
        code = i["weather"]["icon"]
        desc = i["weather"]["description"]
        max_temp = str(i["max_temp"])
        min_temp = str(i["min_temp"])
        humid = str(round(i["rh"], 1)) + "%"
        precip = str(round(i["precip"], 1)) + "mm"
        days.append((code, desc, max_temp, min_temp, humid, precip))
        icon = requests.get(f"https://www.weatherbit.io/static/img/icons/{code}.png", stream=True)
        icon_bin = icon.raw
        with open(f"{code}.png", "wb") as f:
            shutil.copyfileobj(icon_bin, f)
        img = Image.open(f"{code}.png")
        img = img.resize((55, 55), Image.ANTIALIAS)
        img.save(f"{code}_compressed.png", quality=95)
        print("DAY DONE SAVING")

    for day in range(len(days)):
        if day == 0:
            day_1_icon = pyglet.image.load(f"{days[0][0]}_compressed.png", decoder=PNGImageDecoder())
            day_1_desc.text = days[0][1]
            if len(days[0][1]) > 10:
                day_1_desc.font_size = 12
            day_1_max.text = days[0][2]
            day_1_min.text = days[0][3]
            day_1_humid.text = days[0][4]
            day_1_precip.text = days[0][5]
            print("DAY 1 CHANGED")

        elif day == 1:
            day_2_icon = pyglet.image.load(f"{days[1][0]}_compressed.png", decoder=PNGImageDecoder())
            day_2_desc.text = days[1][1]
            if len(days[1][1]) > 10:
                day_2_desc.font_size = 12
            day_2_max.text = days[1][2]
            day_2_min.text = days[1][3]
            day_2_humid.text = days[1][4]
            day_2_precip.text = days[1][5]
            print("DAY 2 CHANGED")

        elif day == 2:
            day_3_icon = pyglet.image.load(f"{days[2][0]}_compressed.png", decoder=PNGImageDecoder())
            day_3_desc.text = days[2][1]
            if len(days[2][1]) > 10:
                day_3_desc.font_size = 12
            day_3_max.text = days[2][2]
            day_3_min.text = days[2][3]
            day_3_humid.text = days[2][4]
            day_3_precip.text = days[2][5]
            print("DAY 3 CHANGED")

        elif day == 3:
            day_4_icon = pyglet.image.load(f"{days[3][0]}_compressed.png", decoder=PNGImageDecoder())
            day_4_desc.text = days[3][1]
            if len(days[3][1]) > 10:
                day_4_desc.font_size = 12
            day_4_max.text = days[3][2]
            day_4_min.text = days[3][3]
            day_4_humid.text = days[3][4]
            day_4_precip.text = days[3][5]
            print("DAY 4 CHANGED")

        elif day == 4:
            day_5_icon = pyglet.image.load(f"{days[4][0]}_compressed.png", decoder=PNGImageDecoder())
            day_5_desc.text = days[4][1]
            if len(days[4][1]) > 10:
                day_5_desc.font_size = 12
            day_5_max.text = days[4][2]
            day_5_min.text = days[4][3]
            day_5_humid.text = days[4][4]
            day_5_precip.text = days[4][5]
            print("DAY 5 CHANGED")

        elif day == 5:
            day_6_icon = pyglet.image.load(f"{days[5][0]}_compressed.png", decoder=PNGImageDecoder())
            day_6_desc.text = days[5][1]
            if len(days[5][1]) > 10:
                day_6_desc.font_size = 12
            day_6_max.text = days[5][2]
            day_6_min.text = days[5][3]
            day_6_humid.text = days[5][4]
            day_6_precip.text = days[5][5]
            print("DAY 6 CHANGED")

        elif day == 6:
            day_7_icon = pyglet.image.load(f"{days[6][0]}_compressed.png", decoder=PNGImageDecoder())
            day_7_desc.text = days[6][1]
            if len(days[6][1]) > 10:
                day_7_desc.font_size = 12
            day_7_max.text = days[6][2]
            day_7_min.text = days[6][3]
            day_7_humid.text = days[6][4]
            day_7_precip.text = days[6][5]
            print("DAY 7 CHANGED")

    return cur_temp, desc


def update(unused):
    global listen_counter, check
    time_.text = str(datetime.now().strftime("%H:%M"))
    check = pyglet.resource.image("not_listening.png")
    listen_counter += 1
    if listen_counter == 59:
        check = pyglet.resource.image("listening.png")
    if listen_counter == 60:
        listen()
        listen_counter = 0


def listen():
    global back, home, weather, check, news, check_time
    engine = pyttsx3.init("sapi5")
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    audio = ""
    with mic as source:
        print("STARTED LISTENING")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=4)
        except sr.WaitTimeoutError:
            print("TIMEOUT")
    try:
        text = r.recognize_google(audio)
        print("RECOGNISED")
        print(text)
        audio = ""
        if text == "weather":
            cur_weather = get_weather()
            back = pyglet.resource.image("weather_template.png")
            home = False
            news = False
            weather = True
            engine.say(f"It is currently {cur_weather[0]} degrees and {cur_weather[1]}")
            engine.runAndWait()
            check_time = True
        elif text == "news":
            articles = get_news()
            back = pyglet.resource.image("news.png")
            home = False
            weather = False
            news = True
            engine.say(f"The headlines are: {articles[0][0]}. {articles[1][0]}. and - {articles[2][0]}")
            engine.runAndWait()
            check_time = True
    except Exception as e:
        print("NOT RECOGNISED" + str(e))


@window.event
def on_key_press(letter, mod):
    global back, imgs, home, weather, news
    if letter == key.W:
        print("W")
        get_weather()
        back = pyglet.resource.image("weather_template.png")
        home = False
        news = False
        weather = True
    elif letter == key.T:
        print("T")
        back = pyglet.resource.image(imgs[0])
        time_.color = (255, 255, 255, 255)
        date.color = (255, 255, 255, 255)
        home = True
        weather = False
        news = False
    elif letter == key.C:
        print("C")
        if home:
            back = pyglet.resource.image(imgs[1])
            time_.color = (0, 0, 0, 255)
            date.color = (0, 0, 0, 255)
    elif letter == key.N:
        get_news()
        back = pyglet.resource.image("news.png")
        weather = False
        home = False
        news = True


@window.event
def on_draw():
    global news, home, back, check_time, counter, weather
    print("DRAW")
    window.clear()
    back.blit(0, 0)
    check.blit(0, 0)
    glEnable(GL_BLEND)
    if home:
        time_.draw()
        date.draw()
    if weather:
        weather_img.blit(100, 270)
        main_temp.draw()
        temp_desc.draw()
        sunrise.draw()
        sunset.draw()
        day_1_icon.blit(310, 395)
        day_1_desc.draw()
        day_1_max.draw()
        day_1_min.draw()
        day_1_humid.draw()
        day_1_precip.draw()

        day_2_icon.blit(310, 335)
        day_2_desc.draw()
        day_2_max.draw()
        day_2_min.draw()
        day_2_humid.draw()
        day_2_precip.draw()

        day_3_icon.blit(310, 275)
        day_3_desc.draw()
        day_3_max.draw()
        day_3_min.draw()
        day_3_humid.draw()
        day_3_precip.draw()

        day_4_icon.blit(310, 215)
        day_4_desc.draw()
        day_4_max.draw()
        day_4_min.draw()
        day_4_humid.draw()
        day_4_precip.draw()

        day_5_icon.blit(310, 155)
        day_5_desc.draw()
        day_5_max.draw()
        day_5_min.draw()
        day_5_humid.draw()
        day_5_precip.draw()

        day_6_icon.blit(310, 95)
        day_6_desc.draw()
        day_6_max.draw()
        day_6_min.draw()
        day_6_humid.draw()
        day_6_precip.draw()

        day_7_icon.blit(310, 35)
        day_7_desc.draw()
        day_7_max.draw()
        day_7_min.draw()
        day_7_humid.draw()
        day_7_precip.draw()
        if check_time:
            counter += 1
            if counter >= 300:
                back = pyglet.resource.image("border_1.png")
                weather = False
                home = True
                check_time = False
                counter = 0

    if news:
        news_1_img.blit(495, 325)
        news_2_img.blit(495, 160)
        news_3_img.blit(495, 5)
        news_1_title_layout.draw()
        news_1_body_layout.draw()
        news_2_title_layout.draw()
        news_2_body_layout.draw()
        news_3_title_layout.draw()
        news_3_body_layout.draw()
        if check_time:
            counter += 1
            if counter >= 180:
                back = pyglet.resource.image("border_1.png")
                news = False
                home = True
                check_time = False
                counter = 0


pyglet.clock.set_fps_limit(60)
pyglet.clock.schedule(update)
pyglet.app.run()

