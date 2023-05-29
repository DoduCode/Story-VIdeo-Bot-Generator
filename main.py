from tkinter import *
from math import floor

from gtts import gTTS
from pexelsPy import API
import requests
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip, ImageClip

# Commands
# Story = give a story on a random topic with a title in 5 sentences with a plot twist with not so many dialogues without bulletpoints
# Keywords = give me 1 keyword in each sentence of the story and put them all in a list in python format
# Keywords(2) = give me 2 seperate keywords in each sentence of the story and put them all in a list in python format and remove the inner brackets

class App(Tk):
    def __init__(self, api):
        super().__init__()
        
        self.api = api
        self.mode = True

        self.geometry("500x600") 
        self.configure(bg='ghost white')
        self.title("Story Video Bot")

        Label(self, text = "TEXT_TO_SPEECH", font = "arial 20 bold", bg='white smoke').pack()
        
        self.msg = StringVar()

        Label(self, text ="Story Name", font = 'arial 15 bold', bg ='white smoke').place(x = 20,y = 100)
        self.name_field = Entry(self, width ='50')
        self.name_field.place(x = 20,y = 150)

        Label(self, text ="Enter Story", font = 'arial 15 bold', bg ='white smoke').place(x = 20,y = 200)
        self.entry_field = Entry(self, width ='50')
        self.entry_field.place(x=20,y=250)

        Label(self, text ="Story Keywords", font = 'arial 15 bold', bg ='white smoke').place(x = 20,y = 300)
        self.keyword_field = Entry(self, width ='50')
        self.keyword_field.place(x=20,y=350)

        Label(self, text ="Enter how long each clip", font = 'arial 15 bold', bg ='white smoke').place(x = 20,y = 400)
        self.clip_field = Entry(self, width ='50')
        self.clip_field.place(x=20,y=450)

        Button(self, text = "PLAY", font = 'arial 15 bold', command = self.text_to_speech, width = '4').place(x = 25, y = 500)
        Button(self, font = 'arial 15 bold', text = 'Exit', width = '4', command = self.exit, bg = 'OrangeRed1').place(x = 100 , y = 500)
        Button(self, font = 'arial 15 bold', text = 'Make Video', width = '11', command = self.make_video).place(x = 175 , y = 500)

        self.var = IntVar()

        self.r1 = Radiobutton(self, text = "Use Videos", variable = self.var, value = 1, command = self.setMode).place(x = 340, y = 100)
        self.r2 = Radiobutton(self, text = "Use Photos", variable = self.var, value = 2, command = self.setMode).place(x = 340, y = 120)
        self.mainloop()

    def text_to_speech(self):
        self.message = self.entry_field.get()
        self.speech = gTTS(text = self.message, slow = False, tld='us')
        self.name = f'Test-To-Speech-Story-{self.name_field.get()}.mp3'
        self.speech.save("files/" + self.name)

        self.get_videos()

    def get_videos(self):
        self.keywords = self.keyword_field.get()
        self.keywords = self.make_list(self.keywords)
        self.amount_of_videos = 5
        
        for i in range(0, len(self.keywords)):
            if self.mode is True:
                self.api.search_videos(self.keywords[i], page = 1, results_per_page = self.amount_of_videos)
                self.videos = self.api.get_videos()

                self.video_key = 0

                print(self.videos)
                print('https://www.pexels.com/video/' + str(self.videos[self.video_key].id) + '/download')

                self.url_video = 'https://www.pexels.com/video/' + str(self.videos[self.video_key].id) + '/download'
                self.r = requests.get(self.url_video, stream = True)

                if self.r.content == b'Video not found' or self.r.content == b'Video temporarily unavailable':
                    print("Vid 0 Failed")

                    for j in range(0, self.amount_of_videos):
                        self.video_key += 1
                        print('https://www.pexels.com/video/' + str(self.videos[self.video_key].id) + '/download')

                        self.url_video = 'https://www.pexels.com/video/' + str(self.videos[self.video_key].id) + '/download'
                        self.r = requests.get(self.url_video, stream = True)

                        if self.r.content == b'Video not found' or self.r.content == b'Video temporarily unavailable':
                            print(f"Vid {self.video_key} Failed")
                            continue

                        else:
                            break

                with open(f'files/clip{i}.mp4', 'wb') as outfile:
                    outfile.write(self.r.content)

            if self.mode is False:
                self.api.search_photos(self.keywords[i], page = 1, results_per_page = self.amount_of_videos)
                self.photos = self.api.get_photos()

                self.photo_key = 0

                print(self.photos)

                print(str(self.photos[self.photo_key].original))

                self.url_photo = str(self.photos[self.photo_key].original)
                self.r = requests.get(self.url_photo, stream = True)

                if self.r.content == b'Photo not found' or self.r.content == b'Photo temporarily unavailable':
                    print("Photo 0 Failed")

                    for j in range(0, self.amount_of_videos):
                        self.photo_key += 1
                        print(str(self.photos[self.photo_key].original))

                        self.url_photo = str(self.photos[self.photo_key].original)
                        self.r = requests.get(self.url_photo, stream = True)

                        if self.r.content == b'Photo not found' or self.r.content == b'Photo temporarily unavailable':
                            print(f"Photo {self.photo_key} Failed")
                            continue

                        else:
                            break

                with open(f'files/clip{i}.jpeg', 'wb') as outfile:
                    outfile.write(self.r.content)

    def make_video(self):
        self.length_of_clip = self.clip_field.get()
        self.length_of_clip = self.make_list(self.length_of_clip)

        for i in range(0, len(self.length_of_clip)):
            self.length_of_clip[i] = int(self.length_of_clip[i])

        self.clips = []

        for i in range(0, len(self.keywords)):
            if self.mode is True:
                self.clip = VideoFileClip(f"files/clip{i}.mp4").without_audio()

                self.duration = floor(self.clip.duration)

                if self.duration > self.length_of_clip[i]:
                    self.clip = self.clip.subclip(0, self.length_of_clip[i])

                else:
                    self.clip = self.clip.subclip(0, self.duration)

                self.clip_resized = self.clip.resize(newsize=(1080, 1920))
                self.clips.append(self.clip_resized)

                if self.duration < self.length_of_clip[0]:
                    self.new_length_remaining = self.length_of_clip[0] - self.duration

                    if self.new_length_remaining > self.duration:
                        self.last_clip = self.new_length_remaining % self.duration

                        for i in range(self.duration, self.new_length_remaining, self.duration):
                            self.clips.append(self.clip_resized)

                            self.new_clip = self.clip.subclip(0, self.last_clip)
                            self.clip_resized = self.new_clip.resize(newsize=(1000, 700))
                            self.clips.append(self.clip_resized)


                    if self.new_length_remaining == self.duration:
                        self.clips.append(self.clip_resized)

                    if self.new_length_remaining < self.duration:
                        self.new_clip = self.clip.subclip(0, self.new_length_remaining % self.duration)
                        self.clip_resized = self.new_clip.resize(newsize=(1000, 700))
                        self.clips.append(self.clip_resized)

            if self.mode is False:
                self.clip = ImageClip(f"files/clip{i}.jpeg").set_duration(self.length_of_clip[i])
                self.resized_clip = self.clip.resize(newsize=(1080, 1920))

                self.clips.append(self.resized_clip)
                    

        self.audioclip = AudioFileClip(f'files/Test-To-Speech-Story-{self.name_field.get()}.mp3')
        self.credits = VideoFileClip("credits.mp4")

        self.clips.append(self.credits)

        self.combined = concatenate_videoclips(self.clips)
        self.new_audioclip = CompositeAudioClip([self.audioclip])
        self.combined.audio = self.new_audioclip
        self.combined.write_videofile(f"files/Story - {self.name_field.get()}.mp4", threads = 8, fps=24)

    def make_list(self, future_list):
        self.future_list = future_list

        self.future_list = self.future_list.replace(" ", "")
        self.future_list = self.future_list.replace('"', "")
        self.future_list = self.future_list.split(',')

        return self.future_list

    def setMode(self):
        if self.var.get() == 1:
            self.mode = True

        if self.var.get() == 2:
            self.mode = False

    def exit(self):
        self.destroy()

if __name__ == "__main__":
    PEXELS_API_KEY = 'bXLziGLVKBUcLVDbuDr2e262IolPKdqwN7Njt8OCY0BvjMlsIIapy5RM'
    api = API(PEXELS_API_KEY)
    app = App(api)