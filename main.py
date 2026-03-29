#ANDREW CHURCH -- SETAPP -- 2022 -- PROJECT DIST-PM
import pygame,random,os,time,sys
try:
    from tkinter import *
    from tkinter import filedialog
except:
    print("TKINTER FILEDIALOG NOT FOUND. SAVING NOT SUPPORTED.")
    pass


# CHANGING THE WORKING DIRECTORY, IF THE PROGRAM IS RUNNING IN A PYINSTALLER BUNDLE -- thanks, pyinstaller ;)
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    print('Running via: PyInstaller Bundle')
    os.chdir(sys._MEIPASS)
    debug = False
else:
    print('Running via: Python Process')
    debug = True
    pass
# print("__file__ is:", __file__)
# the debug info is set based off if you're in a pyinstaller bundle or source code


version="1.0.2: OPTIMIZATION UPDATE"
debug=True

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#LOADING IMAGES
studentpics=[]
#defaulting
default_image=pygame.transform.scale(pygame.image.load("./defaults/default_image.png"),(50,50))
#gathering a list of random images, shuffling them
img_list=os.listdir("./images/students/");random.shuffle(img_list)
#shrinking the list to only load 100 images at MOST
while(len(img_list)>100):img_list.pop((len(img_list)-1))
#loading every image in the list
for item in img_list:
    #print(str(os.path.getsize("./images/students/"+str(item))/1000), "K")
    try:
        temp=pygame.transform.scale(pygame.image.load("./images/students/"+str(item)),(50,50))
        studentpics.append(temp)
    except:pass



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#DEFINITIONS

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#tkinter window setup
try:
    tkWindow=Tk()
    tkWindow.withdraw()
