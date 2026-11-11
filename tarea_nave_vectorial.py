
import math
import pygame

ANCHO = 800
ALTO = 600
FPS = 60
FONDO = (12, 16, 32)
BLANCO = (235, 240, 255)
VERDE = (100, 230, 170)
ROJO = (255, 110, 100)
PURPURA = (180, 100, 255)

# Velocidades expresadas en píxeles (o grados) por segundo
VELOCIDAD_NAVE = 220
VELOCIDAD_GIRO = 180
VELOCIDAD_PROYECTIL = 430
COOLDOWN_DISPARO = 250  
VIDA_PROYECTIL = 1800  

ENVOLVER_PANTALLA = True

class Proyectil:
    def __init__(self, x, y, angulo):
        self.x = x
        self.y = y
        self.vx = math.sin(angulo) * VELOCIDAD_PROYECTIL
        self.vy = -math.cos(angulo) * VELOCIDAD_PROYECTIL
        self.tiempo_restante = VIDA_PROYECTIL

    def actualizar(self, dt):
        """Avanza el disparo según el tiempo transcurrido."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.tiempo_restante -= dt * 1000

    def sigue_activo(self):
        """Indica si sigue dentro de la ventana y no ha caducado."""
        dentro = 0 <= self.x <= ANCHO and 0 <= self.y <= ALTO
        return dentro and self.tiempo_restante > 0

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, ROJO, (int(self.x), int(self.y)), 4)


def dibujar_nave(pantalla, x, y, angulo):
    """Gira los puntos del triángulo local y los coloca en la pantalla."""
    puntos_locales = [(0, -25), (-18, 18), (18, 18)]
    puntos_pantalla = []

    coseno = math.cos(angulo)
    seno = math.sin(angulo)

    for px, py in puntos_locales:
        # Rotación alrededor del centro; luego trasladamos a (x, y).
        girado_x = px * coseno - py * seno
        girado_y = px * seno + py * coseno
        puntos_pantalla.append((x + girado_x, y + girado_y))

    pygame.draw.polygon(pantalla, PURPURA, puntos_pantalla, width=2)
    return puntos_pantalla[0]  # La punta exacta de la nave


def main():
    pygame.init()

    # DOUBLEBUF activa el doble buffer para dibujar sin parpadeos.
    pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.DOUBLEBUF)
    pygame.display.set_caption("Nave espacial")
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 24)

    nave_x = ANCHO / 2
    nave_y = ALTO / 2
    angulo = 0.0  # 0 apunta hacia arriba
    proyectiles = []
    ultimo_disparo = -COOLDOWN_DISPARO
    ejecutando = True

    while ejecutando:
        # dt permite que el movimiento sea parecido aunque cambien los FPS.
        dt = reloj.tick(FPS) / 1000.0
        ahora = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_SPACE:
                    if ahora - ultimo_disparo >= COOLDOWN_DISPARO:
                        # El disparo nace en la punta y hereda la dirección.
                        punta_x = nave_x + math.sin(angulo) * 25
                        punta_y = nave_y - math.cos(angulo) * 25
                        proyectiles.append(Proyectil(punta_x, punta_y, angulo))
                        ultimo_disparo = ahora

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            angulo -= math.radians(VELOCIDAD_GIRO) * dt
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            angulo += math.radians(VELOCIDAD_GIRO) * dt

        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            # La nave avanza en la dirección a la que apunta su proa.
            nave_x += math.sin(angulo) * VELOCIDAD_NAVE * dt
            nave_y -= math.cos(angulo) * VELOCIDAD_NAVE * dt

        if ENVOLVER_PANTALLA:
            nave_x %= ANCHO
            nave_y %= ALTO
        else:
            nave_x = max(0, min(ANCHO, nave_x))
            nave_y = max(0, min(ALTO, nave_y))

        # Actualiza y luego conserva solo los proyectiles todavía activos.
        for proyectil in proyectiles:
            proyectil.actualizar(dt)
        proyectiles = [p for p in proyectiles if p.sigue_activo()]

        pantalla.fill(FONDO)
        for proyectil in proyectiles:
            proyectil.dibujar(pantalla)
        dibujar_nave(pantalla, nave_x, nave_y, angulo)

        ayuda = fuente.render("A/D: girar   W: avanzar   Espacio: disparar   Esc: salir", True, BLANCO)
        pantalla.blit(ayuda, (15, 15))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
