import pygame, sys, time, os, glob, filetype, serial
import tkinter as tkr
from pygame import mixer
from tinytag import TinyTag
from tkinter.filedialog import askdirectory
import speech_recognition as sr 
from datetime import datetime
from preferredsoundplayer import playsound
from mutagen.mp3 import MP3

mixer.init()
pygame.init()
recognizer = sr.Recognizer()
#PuertoSerie = serial.Serial('/dev/ttyACM0', 115000)

pausa = False
cancion = []
foto = []
cancion2 = []
foto2 = []
caminosC = []
caminosF = []

temp = ""
tamp = ""
temp2 = ""
tamp2 = ""

directory = '/home/saul/Documentos/Reproductor'
os.chdir(directory) #it permits to chenge the current dir
for x in os.listdir(): #it returns the list of files song
    if x.endswith(".mp3"):
        cancion.append(x)
for y in os.listdir(): #it returns the list of files song
    if y.endswith(".jpg"):
        foto.append(y)
os.chdir('..')
for a in cancion:
    temp = glob.glob('**/' + a, recursive=True)
    cancion2.append(temp[0])
for b in foto:
    tamp = glob.glob('**/' + b, recursive=True)
    foto2.append(tamp[0])
os.chdir('/home/saul')
for z in cancion2:
    temp2 = glob.glob('**/' + z, recursive=True)
    caminosC.append(temp2[0])
for w in foto2:
    tamp2 = glob.glob('**/' + w, recursive=True)
    caminosF.append(tamp2)
cancion.sort()
foto.sort()
cancion2.sort()
foto2.sort()
caminosC.sort()
caminosF.sort()

rola = 0

presionado1 = False
presionado2 = False
oscuro = False
tema = False
carpeta = False
salir = False
font = pygame.font.Font("freesansbold.ttf",20)
texto = 'black'
texti = ""

fondo = '#DCDDD8'

pasado = False
pasado2 = False

