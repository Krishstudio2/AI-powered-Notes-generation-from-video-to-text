import speech_recognition as sr
import moviepy.editor as mp
from flask import *
import os

app=Flask(__name__)


@app.route('/')
def hello_world():
   return render_template('index.html')

@app.route('/upload')
def upload():
   return render_template("file_upload_form.html")

@app.route('/success',methods=['POST'])
def success():
   if request.method == 'POST':
      f=request.files['file']
      f.save(f.filename)
      print(f.filename)
      
      pat=os.path.join(r"C:\Users\as\PycharmProjects\kalaiproject",f.filename)
      clip = mp.VideoFileClip(pat)
      clip.audio.write_audiofile(r"converted.wav")
      r = sr.Recognizer()
      audio = sr.AudioFile("converted.wav")

      with audio as source:
         audio_file = r.record(source)
         result = r.recognize_google(audio_file)
         with open('recognized.txt', mode='w') as file:
            file.write("Recognized Speech:")
            file.write("\n")
            file.write(result)

      return render_template("success.html",name=f.filename)

@app.route("/wav")
def streamwav():
    def generate():
        with open("converted.wav", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/x-wav")

if __name__ == '__main__':
   app.run(debug=True, port=5000, host='0.0.0.0')

