#pygame skeleton
import pygame
import random
import base64

WIDTH=480
HEIGHT=600
FPS=60
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
POWER_TIME_UP = 5000
pygame.init()
pygame.mixer.init()

screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Galactica")
pygame.display.set_icon(pygame.image.load("./img/player.png"))
clock=pygame.time.Clock()

font_name=pygame.font.match_font('arial')

def set_highscore(sc):
    highscore=check_highscore()
    print(highscore)
    highscore_in_no=int(highscore)
    if sc>highscore_in_no:
        hisc=open('imp.txt','w')
        hisc.write(encode("anuran_galactica",str(sc)))
        highscore_in_no=sc
        hisc.close()

def check_highscore():
    hisc=open("imp.txt","r")
    highscore=decode("anuran_galactica",hisc.read())
    hisc.close()
    return highscore

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,WHITE)
    text_rect=text_surface.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text_surface,text_rect)

def draw_shield_bar(surf,x,y,shield):
    if shield < 0:
        shield=0
    BAR_LENGTH=100
    BAR_HEIGHT=10
    fill = (shield / 100) * BAR_LENGTH
    outline_rect=pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect=pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect=img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y= y
        surf.blit(img,img_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def newenem():
    m = Enemy()
    all_sprites.add(m)
    enems.add(m)
    print("enemy added")

def show_game_over_screen():
    screen.blit(background,background_rect)
    draw_text(screen,"Galactica",64,WIDTH/2,HEIGHT/4)
    draw_text(screen,"High Score: "+check_highscore(),24,WIDTH/2,HEIGHT-100)
    draw_text(screen,"Arrow Keys to Move and Space to Fire",22,WIDTH/2,HEIGHT/2)
    draw_text(screen,"Press a key to begin",18,WIDTH/2,HEIGHT * 3 / 4)
    draw_text(screen,"Developed by Anuran Barman",18,WIDTH/2,HEIGHT -20)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        pygame.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting=False

def addUFO():
    global ufoMain
    ufoMain=UFO()
    all_sprites.add(ufoMain)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(player_image,(50,38))
        self.rect=self.image.get_rect()
        self.rect.centerx=WIDTH/2
        self.rect.bottom=HEIGHT-10
        self.speedx=0
        self.radius=20
        self.shield=100
        self.shoot_delay=250
        self.last_shot=pygame.time.get_ticks()
        self.lives=3
        self.hidden=False
        self.hide_timer = pygame.time.get_ticks()
        self.power=1
        self.power_timer=pygame.time.get_ticks()


    def update(self):
        if self.power >=2 and pygame.time.get_ticks()-self.power_timer > POWER_TIME_UP:
            self.power=1
            self.power_timer=pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks()-self.hide_timer > 1000 :
            self.hidden=False
            self.rect.centerx=WIDTH/2
            self.rect.bottom=HEIGHT -10

        self.speedx=0
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx =-5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x +=self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def powerup(self):
        self.power+=1
        self.power_timer=pygame.time.get_ticks()

    def shoot(self):
        now=pygame.time.get_ticks()
        if now-self.last_shot > self.shoot_delay:
            self.last_shot=now
            if self.power ==1:
                shoot_sound.play()
                bullet=Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            if self.power == 2:
                shoot_sound.play()
                bullet1=Bullet(self.rect.left,self.rect.centery)
                bullet2=Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
            if self.power >= 3:
                shoot_sound.play()
                bullet1=Bullet(self.rect.left,self.rect.centery)
                bullet2=Bullet(self.rect.right,self.rect.centery)
                bullet3=Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)


    def hide(self):
        self.hidden=True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2,HEIGHT + 200)
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig=random.choice(meteors)
        self.image=self.image_orig.copy()
        self.rect=self.image.get_rect()
        self.rect.x = random.randrange(WIDTH-self.rect.width)
        self.rect.y = random.randrange(-150,180)
        self.speedy=random.randrange(1,8)
        self.speedx=random.randrange(-3,3)
        self.radius=int(self.rect.width * .85 /2)
        self.rot=0
        self.rot_speed=random.randrange(-8,8)
        self.last_update=pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.y +=self.speedy
        self.rect.x +=self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH +20:
            self.rect.x = random.randrange(WIDTH-self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy=random.randrange(1,8)
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update=now
            self.rot =(self.rot+self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig,self.rot)
            self.image=new_image
            old_center=self.rect.center
            self.rect=self.image.get_rect()
            self.rect.center=old_center

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image=pygame.transform.scale(enemies[0],(50,38))
        self.image=pygame.transform.scale(random.choice(enemies),(50,38))
        self.rect=self.image.get_rect()
        self.rect.x = random.randrange(WIDTH-self.rect.width)
        self.rect.y = random.randrange(-50,10)
        self.speedy=random.randrange(1,8)
        self.speedx=random.randrange(-3,3)
        self.radius=int(self.rect.width * .85 /2)
        self.shoot_delay=250
        self.last_shot=pygame.time.get_ticks()

    def update(self):
        self.rect.x +=self.speedx
        self.rect.y +=self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH +20:
            self.rect.x = random.randrange(WIDTH-self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy=random.randrange(1,8)
        self.shoot()
        # if self.rect.top > HEIGHT + 10:
        #     self.rect.y = random.randrange(-100,-40)
        #     self.speedy=random.randrange(1,8)

    def shoot(self):
        now=pygame.time.get_ticks()
        if now-self.last_shot > self.shoot_delay:
            bullet=EnemyBullet(self.rect.centerx,self.rect.top+50)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
            self.last_shot=now

    


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=laser
        self.rect=self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y +=self.speedy
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(enemy_laser,(10,20))
        self.rect=self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10
    def update(self):
        self.rect.y +=self.speedy
        if self.rect.bottom > HEIGHT:
            self.kill()

class UFOBullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(ufo_bullet,(20,20))
        self.rect=self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10
    def update(self):
        self.rect.y +=self.speedy
        if self.rect.bottom > HEIGHT:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type=random.choice(['shield','gun'])
        self.image=powerup_images[self.type]
        self.rect=self.image.get_rect()
        self.rect.center = center
        self.speedy = 2
    def update(self):
        self.rect.y +=self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class UFO(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=random.choice(ufos)
        self.rect=self.image.get_rect()
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.rect.y=-100
        self.shield=100
        self.speedy=3
        self.last_shot=pygame.time.get_ticks()
        self.shoot_delay=250
        self.radius=int(self.rect.width * .85 /2)
    
    def update(self):
        if self.rect.y < 100:
            self.rect.y +=self.speedy
        self.shoot()
        

    def shoot(self):
        now=pygame.time.get_ticks()
        if now-self.last_shot > self.shoot_delay:
            bullet=UFOBullet(self.rect.centerx,self.rect.top+50)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
            self.last_shot=now


class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size=size
        self.image=explosion_anim[self.size][0]
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.frame=0
        self.last_update=pygame.time.get_ticks()
        self.frame_rate=75
    def update(self):
        now= pygame.time.get_ticks()
        if now-self.last_update > self.frame_rate:
            self.last_update=now
            self.frame+=1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center=self.rect.center
                self.image= explosion_anim[self.size][self.frame]
                self.rect=self.image.get_rect()
                self.rect.center=center

score=0
ufoMain= None
ufos=[]
ufo_image_list=['ufoRed.png','ufoBlue.png','ufoBlue.png','ufoYellow.png']
for img in ufo_image_list:
    ufos.append(pygame.image.load("./img/"+img))

ufo_bullet=pygame.image.load("./img/ufo_bullet.png")
background=pygame.image.load("./img/bg.png")
background_rect=background.get_rect()
player_image=pygame.image.load("./img/player.png")
player_image_mini=pygame.transform.scale(player_image,(25,19))
meteors=[]
meteors_img_list = ['meteor.png','meteor2.png','meteor3.png']
for img in meteors_img_list:
    meteors.append(pygame.image.load("./img/"+img))

enemies=[]
enemies_img_list = ['enemy1.png','enemy2.png','enemy3.png','enemy4.png']
for img in enemies_img_list:
    print('adding image '+img)
    enemies.append(pygame.image.load("./img/"+img))

laser=pygame.image.load("./img/laser.png")
enemy_laser=pygame.image.load("./img/enemy_laser.png")
explosion_anim = {}
explosion_anim['lg']=[]
explosion_anim['sm']=[]
explosion_anim['player']=[]
for i in range(9):
    filename='regularExplosion0{}.png'.format(i)
    img= pygame.image.load("./img/"+filename)
    img_lg=pygame.transform.scale(img,(75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm=pygame.transform.scale(img,(32,32))
    explosion_anim['sm'].append(img_sm)
    filename='sonicExplosion0{}.png'.format(i)
    img = pygame.image.load("./img/"+filename)
    explosion_anim['player'].append(img)

powerup_images={}
powerup_images['shield']=pygame.image.load("./img/shield.png")
powerup_images['gun']=pygame.image.load("./img/gun.png")


player_expl_sound=pygame.mixer.Sound("./sounds/rumble1.ogg")
shoot_sound=pygame.mixer.Sound("./sounds/shoot.wav")
shield_power_sound=pygame.mixer.Sound("./sounds/shield_power.ogg")
bullet_power_sound=pygame.mixer.Sound("./sounds/bullet_power.ogg")
exp_sounds=[]
for sound in ['small_m.wav','big_m.wav']:
    exp_sounds.append(pygame.mixer.Sound("./sounds/"+sound))
pygame.mixer.music.load("./sounds/bg_sound.ogg")
pygame.mixer.music.set_volume(0.3)

game_over=True
running=True
ufoAdded=False
ufoTimer=pygame.time.get_ticks()
all_sprites=pygame.sprite.Group()
mobs=pygame.sprite.Group()
enems=pygame.sprite.Group()
bullets=pygame.sprite.Group()
enemy_bullets=pygame.sprite.Group()
powerups=pygame.sprite.Group()
player=Player()
all_sprites.add(player)
for i in range(8):
    newmob()
for i in range(4):
    newenem()
pygame.mixer.music.play(loops=-1)
while running:
    if game_over:
        
        score=0
        show_game_over_screen()
        game_over=False
        all_sprites=pygame.sprite.Group()
        mobs=pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        enemy_bullets=pygame.sprite.Group()
        powerups=pygame.sprite.Group()
        enems=pygame.sprite.Group()
        player=Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        for i in range(4):
            newenem()
        pygame.mixer.music.play(loops=-1)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    if score > 1000 and ufoAdded == False:
        addUFO()
        ufoAdded=True
        ufoTimer=pygame.time.get_ticks()
         

    all_sprites.update()

    hits= pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        random.choice(exp_sounds).play()
        expl=Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        score +=50-hit.radius
        if random.random() > 0.9:
            pow=Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    if ufoAdded:
        hits= pygame.sprite.spritecollide(ufoMain,bullets,True,pygame.sprite.collide_circle)
        for hit in hits:
            random.choice(exp_sounds).play()
            expl=Explosion(hit.rect.center,'lg')
            all_sprites.add(expl)
            ufoMain.shield-=10
            if ufoMain.shield < 0:
                expl=Explosion(hit.rect.center,'lg')
                all_sprites.add(expl)
                ufoMain.kill()
                score +=500
                ufoAdded=False
                if random.random() > 0.9:
                    pow=Pow(hit.rect.center)
                    all_sprites.add(pow)
                    powerups.add(pow)
        
    hits=pygame.sprite.spritecollide(player,enemy_bullets,True,pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -=10
        hit.kill()
        expl=Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        random.choice(exp_sounds).play()
        if player.shield <= 0:
            death_explosion=Explosion(player.rect.center,'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -=1
            player.shield=100
    
    hits= pygame.sprite.groupcollide(enems,bullets,True,True)
    for hit in hits:
        random.choice(exp_sounds).play()
        expl=Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        score +=50-hit.radius
        if random.random() > 0.9:
            pow=Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newenem()

    hits=pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -=hit.radius * 2
        newmob()
        expl=Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        if player.shield <= 0:
            player_expl_sound.play()
            death_explosion=Explosion(player.rect.center,'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -=1
            player.shield=100
    
    hits=pygame.sprite.spritecollide(player,enems,True,pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -=hit.radius * 2
        newenem()
        expl=Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        if player.shield <= 0:
            player_expl_sound.play()
            death_explosion=Explosion(player.rect.center,'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -=1
            player.shield=100

    hits = pygame.sprite.spritecollide(player,powerups,True)
    for hit in hits:
        if hit.type == 'shield':
            shield_power_sound.play()
            player.shield += random.randrange(10,30)
            if player.shield > 100:
                player.shield = 100
        if hit.type == 'gun':
            bullet_power_sound.play()
            player.powerup()

    if player.lives == 0 and not death_explosion.alive():
        set_highscore(score)
        game_over=True
        

    screen.fill(BLACK)
    screen.blit(background,background_rect)

    all_sprites.draw(screen)
    draw_text(screen,str(score),28,WIDTH/2,10)
    draw_shield_bar(screen,5,5,player.shield)
    draw_lives(screen,WIDTH-100,5,player.lives,player_image_mini)
    pygame.display.flip()

pygame.quit()
