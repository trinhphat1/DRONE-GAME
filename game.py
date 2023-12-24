#khai báo các thư viện cần thiết
import pygame,sys
import random
import pygame_menu
from pygame.locals import *
pygame.init()
#bảng màu
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# size màn hình 
width = 500
height = 500
width1=90
screen=pygame.display.set_mode((width,height))
#thời gian
clock = pygame.time.Clock()
#tên game 
pygame.display.set_caption('DRONE GAME')
#tạo icon cho game
icon=pygame.image.load("D:\\plane\\drone.png")
pygame.display.set_icon(icon)
#tải hình nền
bg=pygame.image.load("D:\\plane\\background.jpg")
bg=pygame.transform.scale2x(bg)
#nhạc nền
music=pygame.mixer.music.load("D:\\plane\\music.mp3")
pygame.mixer.music.play(-1)
#kiểu chữ và cõ chữ
game_over_font = pygame.font.Font('freesansbold.ttf', 40)
menu = pygame_menu.Menu('Welcome', 400, 300,theme=pygame_menu.themes.THEME_BLUE)

menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)
#hàm kết thúc game khi drone bỏ lỡ một đơn hàng
def game_over():
    game_over_text = game_over_font.render("GAME OVER",True, (255,255,255))
    screen.blit(game_over_text, (135, 200))
#tạo đối tượng Drone
class DRONE(pygame.sprite.Sprite):

    def __init__(self, width, height):
        super().__init__() # khai báo thừa kế từ class Sprite của pygame
        self.w = width
        self.h = height
        drone = pygame.image.load('D:\\plane\\drone.png') # load ảnh DRONE
        self.image = pygame.transform.scale(drone, (width1, width1)) # scale lại kính thước
        self.rect = self.image.get_rect() # khung chữ nhật bao quanh DRONE
        self.speed_x = 0 # tốc độ theo phương x
        self.speed_y = 0# tốc độ theo phương y

    # hàm set vị trí
    def set_pos(self,x,y):
        self.rect.x = x 
        self.rect.y = y

    # hàm thay đổi tốc độ 
    # hàm di chuyển theo tốc độ 
    def change_speed(self,a,b):
        self.speed_x += a
        self.speed_y += b

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    # hàm update vị trí (để trống, không cần làm gì)
    def update(self):
        pass # pass là để trống, không cần làm gì

