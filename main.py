import pygame
import random
import time

pygame.init()

ancho = 1200
alto = 600
FPS = 60





pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Mi Primer Proyecto")

jugador = pygame.Rect(100, alto - 60, 50, 50)
jugador_velocidad = 10

jugador_imagen = pygame.image.load("Imagenes/tank.png").convert_alpha()
jugador_imagen = pygame.transform.scale(jugador_imagen, (50, 50))  # Escalar la imagen al tamaño deseado (50x50 en este caso)

enemigo_imagen = pygame.image.load("Imagenes/airplane.png").convert_alpha()
enemigo_imagen = pygame.transform.scale(enemigo_imagen, (50, 50))  # Escalar la imagen al tamaño deseado (50x50 en este caso)
enemigo_imagen_girada = pygame.transform.rotate(enemigo_imagen, 180)


bala_imagen = pygame.image.load("Imagenes/bala.png").convert_alpha()
bala_imagen = pygame.transform.scale(bala_imagen, (10, 10))  # Escalar la imagen al tamaño deseado (50x50 en este caso)






balas = []
enemigos = []
enemigo_velocidad = 5

bala_velocidad = 15
bala_color = (255, 0, 0)

reloj = pygame.time.Clock()

vidas = 3
nivel = 1
score = 0
tiempo_inicial = time.time()

tiempo_espera = 1.0

fuente = pygame.font.SysFont(None, 36)

def mostrar_info():
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, (255, 255, 255))
    texto_nivel = fuente.render(f"Nivel: {nivel}", True, (255, 255, 255))
    texto_score = fuente.render(f"Score: {score}", True, (255, 255, 255))
    pantalla.blit(texto_vidas, (10, 10))
    pantalla.blit(texto_nivel, (10, 40))
    pantalla.blit(texto_score, (10, 70))

def dibujar_jugador():
    pantalla.blit(jugador_imagen, jugador)


def dibujar_balas():
    for bala in balas:
        pantalla.blit(bala_imagen, bala)


def dibujar_enemigos():
    for enemigo in enemigos:
        pantalla.blit(enemigo_imagen_girada, enemigo)

def mover_balas():
    for bala in balas:
        bala.y -= bala_velocidad

def mover_enemigos():
    for enemigo in enemigos:
        enemigo.y += enemigo_velocidad

def eliminar_balas_fuera_de_pantalla():
    balas[:] = [bala for bala in balas if bala.y > 0]

def eliminar_enemigos_fuera_de_pantalla():
    global vidas
    enemigos[:] = [enemigo for enemigo in enemigos if enemigo.y < alto]
    for enemigo in enemigos:
        if enemigo.y >= alto:
            vidas -= 1
            enemigos.remove(enemigo)

def generar_enemigo():
    global tiempo_espera
    if time.time() - tiempo_espera >= 0:
        x = random.randint(0, ancho - 50)
        enemigo = pygame.Rect(x, 0, 50, 50)
        enemigos.append(enemigo)
        tiempo_espera = time.time() + random.uniform(0.5, 1.5)

def colisiones():
    global score, vidas
    for enemigo in enemigos:
        if jugador.colliderect(enemigo):
            vidas -= 1
            enemigos.remove(enemigo)
            break
    for bala in balas:
        for enemigo in enemigos:
            if bala.colliderect(enemigo):
                balas.remove(bala)
                enemigos.remove(enemigo)
                score += 10

# Variables de los power-ups
POWERUP_TIEMPO = 10
POWERUP_INMUNE_COLOR = (0, 0, 255)  # Azul
POWERUP_GRANDE_COLOR = (255, 165, 0)  # Naranja
powerups_activos = []

def generar_powerup():
    global powerups_activos, tiempo_inicial
    if len(powerups_activos) < 2 and time.time() - tiempo_inicial >= 10:
        x = random.randint(0, ancho - 30)
        y = random.randint(0, alto - 30)
        tipo_powerup = random.choice(["inmune", "grande"])
        color_powerup = POWERUP_INMUNE_COLOR if tipo_powerup == "inmune" else POWERUP_GRANDE_COLOR
        powerup = {"rect": pygame.Rect(x, y, 30, 30), "tipo": tipo_powerup, "color": color_powerup}
        powerups_activos.append(powerup)
        tiempo_inicial = time.time()


