import pygame
import sys
from enum import Enum
from tablero import Tablero, Pieza, Color  
from min_Max import MinMax


class Juego:
    def __init__(self):
        pygame.init()
        self.TAMANO_CASILLA = 60
        self.ANCHO = self.TAMANO_CASILLA * 16  # Para dos tableros
        self.ALTO = self.TAMANO_CASILLA * 8
        self.pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption('Ajedrez Alice')
        self.tablero = Tablero()
        self.cargar_imagenes()
        self.maquina = MinMax (Color.NEGRO)  # La IA juega con las negras
        self.jugador_vs_ia = True  # Activar modo jugador vs IA
        
        # Variables para el manejo de movimientos
        self.pieza_seleccionada = None
        self.tablero_seleccionado = None
        self.turno_actual = Color.BLANCO
        self.movimientos_validos = []

    def cargar_imagenes(self):
        try:
            self.imagenes = {}
            piezas = {
                Pieza.PEON: 'peon',
                Pieza.CABALLO: 'caballo', 
                Pieza.ALFIL: 'alfil',
                Pieza.TORRE: 'torre',
                Pieza.DAMA: 'dama',
                Pieza.REY: 'rey'
            }
            colores = {
                Color.BLANCO: 'blanco',
                Color.NEGRO: 'negro'
            }
            
            for pieza in Pieza:
                for color in Color:
                    ruta = f"imagenes/{piezas[pieza]}_{colores[color]}.png"
                    try:
                        imagen = pygame.image.load(ruta)
                        imagen = pygame.transform.scale(imagen, (self.TAMANO_CASILLA, self.TAMANO_CASILLA))
                        self.imagenes[(pieza, color)] = imagen
                        print("Imagien cargada con exito:" + ruta)
                    except pygame.error as e:
                        print(f"Error al cargar la imagen: {ruta}")
                        print(f"Error específico: {e}")
                        
        except Exception as e:
            print(f"Error general al cargar imágenes: {e}")

    def dibujar_tablero(self):
        # Dibujar tableros base
        for tablero in range(2):
            offset_x = tablero * self.TAMANO_CASILLA * 8
            for fila in range(8):
                for columna in range(8):
                    # Dibujar las casillas
                    color = (229, 242, 229) if (fila + columna) % 2 == 0 else (189, 172, 97)
                    pygame.draw.rect(self.pantalla, color,
                                   (offset_x + columna * self.TAMANO_CASILLA,
                                    fila * self.TAMANO_CASILLA,
                                    self.TAMANO_CASILLA, self.TAMANO_CASILLA))

        # Resaltar casilla seleccionada
        if self.pieza_seleccionada:
            fila, columna = self.pieza_seleccionada
            offset_x = 0 if self.tablero_seleccionado == 1 else self.TAMANO_CASILLA * 8
            pygame.draw.rect(self.pantalla, (255, 44, 5),
                           (offset_x + columna * self.TAMANO_CASILLA,
                            fila * self.TAMANO_CASILLA,
                            self.TAMANO_CASILLA, self.TAMANO_CASILLA), 3)

        # Resaltar movimientos válidos
        for fila, columna in self.movimientos_validos:
            offset_x = 0 if self.tablero_seleccionado == 1 else self.TAMANO_CASILLA * 8
            pygame.draw.circle(self.pantalla, (0, 0, 0),
                             (offset_x + columna * self.TAMANO_CASILLA + self.TAMANO_CASILLA // 2,
                              fila * self.TAMANO_CASILLA + self.TAMANO_CASILLA // 2),
                             10)

    def obtener_casilla_desde_mouse(self, pos_mouse):
        x, y = pos_mouse
        # Determinar en qué tablero se hizo clic
        if x < self.TAMANO_CASILLA * 8:
            tablero = 1
            columna = x // self.TAMANO_CASILLA
        else:
            tablero = 2
            columna = (x - self.TAMANO_CASILLA * 8) // self.TAMANO_CASILLA
        
        fila = y // self.TAMANO_CASILLA
        return tablero, fila, columna

    def manejar_click(self):
        pos_mouse = pygame.mouse.get_pos()
        tablero, fila, columna = self.obtener_casilla_desde_mouse(pos_mouse)
        
        # Si está fuera del tablero, ignorar el click
        if not (0 <= fila < 8 and 0 <= columna < 8):
            return

        print(f"Click en tablero {tablero}, fila {fila}, columna {columna}")  # Debug

        # Si no hay pieza seleccionada
        if self.pieza_seleccionada is None:
            pieza = self.tablero.obtener_pieza(tablero, fila, columna)
            if pieza and pieza[1] == self.turno_actual:
                print(f"Seleccionando pieza: {pieza}")  # Debug
                self.pieza_seleccionada = (fila, columna)
                self.tablero_seleccionado = tablero
                self.movimientos_validos = self.tablero.movimientos_pieza(
                    pieza[0], (fila, columna), tablero)
        
        # Si hay una pieza seleccionada
        else:
            desde_fila, desde_col = self.pieza_seleccionada
            if (fila, columna) in self.movimientos_validos:
                print(f"Moviendo pieza a {fila}, {columna}")
                self.tablero.realizar_movimiento((
                    self.tablero_seleccionado,
                    (desde_fila, desde_col),
                    (fila, columna)
                ))
                self.turno_actual = Color.NEGRO if self.turno_actual == Color.BLANCO else Color.BLANCO
            
            self.pieza_seleccionada = None
            self.tablero_seleccionado = None
            self.movimientos_validos = []

        # Después de realizar el movimiento del jugador
        if self.turno_actual == self.maquina.color and self.jugador_vs_ia:
            # Hacer que la IA realice su movimiento
            movimiento_ia = self.maquina.obtener_mejor_movimiento(self.tablero)
            if movimiento_ia:
                self.tablero.realizar_movimiento(movimiento_ia)
                self.turno_actual = Color.BLANCO  # Cambiar el turno al jugador

    def dibujar_piezas(self):
        # Dibujar piezas en tablero 1
        for fila in range(8):
            for columna in range(8):
                pieza = self.tablero.tablero1[fila][columna]
                if pieza:  # Si hay una pieza en esta posición
                    imagen = self.imagenes.get(pieza)  # Obtener la imagen correspondiente
                    if imagen:
                        self.pantalla.blit(imagen,
                                         (columna * self.TAMANO_CASILLA,
                                          fila * self.TAMANO_CASILLA))
                      
        # Dibujar piezas en tablero 2
        for fila in range(8):
            for columna in range(8):
                pieza = self.tablero.tablero2[fila][columna]
                if pieza:  # Si hay una pieza en esta posición
                    imagen = self.imagenes.get(pieza)  # Obtener la imagen correspondiente
                    if imagen:
                        self.pantalla.blit(imagen,
                                         ((columna + 8) * self.TAMANO_CASILLA,
                                          fila * self.TAMANO_CASILLA))

    def ejecutar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:  # Click izquierdo
                        self.manejar_click()

            self.dibujar_tablero()
            self.dibujar_piezas()  # Asegurarnos de que se llame a dibujar_piezas
            pygame.display.flip()