except:pass
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""SPRITE GROUPS
-allsprites is just a universal blanket sprite group for modifying values
-all the other values contain everything individually
"""
allsprites=pygame.sprite.Group()
ui=pygame.sprite.Group()
#Students is the universal class for all students, and students_graphics is the class for students that will be drawn
students=pygame.sprite.Group()
students_graphics=pygame.sprite.Group()
superstudents=pygame.sprite.Group()

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#icon definition
pygame.display.set_caption("KROOG")
icon = pygame.image.load("images/icon.ico")
pygame.display.set_icon(icon)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#graphics initialization
WIN = pygame.display.set_mode((600, 800),pygame.SCALED)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#BG CODE
bgimages=[];bgframe=1;bg_inc=True #inc means its going forwards, inc false means its going backwards
while True:
    try:
        bgimages.append(pygame.transform.scale(pygame.image.load("./images/bg/bg ("+str(bgframe)+").png"),(600,800)));bgframe+=1
    except:break
bgframe=0

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#EXTRA IMAGES
pause_alert=pygame.image.load("./images/paused.png")

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#ITEM CODE
shake_stoppers=1#00
students=pygame.sprite.Group()
click_up=1
student_click_up=1
doubles=0

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#GAME VALUE CODE 
FPS=30;points=0;run=True #self explanatory
clock=pygame.time.Clock() #self explanatory
multiplier=1 #how many times should you click
playsession_clicks=0 #for voiceline purposes
mute=False #self explanatory
start=time.time() #time starter for recording total boot time 

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#AUDIO LOADING
pygame.mixer.init()
pygame.mixer.set_num_channels(10)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#UI FUNCTIONS

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#TKINTER WINDOW CODE

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#UNIVERSAL PRICE UPDATING CODE
def update_price(function,x=0,y=0,z=0):
        try: return eval(function)
        except OverflowError:return float('inf')

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#SAVING
def save_data(points,shake_stoppers,click_up,student_click_up,doubles,students,superstudents):
    WIN.blit(pause_alert,(0,0));pygame.display.update() #HALTING THE SCREEN
    """SAVING DATA
    Two individual items are taken into consideration when a value is loaded: normal values and students
    Values are simple, all they do is copy a number and save them.
    Students are different, for the game cycles through all of them and takes their image and their stats
    It then saves the item as a .KROOG file, a joke file that works as a normal text file
    """
    final_dict={"data":[points,shake_stoppers,click_up,student_click_up,doubles],"students":[],"superstudents":[]}
    for item in students:
        final_dict["students"].append([item.speed])
    for item in superstudents:
        final_dict["superstudents"].append([item.pkgvalue])
    filename=filedialog.asksaveasfilename()
    print(filename)
    try:
        with open(filename,"w") as file:file.write(str(final_dict))
        print("DATA WRITTEN.")
    except Exception as e: print("ERROR:",str(e))

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#LOADING
def load_data():
    WIN.blit(pause_alert,(0,0));pygame.display.update() #HALTING THE SCREEN
    """LOADING DATA
    this just takes the dictionary from save_data and returns it"""
    filename=filedialog.askopenfilename()
    try:
        with open(filename,"r") as file:file=eval(file.read())
    except:return None
    return file

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#ASSETS

#TITLE      
class Title(pygame.sprite.Sprite):
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)
        self.imgdir=image
        self.image=pygame.image.load(self.imgdir)
        self.rect=self.image.get_rect()
        self.rect.center=(300,100)
        self.rotate=-5;self.inc=True;self.totalinc=-5
    def update(self):
    #making the logo bounce from side to side
        if self.inc: self.rotate+=1 #updating rotation value
        else: self.rotate-=1 #updating rotation value
        self.totalinc+=self.rotate #checking total rotation value
        if self.totalinc==0:self.image=pygame.image.load(self.imgdir) #resetting the photo to prevent degradation
        if self.rotate>=5:self.inc=False #changing direction to turn left
        elif self.rotate<=-5:self.inc=True #changing direction to turn right
        self.image=pygame.transform.rotate(self.image,self.rotate);self.rect=self.image.get_rect()
        self.rect.center=(300,100)
    def update_values(self,values):pass

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#BUTTON
class MainButton(pygame.sprite.Sprite):
    def __init__(self,image,points,pos=(300,400)):
        pygame.sprite.Sprite.__init__(self)
        self.pos=pos #THIS IS THE DEFAULT POS. THIS IS TO PREVENT HIM FROM MOVING OFF SCREEN
        self.image=pygame.image.load(image)
        self.rect=self.image.get_rect()
        self.rect.center=self.pos
        self.points=points
        self.shake_stoppers=0
    def update(self):
        self.rect.center=self.pos
        curCenter=list(self.rect.center)
        #ERROR PREVENTION
        if ((self.points)/(8**self.shake_stoppers))>=10000: self.rect.center=(1000,1000)#PREVENTING THE GAME FROM CRASHING 
        else:
            curCenter[0]+=(
                random.randint(
                    int(round((self.points*-1)/(10**self.shake_stoppers),0)),
                    int(round((self.points)/(10**self.shake_stoppers),0))
                    )
                )
            curCenter[1]+=(
                random.randint(
                    int(round((self.points*-1)/(10**self.shake_stoppers),0)),
                    int(round((self.points)/(10**self.shake_stoppers),0))
                    )
                )
            self.rect.center=tuple(curCenter)
    def update_values(self,values):
        self.points=values[0]
        self.shake_stoppers=values[1]
    def collision(self,pos):
        #print(str(self.rect.left),str(pos[0]),str(self.rect.right))
        #print(str(self.rect.top),str(pos[1]),str(self.rect.bottom))
        if (pos[0] > self.rect.left and pos[0] < self.rect.right) and (pos[1] < self.rect.bottom and pos[1] > self.rect.top): return True
        else: return False   

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#SCORE
class PointDisplay(pygame.sprite.Sprite):
    def __init__(self,pos,points,size=50,valueCounting=0,secondaryValueCounting=None):
        pygame.sprite.Sprite.__init__(self)
        pygame.font.init()
        self.points,self.pos,self.size,self.valueCounting,self.secondaryValueCounting=points,pos,size,valueCounting,secondaryValueCounting
        self.font=pygame.font.Font("./font.ttf",self.size)
        self.surface=self.font.render(str(self.simplify()),True,(255,255,255));self.image=self.surface
        self.rect=self.surface.get_rect()
        self.rect.center = self.pos
    def simplify(self):
        if self.points==float('inf'):return float('inf')
        if type(self.points)==str:return self.points
        if self.points<10**3:return self.points
        elif self.points<10**6:return str(round((self.points/10**3),2)) + "K" #less than a million
        elif self.points<10**9:return str(round((self.points/10**6),2)) + "M" #less than a billion
        elif self.points<10**12:return str(round((self.points/10**9),2)) + "B" #less than a trillion
        elif self.points<10**15:return str(round((self.points/10**12),2)) + "T" #less than a quadrillion
        elif self.points<10**18:return str(round((self.points/10**15),2)) + "Q" #less than a quadrillion
        else: return str(round((self.points/10**18),2)) + "kroog"
    def update(self):
        pass
    def update_values(self,values):
        if self.valueCounting==None:return
        if self.secondaryValueCounting==None:self.points=values[self.valueCounting]
        else:self.points=values[self.valueCounting][self.secondaryValueCounting]
        self.surface=self.font.render(str(self.simplify()),True,(255,255,255));self.image=self.surface
        self.rect=self.surface.get_rect()
        self.rect.center=self.pos

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#BUTTON
class Button(pygame.sprite.Sprite):
    def __init__(self,image,pos=(300,700),center=True):
        pygame.sprite.Sprite.__init__(self)
        self.lock=False
        self.pos=pos #THIS IS THE DEFAULT POS. THIS IS TO PREVENT HIM FROM MOVING OFF SCREEN
        self.imgfile=image #saving original image in case the image changes
        self.image=pygame.transform.scale(pygame.image.load(image),(50,50))
        self.rect=self.image.get_rect()
        self.center=center
        if center:self.rect.center=self.pos
        else:self.rect.x,self.rect.y=self.pos[0],self.pos[1]
    def update(self):pass
    def collision(self,pos):
        if self.lock:return False
        elif (pos[0] > self.rect.left and pos[0] < self.rect.right) and (pos[1] < self.rect.bottom and pos[1] > self.rect.top): return True
        else:return False
    def update_photo(self,imgfile): #updating the photo, self-explanatory
        self.image=pygame.transform.scale(pygame.image.load(imgfile),(50,50))
        self.rect=self.image.get_rect()
        if self.center:self.rect.center=self.pos
        else:self.rect.x,self.rect.y=self.pos[0],self.pos[1]
    def lockbutton(self):
        self.update_photo("./images/icon_lock.png")
        self.lock=True
    def unlock(self):
        self.update_photo(self.imgfile)
        self.lock=False
    def update_values(self,values):pass

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#STUDENT
class Student(pygame.sprite.Sprite):
    def __init__(self,graphic=False):
        #basic initialization stuff
        pygame.sprite.Sprite.__init__(self)
        self.has_package=False #explained in "run"
        self.baseTimer=random.randint(1,10) #lower the number, faster points are generated
        self.timer=0
        self.start=time.time()
        self.graphic=graphic
        if self.graphic:
            #image code
            self.image=random.choice(studentpics)#selecting a random images
            self.image=pygame.transform.scale(self.image,(50,50)) #resizing the image
            self.rect=self.image.get_rect()
            #positioning code
            self.rect.center=(250,400)
            self.direction="l"
        else:pass


    def update(self):
        self.package()
        if self.graphic:self.movement()
    def package(self):
        #package code
        if time.time()-self.start>=self.timer:self.has_package=True;self.start=time.time()
    def movement(self):
        #moving left and right
        if self.direction=='r':self.rect.x+=self.speed
        if self.direction=='l':self.rect.x-=self.speed
        #changing directions
        if self.direction=='r' and self.rect.center[0]>=500:self.direction='l';self.rect.center=(500,self.rect.center[1])
        if self.direction=='l' and self.rect.center[0]<=100:self.direction='r';self.rect.center=(100,self.rect.center[1])
        #vertical code
        if self.direction=='r': self.rect.y=200+(0.005*(self.rect.center[0]-300)**2)
        if self.direction=='l': self.rect.y=575-(0.005*(self.rect.center[0]-300)**2)
    def update_values(self,values):
        self.timer=self.baseTimer/(2**values[3])
        self.speed=5+(random.uniform(1,2)**values[3])

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#SUPERSTUDENT
class SuperStudent(pygame.sprite.Sprite):
    def __init__(self,clicks=0,pkgvalue=0):
        #basic initialization stuff
        pygame.sprite.Sprite.__init__(self)
        self.image=random.choice(studentpics)#selecting a random images
        self.image=pygame.transform.scale(self.image,(50,50))#resizing the image
        self.rect=self.image.get_rect()
        #positioning stuff
        self.pos = [random.randint(0,600),random.randint(0,800)]
        self.rect.center=(random.randint(self.pos[0]-5,self.pos[0]+6),random.randint(self.pos[1]-5,self.pos[1]+6))
        #figuring out package generation values -- DEFAULTS AT PKGVALUE. IF PKGVALUE IS 0, RESORTS TO INDIVIDUAL VALUES. IF INDIVIDUAL VALUES ARE 0, NO SPAWN
        self.pkgvalue=pkgvalue
        if pkgvalue==0: #error checking if pkgvalue is 0
            if clicks==0: print("LOAD ERROR");self.kill() #This is if no values are loaded, which occurs from an error
            else:self.pkgvalue=((clicks//10)*5120)

        self.packages=0
    def update(self):
        self.packages+=self.pkgvalue
        self.rect.center=(random.randint(self.pos[0]-5,self.pos[0]+6),random.randint(self.pos[1]-5,self.pos[1]+6))
    def update_values(self,values):pass

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#SOUNDS
class Sounds:
    muted=False
    squash=pygame.mixer.Sound("sounds/Squish Pop.mp3")
    welcome=pygame.mixer.Sound("sounds/announcements/welcome.wav")
    data_saved=pygame.mixer.Sound("sounds/announcements/data_saved.wav")
    data_loaded=pygame.mixer.Sound("sounds/announcements/data_loaded.wav")
    click_the_kroog=pygame.mixer.Sound("sounds/voicelines/click_the_kroog.wav")
    superstudent_created=pygame.mixer.Sound("sounds/announcements/superstudent_created.wav")
    byebye=pygame.mixer.Sound("sounds/announcements/byebye.wav")
    shake=pygame.mixer.Sound("sounds/announcements/shaking.wav")
    cash=pygame.mixer.Sound("sounds/cash.mp3")
    sounds=[squash,welcome,data_saved,data_loaded,click_the_kroog,superstudent_created,byebye,shake,cash] #putting all items in a list for organization
    for item in sounds:item.set_volume(0.75) #setting volume
    cash.set_volume(0.25)
    voicelines=os.listdir("./sounds/voicelines")
    def kroog_propaganda(self):
        if self.muted:return #skips if muted
        self.click_the_kroog.set_volume(random.uniform(0,0.25))
        pygame.mixer.Channel(4).play(self.click_the_kroog)
    def random_voiceline(self):
        if self.muted:return #skips if muted
        try:
            vc=random.choice(self.voicelines);self.voicelines.remove(vc) #random sounds
            vc=pygame.mixer.Sound("./sounds/voicelines/"+str(vc))
            pygame.mixer.Channel(2).play(vc)
        except:self.click_the_kroog.play() #it doesn't loop, everything just becomes click_the_kroog    
    def selected_voiceline(self,type):
        if type.lower()=="load":
            pygame.mixer.Channel(3).play(self.data_loaded)
        if type.lower()=="save":
            pygame.mixer.Channel(3).play(self.data_saved)
        if type.lower()=="welcome":
            pygame.mixer.Channel(3).play(self.welcome)
        if type.lower()=="bye" or type.lower=="byebye":
            pygame.mixer.Channel(3).play(self.byebye)
        if type.lower()=="shake" or type.lower()=="shaking":
            pygame.mixer.Channel(3).play(self.shake)
        if type.lower()=="superstudent":
            pygame.mixer.Channel(3).play(self.superstudent_created)
    def cashPlay(self):
        pygame.mixer.Channel(1).play(self.cash)
    def mute(self):
        self.muted=True
        for item in self.sounds:item.set_volume(0)
    def unmute(self):
        self.muted=False
        for item in self.sounds:item.set_volume(0.75)
class Music:
    #basic setup
    pygame.mixer.music.set_volume(0.5)
    #fetches directory and shuffles it
    musicqueue=os.listdir("./ost/")
    random.shuffle(musicqueue)
    #1% rickroll
    if random.randint(0,100)==50:musicqueue[0]="rickroll.mp3"
    #loads in the music
    try:pygame.mixer.music.load("./ost/"+str(musicqueue[0])) #loading from ost folder
    #error handling in case you input the wrong directory
    except:
        try:pygame.mixer.music.load("./sounds/"+str(musicqueue[0])) #loading from sounds folder
        except:pygame.mixer.music.load("./defaults/default_song.mp3") #loading default song
    pygame.mixer.music.play()
    #deletes the current song from the shuffle directory to load the next
    musicqueue.pop(0)
    def update(self):
        #checks if no songs are playing
        if not pygame.mixer.music.get_busy(): 
            #loads in the music
            try:
                pygame.mixer.music.load("./ost/"+str(self.musicqueue[0]))
            except IndexError: 
                #fetches directory and shuffles it -- ERROR HANDLING WHEN LIST IS EMPTY
                self.musicqueue=os.listdir("./ost/")
                random.shuffle(self.musicqueue)
            pygame.mixer.music.play()
            #deletes the current song
            self.musicqueue.pop(0)
    def mute(self):pygame.mixer.music.set_volume(0)
    def unmute(self):pygame.mixer.music.set_volume(0.5)

#ADDING ASSETS

kroog=MainButton("images/KROOG.png",points);allsprites.add(kroog);ui.add(kroog)
title=Title("images/title.png");allsprites.add(title);ui.add(title)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#BUTTON ASSETS
shakebutton=Button("images/icon_shake.png",(100,700));allsprites.add(shakebutton);ui.add(shakebutton)
powerbutton=Button("images/icon_click.png",(200,700));allsprites.add(powerbutton);ui.add(powerbutton)
studentbutton=Button("images/icon_student.png",(300,700));allsprites.add(studentbutton);ui.add(studentbutton)
doublebutton=Button("images/icon_double.png",(400,700));allsprites.add(doublebutton);ui.add(doublebutton)
studentpowerbutton=Button("images/icon_studentclick.png",(500,700));allsprites.add(studentpowerbutton);ui.add(studentpowerbutton)
savebutton=Button("images/icon_save.png",(550,0),False);allsprites.add(savebutton);ui.add(savebutton)
loadbutton=Button("images/icon_load.png",(550,50),False);allsprites.add(loadbutton);ui.add(loadbutton)
mutebutton=Button("images/icon_unmuted.png",(50,0),False);allsprites.add(mutebutton);ui.add(mutebutton)
exitbutton=Button("images/icon_exit.png",(0,0),False);allsprites.add(exitbutton);ui.add(exitbutton)
# prestigebutton=Button("images/icon_darth.png",(300,400));allsprites.add(prestigebutton);ui.add(prestigebutton)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#COUNTER ASSETS
pointdisplay=PointDisplay((300,600),points);allsprites.add(pointdisplay);ui.add(pointdisplay)
shake_counter=PointDisplay((100,750),shake_stoppers,20,1);allsprites.add(shake_counter);ui.add(shake_counter)
click_counter=PointDisplay((200,750),click_up,20,2);allsprites.add(click_counter);ui.add(click_counter)
student_counter=PointDisplay((300,750),len(students),20,4);allsprites.add(student_counter);ui.add(student_counter)
double_counter=PointDisplay((400,750),doubles,20,3);allsprites.add(double_counter);ui.add(double_counter)
studentclick_counter=PointDisplay((500,750),student_click_up,20,6);allsprites.add(studentclick_counter);ui.add(studentclick_counter)
superstudent_counter=PointDisplay((300,625),len(superstudents),20,7);allsprites.add(superstudent_counter);ui.add(superstudent_counter)
versionDisplay=PointDisplay((300,10),version,15,None);allsprites.add(versionDisplay);ui.add(versionDisplay)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#PRICE DISPLAY ASSETS
shake_costdisplay=PointDisplay((100,775),0,20,5,0);allsprites.add(shake_costdisplay);ui.add(shake_costdisplay)
click_costdisplay=PointDisplay((200,775),0,20,5,1);allsprites.add(click_costdisplay);ui.add(click_costdisplay)
student_costdisplay=PointDisplay((300,775),0,20,5,2);allsprites.add(student_costdisplay);ui.add(student_costdisplay)
double_costdisplay=PointDisplay((400,775),0,20,5,3);allsprites.add(double_costdisplay);ui.add(double_costdisplay)
studentclick_costdisplay=PointDisplay((500,775),0,20,5,4);allsprites.add(studentclick_costdisplay);ui.add(studentclick_costdisplay)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#PRICE DECLARATION -- SELF-EXPlANATORY
shake_price=0
power_price=0
student_price=0
double_price=0
studentclick_price=0

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#LOCK DECLARATION -- MAXIMUM AMOUNT OF ITEMS PURCHASABLE
shake_lock=0
power_lock=0
student_lock=0
double_lock=0
studentclick_lock=0

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#MULTIPLIER ASSETS
x1=Button("images/multipliers/icon_x1.png",(10,100),False);allsprites.add(x1);ui.add(x1)
x5=Button("images/multipliers/icon_x5.png",(0,200),False);allsprites.add(x5);ui.add(x5)
x10=Button("images/multipliers/icon_x10.png",(0,300),False);allsprites.add(x10);ui.add(x10)
x50=Button("images/multipliers/icon_x50.png",(0,400),False);allsprites.add(x50);ui.add(x50)
x100=Button("images/multipliers/icon_x100.png",(0,500),False);allsprites.add(x100);ui.add(x100)
multipliers=[x1,x5,x10,x50,x100]

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#AUDIO
sounds=Sounds()
music=Music()
sounds.selected_voiceline("welcome")

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#TEST OUTPUTS
#print(random.choice(os.listdir("./images/students/")))


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

while run:
    clock.tick(FPS) #fpv fix
    if points<0:points=0 #error prevention

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    """UPDATING VALUES IN SPRITES
    the values list is used to update values in a sprite object
    the values are stored in a list to prevent the game from crashing from too many arguments
    [points,shake_stoppers,click_up,doubles,len(students),[shake_price,power_price,student_price,double_price]]
    """
    for item in allsprites: item.update_values([
        points,
        shake_stoppers,
        click_up,
        doubles,
        len(students),
        [shake_price,power_price,student_price,double_price,studentclick_price],
        student_click_up,
        len(superstudents)
        ])
    
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    """CHECKING FOR STUDENT PACKAGES
    the game will iterate through every student to check if they have points to return
    if they do, it takes the points and marks the package as false
    """
    for item in students:
        if item.has_package:
            points+=student_click_up
            #print("package converted")
            item.has_package=False
    
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    """CREATING A SUPER STUDENT
    the game will check and see if doubles is at the amount where students stop moving
    the game will also check and see if there are at least 100 students
    the game then creates a "super student" which contains the total amount of students you have
    the super students will generate a certain amount of revenue every *frame* (30 times a second)
    """
    if doubles>=10:
        doublebutton.update_photo("./images/icon_double.png")
        superstudent=SuperStudent(student_click_up)
        allsprites.add(superstudent);superstudents.add(superstudent)
        students.empty();students_graphics.empty();doubles=0 #emptying student data
        sounds.selected_voiceline("superstudent")
    
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    """TAKING SUPERSTUDENT PACKAGES
    same as students but even simpler
    adds the package to the points, empties the package
    """
    for item in superstudents:
        points+=item.packages
        item.packages=0
    
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    """UPDATING PRICES
    this calculates the prices used for deducting points when an item is purchased
    """
    shake_price=update_price("10**(x)",shake_stoppers)
    power_price=update_price("50*x",click_up)
    student_price=update_price("(100*x)*((1+y)**10)",len(students),len(superstudents))
    double_price=update_price("(10**x)*(5**(1+y))",doubles,len(superstudents))
    studentclick_price=update_price("1000*(x)",student_click_up)
    
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    """UPDATING LOCKS
    this calculates how much of an item you can purchase
    the amount raises depending on how many superstudents you have
    """
    shake_lock=300
    power_lock=1000*(100**len(superstudents))
    student_lock=500
    double_lock=len(students)//50
    studentclick_lock=1000*(10**len(superstudents))
    #print(power_lock)
    
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    """LOCKING ITEMS
    When purchasing an item, if the value has gone past the lock limit, the item will lock and become unpurchasable
    This is the code to do that."""
    if shake_stoppers>=shake_lock and not shakebutton.lock:shakebutton.lockbutton()
    if click_up>=power_lock and not powerbutton.lock:powerbutton.lockbutton()
    if len(students)>=student_lock and not studentbutton.lock:studentbutton.lockbutton()
    if doubles>=double_lock and not doublebutton.lock:doublebutton.lockbutton()
    if student_click_up>=studentclick_lock and not studentpowerbutton.lock:studentpowerbutton.lockbutton()
    
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    """UNLOCKING ITEMS
    When purchasing an item, if the value has gone past the lock limit, the item will lock and will become unpurchasable
    However, there is nothing to automatically unlock an item.
    This is the code to do that.
    It checks to see if the item is NOT at the lock level, and if the item is locked.
    """
    if (shake_stoppers<shake_lock) and (shakebutton.lock): shakebutton.unlock() 
    if (click_up<power_lock) and (powerbutton.lock): powerbutton.unlock() 
    if (len(students)<student_lock) and (studentbutton.lock): studentbutton.unlock() 
    if (doubles<double_lock) and (doublebutton.lock): doublebutton.unlock() 
    if (student_click_up<studentclick_lock) and (studentpowerbutton.lock): studentpowerbutton.unlock() 

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #BG CODE
    if bg_inc:bgframe+=1
    elif not bg_inc:bgframe-=1
    if bgframe>=len(bgimages)-1:bgframe-=1;bg_inc=False
    elif bgframe<=0:bgframe+=1;bg_inc=True
    
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #GRAPHIC UPDATE
    pygame.display.update()
    WIN.blit(bgimages[bgframe],(0,0))
    allsprites.update() #updates EVERYTHING; but everything is DISPLAYED separately
    
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #DRAWING SPRITES IN SEPARATE LAYERS
    superstudents.draw(WIN) 
    students_graphics.draw(WIN)
    ui.draw(WIN)
    
    #MUSIC CODE
    music.update()
    
    
    #CHECKING FOR INPUTS
    for event in pygame.event.get():
        if event == pygame.QUIT:run = False
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button<=3) or event.type==pygame.KEYDOWN:
            """CLICK DETECTION
            all of these buttons have a generic click detection method used to see if they are clicked
            the buttons do not do anything when clicked, but the program does something when they are clicked
            for example, most of the buttons are shop buttons, where they detect a price, subtract the price, and give you something
            """
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            #MAIN BUTTON CLICK DETECTION
            if kroog.collision(pygame.mouse.get_pos()):
                points+=click_up
                playsession_clicks+=1
                #SOUNDS
                if playsession_clicks%(random.randint(1,10))==0:
                    sounds.kroog_propaganda()
                if playsession_clicks%100==0:
                    sounds.random_voiceline()
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            """SHOP BUTTON CLICK DETECTION
            i had to hard code this because a lot of these behave uniquely"""
            if shakebutton.collision(pygame.mouse.get_pos()):
                for i in range(multiplier): #for multiplied purchases
                    if shake_stoppers>=shake_lock:break #checks for a lock: prevents purchase
                    if points>=shake_price:
                        points-=shake_price
                        shake_stoppers+=1
                        shake_price=update_price("10**(x)",shake_stoppers)
                        sounds.selected_voiceline("shake")
                        #SOUND CONTROL
                        sounds.cashPlay()
            if powerbutton.collision(pygame.mouse.get_pos()):
                for i in range(multiplier): #for multiplied purchases
                    if click_up>=power_lock:break #checks for a lock: prevents purchase
                    if points>=power_price:
                        points-=power_price
                        if len(superstudents)==0: click_up+=1
                        else: click_up+=(100**len(superstudents))
                        power_price=update_price("50*x",click_up)
                        #SOUND CONTROl
                        sounds.cashPlay()
            if studentbutton.collision(pygame.mouse.get_pos()):
                #student=Student();allsprites.add(student);students.add(student)
                for i in range(multiplier): #for multiplied purchases
                    if len(students)>=student_lock:break #checks for a lock: prevents purchase
                    if points>=student_price:
                        points-=student_price
                        #calculating if a student should be graphical or not
                        if len(students_graphics)<100:graphic=True
                        else: graphic=False
                        #spawns a student normally
                        student=Student(graphic=graphic);allsprites.add(student);students.add(student)
                        #only makes a student graphical if graphic is true
                        if graphic:students_graphics.add(student)
                        #updating price
                        student_price=update_price("(100*x)*((1+y)**10)",len(students),len(superstudents))
                        #SOUND CONTROL
                        sounds.cashPlay()
            if doublebutton.collision(pygame.mouse.get_pos()):
                for i in range(multiplier): #for multiplied purchases
                    if doubles>=double_lock:break #checks for a lock: prevents purchase
                    if points>=double_price:
                        points-=double_price
                        doubles+=1
                        double_price=update_price("(10**x)*(5**(1+y))",doubles,len(superstudents))
                        #SOUND CONTROL
                        sounds.cashPlay()
                    if doubles>=9:#this is to prevent the game from going over 10 in double values, and also to change the button image
                        doublebutton.update_photo("./images/icon_superstudent.png")
                        break 
            if studentpowerbutton.collision(pygame.mouse.get_pos()):
                for i in range(multiplier): #for multiplied purchases
                    if student_click_up>=studentclick_lock:break #checks for a lock: prevents purchase
                    if points>=studentclick_price:
                        points-=studentclick_price
                        if len(superstudents)==0: student_click_up+=1
                        else: student_click_up+=(10**len(superstudents))
                        student_click_up+=1
                        studentclick_price=update_price("1000*(x)",student_click_up)
                        #SOUND CONTROL
                        sounds.cashPlay()
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            #UI BUTTON CLICK DETECTION
            if loadbutton.collision(pygame.mouse.get_pos()):
                """LOADING ALL DATA
                This takes the dictionary loaded from the file and begins loading all of the data.
                It replaces all current values, loads every student, and replaces their values.
                This is the more complicated part of load_data()
                the name NEEDS to empty out all the students and superstudents to prevent the students from duplicating
                final_dict={"data":[points,shake_stoppers,click_up,student_click_up,doubles],"students":[],"superstudents":[]}
                """
                file=load_data()
                if file==None:break
                for item in students:item.kill()
                for item in superstudents:item.kill()
                students.empty();students_graphics.empty();superstudents.empty()
                points,shake_stoppers,click_up,student_click_up,doubles=file["data"][0],file["data"][1],file["data"][2],file["data"][3],file["data"][4]
                for item in file["students"]:
                    #deciding if a student should be graphic or not
                    #calculating if a student should be graphical or not
                    if len(students_graphics)<100:graphic=True
                    else: graphic=False
                    student=Student(graphic=graphic);allsprites.add(student);students.add(student)
                    #only makes a student graphical if graphic is true
                    if graphic:students_graphics.add(student)
                    #updating speed
                    student.speed=item[0]
                for item in file["superstudents"]:
                    superstudent=SuperStudent(pkgvalue=item[0]);allsprites.add(superstudent);superstudents.add(superstudent)
                print("LOADED.")

                sounds.selected_voiceline("load")
            if mutebutton.collision(pygame.mouse.get_pos()):
                if mute: #unmutes the game
                    mute=False
                    mutebutton.update_photo("./images/icon_unmuted.png")
                    music.unmute()
                    sounds.unmute()
                elif not mute: #mutes the game
                    mute=True
                    mutebutton.update_photo("./images/icon_muted.png")
                    music.mute()
                    sounds.mute()
            if savebutton.collision(pygame.mouse.get_pos()):
                save_data(points,shake_stoppers,click_up,student_click_up,doubles,students,superstudents)
                sounds.selected_voiceline("save")
            if exitbutton.collision(pygame.mouse.get_pos()):
                with open("./statistics.txt","r+") as fileraw:file=eval(fileraw.read());file["total_logons"]+=1;file["total_seconds_played"]+=int(round((time.time()-start),0))
                with open("./statistics.txt","w") as fileraw:fileraw.write(str(file))
                sounds.selected_voiceline("bye")
                run=False;time.sleep(1)
                
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            #MULTIPLIER CLICK DETECTION
            if x1.collision(pygame.mouse.get_pos()):
                multiplier=1
                for item in multipliers:item.rect.x=0;x1.rect.x=20
            if x5.collision(pygame.mouse.get_pos()):
                multiplier=5
                for item in multipliers:item.rect.x=0;x5.rect.x=20
            if x10.collision(pygame.mouse.get_pos()):
                multiplier=10
                for item in multipliers:item.rect.x=0;x10.rect.x=20
            if x50.collision(pygame.mouse.get_pos()):
                multiplier=50
                for item in multipliers:item.rect.x=0;x50.rect.x=20
            if x100.collision(pygame.mouse.get_pos()):
                multiplier=100
                for item in multipliers:item.rect.x=0;x100.rect.x=20

                
