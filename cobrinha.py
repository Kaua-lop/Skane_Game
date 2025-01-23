import pygame
from pygame.locals import *
import random
import time

WINDOWS_WIDTH = 800 #   Tamanho da janela
WINDOWS_HEIGHT = 600 #Tamanho da janela
BLOCK = 10  #Tamanho do bloco
POS_X = WINDOWS_WIDTH / 2 #Posição inicial da cobrinha
POS_Y = WINDOWS_HEIGHT / 2 #Posição inicial da cobrinha

points = 0
speed = 15

def colider(pos1, pos2): #Verifica se as posições são iguais e retorna True
    return pos1 == pos2
def check_margin(pos):
    if  0 <= pos[0] < WINDOWS_WIDTH and 0 <= pos[1] < WINDOWS_HEIGHT: #Verifica se a posição está dentro da janela
        return False
    else:
        return True
def postion_random():
    x = random.randint(0, WINDOWS_WIDTH) #Retorna uma posição aleatória dentro da janela
    y = random.randint(0, WINDOWS_HEIGHT) #Retorna uma posição aleatória dentro da janela
    
    if(x,y) in obstacle_pos:
        return postion_random()

    return x // BLOCK * BLOCK, y // BLOCK * BLOCK #Retorna a posição da maça dentro do grid
def game_over():
    font = pygame.font.SysFont('Arial', 65, True, True)
    gameOver = 'GAME OVER'
    text = font.render(gameOver, True, (255,255,255))
    screen.blit(text, (200,200))
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    exit()

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 35, True, True)

screen = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT)) #Cria a janela
pygame.display.set_caption('Cobrinha') #Título da janela
pygame.display.set_icon(pygame.image.load('icon.png')) #Ícone da janela
direction = K_LEFT #Direção da cobrinha

obstacle_pos = []
obstacle_surface = pygame.Surface((BLOCK,BLOCK))#Cria a superfície do obstáculo
obstacle_surface.fill((0,0,0))#Preenche a superfície com uma cor


apple_surface = pygame.Surface((BLOCK,BLOCK))#Cria a superfície da maça
apple_surface.fill((255,0,0))#Preenche a superfície com uma cor
apple_pos = postion_random() #Posição da maça


snake_pos = [(POS_X, POS_Y),(POS_X + BLOCK, POS_Y),(POS_X + 2 * BLOCK , POS_Y)] #Posição da cobrinha
snake_surface = pygame.Surface((BLOCK, BLOCK)) #Cria a superfície da cobrinha
snake_surface.fill((33,8,45)) #Preenche a superfície com uma cor

while True: 
    pygame.time.Clock().tick(speed)
    screen.fill((69,190,60)) #Preenche a tela com uma cor

    message = f'Pontos: {points}'
    text = font.render(message, True, (255,255,255))

    for event in pygame.event.get(): #Verifica os eventos
        if event.type == pygame.QUIT: #Verifica se o usuário fechou a janela
            pygame.quit() #Encerra o jogo
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in [K_UP,K_DOWN,K_LEFT,K_RIGHT]: #Verifica se a tleca foi pressionada
                
                #Verifica se a tecla pressionada é diferente da direção da cobrinha Impede que a cobrinha volte para trás
                if event.key == K_UP and direction == K_DOWN:
                    continue
                elif event.key == K_DOWN and direction == K_UP:
                    continue
                elif event.key == K_LEFT and direction == K_RIGHT:
                    continue
                elif event.key == K_RIGHT and direction == K_LEFT:
                    continue

                direction = event.key

    screen.blit(apple_surface, apple_pos) #Desenha a maça

    if colider(snake_pos[0], apple_pos): #Verifica se a cobrinha colidiu com a maça
        snake_pos.append((-10,-10)) # Adiciona uma parte a cobrinha
        apple_pos = postion_random() #Reposiciona a maça
        obstacle_pos.append(postion_random()) #Adiciona um obstáculo
        points += 1 #Adiciona um ponto
        if points % points == 0: #Aumenta a velocidade a cada x pontos
            speed += 3

    for pos in obstacle_pos:
        if colider(snake_pos[0], pos): #Verifica se a cobrinha colidiu com o obstáculo
            game_over()
        screen.blit(obstacle_surface, pos)

    for pos in snake_pos: #Percorre a lista de posições da cobrinha
        screen.blit(snake_surface, pos)

    for item in range(len(snake_pos) - 1, 0, -1): #Fazer com que todas as partes da cobrinha se movam
        if colider(snake_pos[0], snake_pos[item]): #Verifica se a cobrinha colidiu com ela mesma
            game_over()
        snake_pos[item] = snake_pos[item - 1] 
       

    if check_margin(snake_pos[0]): #Verifica se a posição da cobrinha está dentro da janela se não encerra o jogo
        game_over()

    if direction == K_RIGHT:
        snake_pos[0] = snake_pos[0][0] + BLOCK, snake_pos[0][1] #Movimenta para a DIREITA
    
    elif direction == K_LEFT:
        snake_pos[0] = snake_pos[0][0] - BLOCK, snake_pos[0][1] #Movimenta para a ESQUERDA
    
    elif direction == K_UP:
        snake_pos[0] = snake_pos[0][0], snake_pos[0][1] - BLOCK #Movimenta para CIMA
    
    elif direction == K_DOWN:
        snake_pos[0] = snake_pos[0][0], snake_pos[0][1] + BLOCK #Movimenta para BAIXO

    screen.blit(text,(600,30))
    pygame.display.update() #Atualiza a tela