""" Box sẽ là kiện hàng, có init y hệt DRONE nhưng đổi ảnh"""
class Box(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.w = width
        self.h = height
        box = pygame.image.load("D:\\plane\\product.png")
        self.image = pygame.transform.scale(box, (width, width))
        self.rect = self.image.get_rect()
        self.speed_x = 0
        self.speed_y = 0

    # hàm update vị trí
    # Gọi hàm này trong vòng lặp while True sẽ làm cho kiện hàng liên tục bay lên
    def update(self):
        self.rect.y -= self.speed_y

""" customer sẽ là những khách hàng """
class Customer(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.w = width
        self.h = height
        box = pygame.image.load("D:\\plane\\customer.png")
        self.image = pygame.transform.scale(box, (width1, width1))
        self.rect = self.image.get_rect()
        self.speed_x = 0
        self.speed_y = 0

    # hàm reset vị trí
    # khi bị bắn trúng hoặc khi rơi đụng cạnh dưới thì gọi hàm này để customer quay trở lại phía trên
    def reset_pos(self):
        self.rect.x = random.randint(0,width)
        self.rect.y = 30
    # gọi hàm này trong vòng lặp while True để customer liên tục rơi xuống
    def update(self):
        self.rect.y += self.speed_y

pygame.init()

"""ta cần 3 Group để sau này tiện check va chạm giữa các Group"""
all_sprite_list = pygame.sprite.Group() # Group chứa tất cả sprite
customer_list = pygame.sprite.Group() # Group chứa tất cả customer
box_list = pygame.sprite.Group() # Group chứa tất cả box

# khởi tạo Drone của người chơi
player = DRONE(60,80)
player.set_pos(width/2,height/80)
all_sprite_list.add(player) # thêm player vào Group all sprite

# khởi tạo nhiều customer
for i in range(5):
    customer = Customer(30,20)
    customer.reset_pos()
    customer.speed_y = 1 # cho tốc độ phương y là 1, tức là customer sẽ rơi xuống với tốc độ 1
    all_sprite_list.add(customer) # thêm vào Group all sprite
    customer_list.add(customer) # thêm vào Group enemy

font = pygame.font.SysFont('Calibri',20,True,False) # khai bào font chữ để hiển thị điểm bắn được

score = 0 # biến điểm, sẽ bằng số enemy bắn trúng
def start_the_game():
    global score
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.KEYDOWN:# nếu phát hiện có 1 phím được bấm xuống
                if event.key==pygame.K_a:#nếu phím đó là a
                    player.change_speed(-5,0) # thay đổi tốc độ theo phương x, đang là 0 xuống thàng -5
                if event.key==pygame.K_d:
                    player.change_speed(5,0) # thay đổi tốc độ phương x, đang là 0 lên thành 5 --> di chuyển qua phải  
            if event.type == pygame.KEYDOWN: #nếu phát hiện có 1 phím được bấm xuống    
                if event.key == pygame.K_w: 
                    player.change_speed(0,-3) # thay đổi tốc độ phương y, đang là 0 lên thành 5 --> di chuyển lên trên  
                if event.key == pygame.K_s: 
                    player.change_speed(0,3) # thay đổi tốc độ phương y, đang là 0 lên thành -5 --> di chuyển xuống dưới  
                if event.key == pygame.K_SPACE: # nếu bấm SPACE
                    box = Box(20,30) # khởi tạo 1 kiện hàng
                    box.speed_y = 7 # set tốc độ y (tốc độ bay lên) của kiện hàng
                    box.rect.x = player.rect.x + player.w/2 - box.w/2 # set x của đạn về tâm của drone
                                                                        # rect.x trả về toạ độ góc trên bên trái của sprite chứ ko phải toạ độ tâm
                    box.rect.y = player.rect.y + player.h/2 - box.h/2 # set y của kiện hàng về tâm của drone
                    all_sprite_list.add(box) # thêm đạn vào Group all sprite
                    box_list.add(box) # thêm đạn vào Group box

            if event.type == pygame.KEYUP: #nếu phát hiện phím được nhấc lên thì không di chuyển nữa --> đổi các tốc về 0
                if event.key == pygame.K_a: #nếu phím đó là a
                    player.change_speed(5,0) # thay đổi tốc phương x, đang là -5 (hàng 118), tăng 5 thì trở về 0
                if event.key == pygame.K_d: #tương tự trên
                    player.change_speed(-5,0) # tốc x đang là 5, giảm 5 thì về 0
            if event.type == pygame.KEYUP: #nếu phát hiện phím được nhấc lên thì không di chuyển nữa --> đổi các tốc về 0  
                if event.key == pygame.K_w: #tương tự trên
                    player.change_speed(0,0) # tốc y đang là 5, tăng 5 thì về 0
                if event.key == pygame.K_d: #tương tự trên
                    player.change_speed(0,0) # tốc y đang là -5, giảm 5 thì về 0
    # tìm các sprite va chạm giữa 2 Group box và customer
    # kết quả trả về là 1 dictionary kiểu {box : [list các customer có chạm vào box]}
    # True, False nghĩa là sau khi tìm ra thì xoá box có va chạm, nhưng không xoá customer có va chạm
        hit_sprite = pygame.sprite.groupcollide(box_list,customer_list,True,False) 

    # quét qua hit_sprite.
    # hit_sprite là 1 dictionary, key là các box có chạm customer, còn value là list các customer có chạm box
        for box in hit_sprite: # quét key của hit_sprite
            for customer in hit_sprite[box]: # quét list các customer có chạm box
                customer.reset_pos() # reset vị trí customer có chạm box. Lưu ý box thì bị xoá như đã giải thích ở hàng 138
                score += 1 # tăng điểm 
            
        player.move() # gọi hàm move của drone, tốc độ thì đã được thay đổi khi bấm và nhả phím ở trước

        screen.blit(bg,(0,0))
        all_sprite_list.update() # gọi hàm update của tất cả sprite
        all_sprite_list.draw(screen) # vẽ sprite ra

        text = font.render('Score: '+str(score), True, BLACK) # text cần hiển thị điểm
        screen.blit(text,[10,10]) # hiẻn thị điểm ra màn hình
        for customer in customer_list: # quét qua customer list
            if customer.rect.y > 450: #check customer rơi đụng cạnh dưới thì reset vị trí lên trên
                game_over()
            break    
        pygame.display.update()
        clock.tick(60)
        running=True
    menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default=' ')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)
