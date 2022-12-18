import Speech_recognition as sr

r = sr.recogniser()

with sr.Microphone() as source:
    
    audio = r.listen(source)
    
    text = r.recognise_google(audio)
    
    print(text)