def dibujar_powerups():
    for powerup in powerups_activos:
        pygame.draw.circle(pantalla, powerup["color"], powerup["rect"].center, 15)

def aplicar_powerups(jugador):
    global powerups_activos, bala_velocidad, jugador_velocidad
    powerups_activos_temp = []
    for powerup in powerups_activos:
        if powerup["rect"].colliderect(jugador):
            if powerup["tipo"] == "inmune":
                powerup_timer = time.time()
                jugador_color = (0, 255, 0)  # Verde
                # Aquí puedes agregar el efecto de inmunidad al jugador
                # Por ejemplo, haciendo que el jugador sea invulnerable temporalmente.
            elif powerup["tipo"] == "grande":
                powerup_timer = time.time()
                bala_velocidad += 5  # Aumentamos la velocidad de las balas
                jugador_velocidad += 2  # Aumentamos la velocidad del jugador
                # Aquí puedes agregar el efecto de hacer al jugador más grande temporalmente.
            else:
                # Otros efectos de power-ups aquí
                pass
        else:
            powerups_activos_temp.append(powerup)
    powerups_activos = powerups_activos_temp


# Variables del menú
opciones_menu = ["Jugar", "Instrucciones", "Salir"]
opcion_seleccionada = 0
en_menu = True

def mostrar_menu():
    pantalla.fill((0, 0, 0))
    for i, opcion in enumerate(opciones_menu):
        color = (255, 255, 255) if i == opcion_seleccionada else (128, 128, 128)
        texto_opcion = fuente.render(opcion, True, color)
        pantalla.blit(texto_opcion, (ancho // 2 - texto_opcion.get_width() // 2, 200 + i * 50))
    pygame.display.flip()




# Bucle del menú
while en_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_menu = False
            Iniciar = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones_menu)
            elif event.key == pygame.K_DOWN:
                opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones_menu)
            elif event.key == pygame.K_RETURN:
                if opcion_seleccionada == 0:  # Jugar
                    en_menu = False
                elif opcion_seleccionada == 1:  # Instrucciones
                    print("Instrucciones:")
                    print("Mueve la nave con las teclas izquierda y derecha.")
                    print("Dispara con la tecla ESPACIO.")
                    print("Elimina a todos los enemigos para aumentar el nivel.")
                    print("Cuidado con los enemigos, si te tocan perderás vidas.")
                    print("¡Buena suerte!\n")
                elif opcion_seleccionada == 2:  # Salir
                    en_menu = False
                    Iniciar = False
    


    mostrar_menu()
    

Iniciar = True

while Iniciar:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Iniciar = False
    
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        jugador.x -= jugador_velocidad
        if jugador.x < 0:
            jugador.x = 0
    if teclas[pygame.K_RIGHT]:
        jugador.x += jugador_velocidad
        if jugador.x > ancho - jugador.width:
            jugador.x = ancho - jugador.width
    if teclas[pygame.K_SPACE]:
        bala = pygame.Rect(jugador.centerx - 5, jugador.top, 10, 30)
        balas.append(bala)

    if time.time() - tiempo_inicial >= 10:
        tiempo_inicial = time.time()
        nivel += 1
        enemigo_velocidad += 1
	

    if len(enemigos) < nivel * 10:
        generar_enemigo()

    # Generar y dibujar power-ups
    powerup = generar_powerup()
    if powerup is not None:
        dibujar_powerup()

    # Aplicar efectos de power-ups al jugador
    aplicar_powerups(jugador)

    pantalla.fill((0, 0, 0))

    dibujar_balas()
    mover_balas()
    eliminar_balas_fuera_de_pantalla()
    dibujar_enemigos()
    mover_enemigos()
    eliminar_enemigos_fuera_de_pantalla()
    dibujar_jugador()
    colisiones()
    mostrar_info()

    pygame.display.flip()

    reloj.tick(FPS)

    if vidas <= 0:
        print("¡Has perdido!")
        Iniciar = False

pygame.quit()