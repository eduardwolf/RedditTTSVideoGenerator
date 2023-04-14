import praw
import time
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from selenium import webdriver
import random
import moviepy.editor as mpy
from moviepy.editor import *
import os
import librosa
import datetime
import math
from pydub import AudioSegment
from PIL import Image, ImageFont, ImageDraw, ImageOps

# REDDIT SCRAPE START
# tato sekce vybere pomoci api od redditu nejlepsi prispevky z vybraneho fora pro dalsi zpracovani
# TTS setup

speech_config = SpeechConfig(subscription="KEY_HERE", region="eastus")
speech_config.speech_synthesis_voice_name = "en-US-ChristopherNeural"

# Reddit API setup
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="testing",
)

# Vyber forum
subreddit = reddit.subreddit("askreddit")
top = subreddit.top("month")
top = list(top)

post_list = []
post_amount = 33  # max = 100

if post_amount > len(top):
    post_amount = len(top)
for i in range(post_amount):
    print(top[i])
    top[i].comments.replace_more(limit=0)
    comments = []
    rangeLen = len(top[i].comments)
    if rangeLen > 10:
        rangeLen = 10
    for ix in range(rangeLen):
        toAppend = [top[i].comments[ix].author, top[i].comments[ix].body, top[i].comments[ix].permalink,
                    top[i].comments[ix].id]
        comments.append(toAppend)


    class Post:
        def __init__(self):
            self.title = top[i].title
            self.author = top[i].author
            self.comments = comments
            self.permalink = top[i].permalink
            self.id = top[i].id


    post_list.append(Post())
# REDDIT SCRAPE END

# SCREENSHOT CREATION START
# tato sekce vytvori pomoci chromedriveru screenshoty pro pouziti ve videich a ulozi je do slozky
chrome_driver_location = 'LOCATION_HERE'
p_link = "https://www.reddit.com"
t3 = "t3_"
t1 = "t1_"
post_list_2 = []
for post in post_list:
    # tento for loop projde vsemi posty v post listu a udela screenshot top komentaru
    try:
        title_str = post.title.replace(" ", "")
        title_str = ''.join(filter(str.isalnum, title_str))
        title_str = title_str[:30]
        new_path = "screenshots/" + title_str  # uloziste screenshotu
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        post_id = post.id
        post_p_link = post.permalink
        driver = webdriver.Chrome(chrome_driver_location)
        print(p_link + post_p_link)
        driver.get(p_link + post_p_link)
        driver.find_element_by_id(t3 + post_id).screenshot("screenshots/" + title_str + "/" + "title" + ".png")
        counter = 0
        for comment in post.comments:
            comment_p_link = comment[2]
            comment_id = comment[3]
            driver.get(p_link + comment_p_link)
            driver.find_element_by_id(t1 + comment_id).screenshot(
                "screenshots/" + title_str + "/" + str(counter) + ".png")
            counter += 1
        driver.close()
        post_list_2.append(post)
    except:
        driver.close()
# SCREENSHOT CREATION END


# TEXT TO SPEECH START
# tento for loop projde vsemi posty a vytvori z nich .wav audio zaznamy pomoci TEXT TO SPEECH,
# audiozaznamy ulozi do slozky

for q in range(len(post_list_2)):
    start_txt = "A Reddit user asked: " + post_list_2[q].title
    title_str = post_list_2[q].title.replace(" ", "")
    title_str = ''.join(filter(str.isalnum, title_str))
    title_str = title_str[:30]
    new_path = 'info/' + title_str

    if not os.path.exists(new_path):
        os.makedirs(new_path)
    fileN = "info/" + title_str + "/" + "hi" + ".wav"
    audio_config = AudioOutputConfig(filename=fileN)
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(start_txt)
    time.sleep(2)

    for w in range(len(post_list_2[q].comments)):
        comment_txt = post_list_2[q].comments[w][1]
        fileN = "info/" + title_str + "/" + str(w) + ".wav"

        if comment_txt.find("(http") > 0:
            off_button = False

            for idx in range(comment_txt.find("(http"), len(comment_txt)):
                if not off_button:
                    print(comment_txt)
                    print(len(comment_txt), idx)
                    if comment_txt[idx] == ")":
                        off_button = True
                        slicer = slicer(comment_txt.find("(http"), idx + 1)
                        comment_txt = comment_txt.replace(comment_txt[slicer], "")

        audio_config = AudioOutputConfig(filename=fileN)
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        synthesizer.speak_text_async(comment_txt)
        time.sleep(1)
    time.sleep(60)  # needed to make sure it all goes through
# TEXT TO SPEECH END

# THUMBNAIL CREATION START
# tato sekce vytvori jpg s tucnym textem na predem nachystane obrazky, staci cerne pozadi,
# nabizi se pridat obrazek, thumbnaily ulozi do slozky