buttons = []
class Button:
    def __init__(self,text,width,height,pos,elevation):
        #Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#475F77'

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'
        #text
        self.text = text
        self.text_surf = gui_font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        buttons.append(self)

    def change_text(self, newtext):
        self.text_surf = gui_font.render(newtext, True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
                self.change_text(f"{self.text}")
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    self.change_text(self.text)
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'

    def presionado1(self):
        global presionado1
        if self.pressed == presionado1:
            return False
        elif self.pressed == False and presionado1 != False:
            presionado1 = not(presionado1)
            return True
        else:
            presionado1 = not(presionado1)

    def presionado2(self):
        global presionado2
        if self.pressed == presionado2:
            return False
        elif self.pressed == False and presionado2 != False:
            presionado2 = not(presionado2)
            return True
        else:
            presionado2 = not(presionado2)
    
    def presionado3(self):
        global pasado
        if self.pressed == pasado:
            return False
        elif self.pressed == False and pasado != False:
            pasado = not(pasado)
            return True
        else:
            pasado = not(pasado)

    def presionado4(self):
        global pasado2
        if self.pressed == pasado2:
            return False
        elif self.pressed == False and pasado2 != False:
            pasado2 = not(pasado2)
            return True
        else:
            pasado2 = not(pasado2)

    def presionado5(self):
        global tema
        if self.pressed == tema:
            return False
        elif self.pressed == False and tema != False:
            tema = not(tema)
            return True
        else:
            tema = not(tema)

    def presionado6(self):
        global carpeta
        if self.pressed == carpeta:
            return False
        elif self.pressed == False and carpeta != False:
            carpeta = not(carpeta)
            return True
        else:
            carpeta = not(carpeta)
            
    def presionado7(self):
        global salir
        if self.pressed == salir:
            return False
        elif self.pressed == False and salir != False:
            salir = not(salir)
            return True
        else:
            salir = not(salir)
            
pygame.init()
screen = pygame.display.set_mode((1024,600),pygame.FULLSCREEN)
pygame.display.set_caption('Reproductor')
clock = pygame.time.Clock()
gui_font = pygame.font.Font(None,30)

button1 = Button('Rewind',100,40,(335,550),5)
button2 = Button('Pause',100,40,(460,550),5)
button3 = Button('Next',100,40,(585,550),5)
button4 = Button('Prev',100,40,(210,550),5)
button5 = Button('C/O',50,40,(10,10),5)
button6 = Button('Music',70,40,(705,550),5)
button7 = Button('Salir',70,40,(800,550),5)

def buttons_draw():
    for b in buttons:
        b.draw()

while True:
    r = button1.presionado1()
    p = button2.presionado2()
    n = button3.presionado3()
    a = button4.presionado4()
    c = button5.presionado5()
    m = button6.presionado6()
    s = button7.presionado7()
    
    #sArduino = PuertoSerie.readline()
    #sArduino = sArduino.decode('utf-8')
    #sArduino = sArduino.rstrip('\n')
    #sArduino = sArduino.rstrip()
    sArduino = ""

    now = datetime.now()
    current_time = now.strftime("%H:%M")

    time.sleep(.09)
    
    if s == True:
        mixer.music.stop()
        pygame.display.quit()
        break

    if sArduino == "Presionado":
        mixer.music.pause()
        os.chdir('/home/saul/Documentos/Reproductor')
        playsound('Voz/Comandos.mp3')
        playsound('Voz/Tono.mp3')
        os.chdir('/home/saul')

        try:
            
            #device_index=1
            with sr.Microphone() as mic:

                            start = time.time()

                            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                            audio = recognizer.listen(mic,5,5)

                            end = time.time()

                            if (end - start) < 5:

                                texti = recognizer.recognize_google(audio, language="es-ES")
                                texti = texti.lower()

                            else:
                                texti = "Nada"

                            print(f"Recognized {texti}")
                            
        except Exception as e:

            texti = "No entendí"
            print(f"Recognized {texti}")


    if texti == "Nada":
        os.chdir('/home/saul/Documentos/Reproductor')
        playsound('Voz/Pana.mp3')
        os.chdir('/home/saul')
        texti = ""
        if pausa == False:
            mixer.music.unpause()
    elif texti == "No entendí":
        os.chdir('/home/saul/Documentos/Reproductor')
        playsound('Voz/Entender.mp3')
        os.chdir('/home/saul')
        texti = ""
        if pausa == False:
            mixer.music.unpause()
    elif texti == "salir":
        mixer.music.stop()
        pygame.display.quit()
        break
    elif texti != "" and not(texti == "detener" or texti == "reanudar" or texti == "rebobinar" or texti == "siguiente" or texti == "anterior"):
        if pausa == False:
            mixer.music.unpause()
        texti = ""

    if m == True:

        mixer.music.pause()
        
        music_player = tkr.Tk() 
        music_player.title("Escoger carpeta")
        music_player.withdraw()
        music_player.geometry("460x200")

        directory2 = askdirectory()

        if type(directory2) is str:
            directory = directory2
            mixer.music.stop()
            rola = 0
            cancion = []
            foto = []
            os.chdir(directory) #it permits to chenge the current dir
            for x in os.listdir(): #it returns the list of files song
                if x.endswith(".mp3"):
                    cancion.append(x)
            for y in os.listdir(): #it returns the list of files song
                if y.endswith(".jpg"):
                    foto.append(y)
            os.chdir('..')
            for a in cancion:
                temp = glob.glob('**/' + a, recursive=True)
                cancion2.append(temp[0])
            for b in foto:
                tamp = glob.glob('**/' + b, recursive=True)
                foto2.append(tamp[0])
            os.chdir('/home/saul')
            for z in cancion2:
                temp2 = glob.glob('**/' + z, recursive=True)
                caminosC.append(temp2[0])
            for w in foto2:
                tamp2 = glob.glob('**/' + w, recursive=True)
                caminosF.append(tamp2[0])
            cancion.sort()
            foto.sort()
            cancion2.sort()
            foto2.sort()
            caminosC.sort()
            caminosF.sort()
                
        else:
            mixer.music.unpause()

        music_player.destroy()

    if p == True:
        if pausa == False:
            mixer.music.pause()
            pausa = True
        elif pausa == True:
            mixer.music.unpause()
            pausa = False
    elif texti != "":
        if texti == "detener":
            mixer.music.pause()
            pausa = True
            texti = ""
        elif texti == "reanudar":
            mixer.music.unpause()
            pausa = False
            texti = ""

    elif p == False:
        pausa = pausa

    if r == True or texti == "rebobinar":
        mixer.music.unpause()
        mixer.music.rewind()
        texti = ""

    if (n == True or a == True or texti == "siguiente" or texti == "anterior") or mixer.music.get_busy() == False and pausa == False:
        if n == True or texti == "siguiente":
            if rola >= len(cancion)-1:
                rola = 0
            else:
                rola += 1
            texti = ""
            sArduino == ""
        elif mixer.music.get_busy() == False and not(texti == "anterior"):
            if pausa == False:
                if rola >= len(cancion)-1:
                    rola = 0
                else:
                    rola += 1
            elif a == True or texti == "anterior":
                if rola == 0:
                    rola = len(rola)
                else:
                    rola -= 1
                texti = ""
            else:
                rola = rola
        elif a == True or texti == "anterior":
            if rola == 0:
                rola = len(cancion)-1
            else:
                rola -= 1
            texti = ""
        pausa = False

        mixer.music.stop()
        mixer.music.load(caminosC[rola])
        mixer.music.play()

    if c == True:
        if oscuro == False:
            fondo = '#232227'
            texto = 'white'
            oscuro = True
        else:
            fondo = '#DCDDD8'
            texto = 'black'
            oscuro = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    os.chdir(directory)
    imagen = pygame.image.load(foto[rola])
    os.chdir('/home/saul')
    screen.fill(fondo)
    screen.blit(imagen,(250,40))

    tag = TinyTag.get(caminosC[rola])
    kind = filetype.guess(caminosC[rola])
    audi = MP3(caminosC[rola])
    if tag.artist != "":
        artista = tag.artist
    elif tag.artist == "":
        artista = "No data"
    else:
        artista = "No data"
    if tag.title != "":
        titulo = tag.title
    elif tag.title == "":
        titulo = "No data"
    else:
        titulo = "No data"
    if tag.album != "":
        album = tag.album
    elif tag.album == "":
        album = "No data"
    else:
        album = "No data"
    if tag.year != "":
        año = tag.year
    elif tag.year == "":
        año = "No data"
    else:
        año = "No data"
    if audi.info.channels == 2:
        tip = "Estéreo"
    else:
        tip = "Monoaural"
    
    text1 = font.render('Canción: ' + titulo,True,texto,fondo)
    text2 = font.render('Artista: ' + artista,True,texto,fondo)
    text3 = font.render('Album: ' + album,True,texto,fondo)
    text4 = font.render('Año: ' + año,True,texto,fondo)
    text5 = font.render(current_time,True,texto,fondo)
    text6 = font.render(' Frecuencia de muestreo: 44.1 kHz',True,texto,fondo)
    text7 = font.render(' Tipo de digitalización: ' + kind.extension,True,texto,fondo)
    text8 = font.render(' Audio: ' + tip,True,texto,fondo)

    textRect1 = text1.get_rect()
    textRect1.midleft = (200, 425)
    textRect2 = text2.get_rect()
    textRect2.midleft = (200, 450)
    textRect3 = text3.get_rect()
    textRect3.midleft = (200, 475)
    textRect4 = text4.get_rect()
    textRect4.midleft = (200, 500)
    textRect5 = text5.get_rect()
    textRect5.midleft = (500, 20)
    textRect6 = text6.get_rect()
    textRect6.midleft = (550, 425)
    textRect7 = text7.get_rect()
    textRect7.midleft = (550, 450)
    textRect8 = text8.get_rect()
    textRect8.midleft = (550, 475)
    screen.blit(text1,textRect1)
    screen.blit(text2,textRect2)
    screen.blit(text3,textRect3)
    screen.blit(text4,textRect4)
    screen.blit(text5,textRect5)
    screen.blit(text6,textRect6)
    screen.blit(text7,textRect7)
    screen.blit(text8,textRect8)
    buttons_draw()

    pygame.display.update()
    clock.tick(60)