for post_t in post_list_2:
    text = post_t.title.upper()
    title_str = text.replace(" ", "")
    title_str = ''.join(filter(str.isalnum, title_str))
    title_str = title_str[:30]
    new_path = "thumbnails/" + title_str + ".jpg"
    template_arr = ["../thumbnailtemplate/5.jpg", "../thumbnailtemplate/4.jpg", "../thumbnailtemplate/3.jpg",
                    "../thumbnailtemplate/2.jpg", "../thumbnailtemplate/1.jpg"]
    my_image = Image.open(random.choice(template_arr))
    font_size = 400
    limit = 10
    if len(text) > 60:
        font_size = 333
        limit = 15
    title_font = ImageFont.truetype("../thumbnailtemplate/lmb.otf", font_size)
    split_arr = text.split()
    down = 950
    counter = 0
    color_arr = [(255, 86, 0), (128, 0, 128), (255, 255, 0), (255, 0, 0), (0, 255, 0)]
    randomcolor = random.choice(color_arr)
    while len(split_arr) > 0:  # make this character based rather
        counter += 1
        towrite = ""
        for i in range(3):
            if len(towrite) < limit:
                towrite += split_arr[0] + " "
                split_arr.pop(0)

        if counter == 2:
            rgb = randomcolor
        else:
            rgb = (255, 255, 255)
        txt = Image.new('L', (5000, 5000))
        d = ImageDraw.Draw(txt)
        d.text((0, down), towrite, font=title_font, fill=255)
        w = txt.rotate(0, expand=1)
        my_image.paste(ImageOps.colorize(w, (0, 0, 0), rgb), (242, 60), w)
        down += 500

    my_image.save(new_path)
# THUMBNAIL END

# VIDEO CREATION START
# tato sekce projde vsemi vytvorenymi zaznamy a spoji dohromady content z reddit prispevku a komentaru a audio
# s predem nastavenym backgroundem

v_codec = "libx264"
video_quality = "24"
compression = "ultrafast"
directory = 'info'

for name in os.listdir(directory):
    if name != "bye.wav" and name != "silence.wav":
        title = name
        loadtitle = "../vidtemps/grayytb.mov"
        savetitle = "finishedvids/" + title + "d" + '.mp4'
        f = os.path.join(directory, name)
        g = os.path.join("screenshots", name)
        # checking if it is a file
        totallength = 8
        alllengths = []
        for wav in os.listdir(f):
            totallength += librosa.get_duration(filename=os.path.join(f, wav))
            alllengths.append(librosa.get_duration(filename=os.path.join(f, wav)))
            totallength += 0.5

        cut = str(datetime.timedelta(seconds=math.ceil(totallength))) + ".00"
        cuts = [('00:00:00.00', cut)]
        wholeaudio = AudioSegment.from_wav(directory + '/' + name + "/" + "hi.wav")
        for wavfile in os.listdir(f):
            if wavfile != "hi.wav":
                toadd = AudioSegment.from_wav(directory + '/' + "silence.wav") + AudioSegment.from_wav(
                    os.path.join(f, wavfile))
                wholeaudio += toadd
        wholeaudio += AudioSegment.from_wav(directory + '/' + "silence.wav")
        wholeaudio += AudioSegment.from_wav(directory + '/' + "bye.wav")
        wholeaudio += AudioSegment.from_wav(directory + '/' + "silence.wav")
        wholeaudio = wholeaudio.export(directory + '/' + name + "/" + "wholeaudio.wav", format="wav")


        def edit_video(loadtitle, savetitle, cuts):
            # load file
            video = mpy.VideoFileClip(loadtitle)

            # cut file
            clips = []
            for cut_x in cuts:
                clip = video.subclip(cut_x[0], cut_x[1])
                clips.append(clip)

            final_clip = mpy.concatenate_videoclips(clips)

            logo = (mpy.ImageClip("screenshots/" + name + "/title.png")
                    .set_duration(final_clip.duration)
                    # .resize(height=50) # v potrebe resize...
                    .margin(bottom=500, opacity=0)
                    .set_position(("center", "center")))
            my_audio_clip = AudioFileClip(directory + "/" + title + "/wholeaudio.wav")

            clips_array = [logo]
            counter1 = 0
            last_start = 0
            last_duration = 0
            for comment_x in os.listdir("screenshots/" + name):
                if comment_x != "title.png":
                    comment_png = (mpy.ImageClip("screenshots/" + name + "/" + comment_x)
                                   .set_duration(final_clip.duration)
                                   .set_position(("center", "center")))
                    if counter1 == 0:
                        start = librosa.get_duration(filename="info/" + name + "/hi.wav") + 0.5
                        duration = librosa.get_duration(filename="info/" + name + "/" + str(counter1) + ".wav")
                        clips_array.append(comment_png.set_start(start).set_duration(duration))
                        last_start = start
                        last_duration = duration + 0.5
                    else:
                        start = last_start + last_duration
                        duration = librosa.get_duration(filename="info/" + name + "/" + str(counter1) + ".wav")
                        clips_array.append(comment_png.set_start(start).set_duration(duration))
                        last_start = start
                        last_duration = duration + 0.5
                    counter1 += 1
            final_clip = final_clip.set_audio(my_audio_clip)
            clips_array.insert(0, final_clip)
            final_clip = mpy.CompositeVideoClip(clips_array)
            # save file
            final_clip.write_videofile(savetitle, threads=4, fps=24,
                                       codec=v_codec,
                                       preset=compression,
                                       ffmpeg_params=["-crf", video_quality])

            video.close()
