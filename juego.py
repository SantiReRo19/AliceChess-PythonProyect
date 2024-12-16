import pygame
import sys
from enum import Enum
from tablero import Tablero, Pieza, Color  
from min_Max import MinMax
import os
import menu

class Juego:
    def __init__(self, player_color=None, jugador_vs_ia=True):
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centra la ventana en la pantalla

        #cargar configuracion con el metodo cargar_configuracion de men

        self.configuracion = menu.cargar_configuracion()
        self.modificador_tamano = self.configuracion["tamano"]
        

        pygame.init()
        self.TAMANO_CASILLA = int(60 * self.modificador_tamano)
        self.MARGEN = int(40 * self.modificador_tamano)
        self.ENCABEZADO = int(120 * self.modificador_tamano)  
        self.PIEZAS_CAPTURADAS = int(160 * self.modificador_tamano)  
        self.ANCHO = self.TAMANO_CASILLA * 16 + self.MARGEN * 2  # Ajustar ancho para dos tableros y márgenes
        self.ALTO = self.TAMANO_CASILLA * 8 + self.MARGEN * 2 + self.ENCABEZADO + self.PIEZAS_CAPTURADAS  # Ajustar alto
        self.pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption('Ajedrez Alice')

        self.boton_menu = pygame.image.load("imagenes/menuIcon.png")
        self.boton_menu = pygame.transform.scale(self.boton_menu, (int(30 * self.modificador_tamano), int(30 * self.modificador_tamano)))
        self.boton_menu = pygame.transform.scale(self.boton_menu, (30, 30))  # Ajustar tamaño del botón

        self.tablero = Tablero()
        self.cargar_imagenes()
        

        # Inicialización del sonido
        pygame.mixer.init()
        pygame.mixer.music.load(self.configuracion["cancion"])
        pygame.mixer.music.set_volume(self.configuracion["volumen"])
        pygame.mixer.music.play(loops=-1)
        self.moverFicha_Sound = pygame.mixer.Sound("sonidos/moverFicha.wav")

        # Si player_color no se especifica, default a blancas
        if player_color is None:
            player_color = Color.BLANCO
        
        # Establecer color de la máquina al color opuesto
        self.maquina = MinMax(Color.BLANCO if player_color == Color.NEGRO else Color.NEGRO)

        # Variables para el manejo de movimientos
        self.pieza_seleccionada = None
        self.tablero_seleccionado = None

        # Establecer turno inicial
        self.turno_actual = Color.BLANCO

        # Agregar el atributo jugador_vs_ia
        self.jugador_vs_ia = jugador_vs_ia
        
        # Si el jugador elige negras, hacer primer movimiento de IA
        if player_color == Color.NEGRO:
            movimiento_ia = self.maquina.obtener_mejor_movimiento(self.tablero, primer_movimiento=True)
            if movimiento_ia:
                pieza_capturada = self.tablero.obtener_pieza(movimiento_ia[0], movimiento_ia[2][0], movimiento_ia[2][1])
                if pieza_capturada:
                    if pieza_capturada[1] == Color.BLANCO:
                        self.piezas_capturadas_blancas.append(pieza_capturada)
                    else:
                        self.piezas_capturadas_negras.append(pieza_capturada)
                self.tablero.realizar_movimiento(movimiento_ia)
                self.ultimo_movimiento = movimiento_ia
                self.moverFicha_Sound.play()
                self.turno_actual = player_color  # Cambiar turno al jugador

        self.movimientos_validos = []
        self.piezas_capturadas_blancas = []
        self.piezas_capturadas_negras = []
        self.ultimo_movimiento = None 
        
        
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
        # Paleta de Colores
        color_claro = (252,213,167)
        color_oscuro = (159,116,99)
        color_fondo_indices = (115,79,67)
        color_indices = (255, 255, 255)
        color_fondo_encabezado = (82, 47, 35)
        color_fondo_piezas_capturadas = (82, 47, 35)
        color_resaltado_origen = (175, 115, 43)
        color_resaltado_destino = (123, 66, 38)

        # Dibujar fondo para el encabezado
        pygame.draw.rect(self.pantalla, color_fondo_encabezado, (0, 0, self.ANCHO, self.ENCABEZADO))

        # Dibujar fondo para los índices y tableros
        pygame.draw.rect(self.pantalla, color_fondo_indices, (0, self.ENCABEZADO, self.ANCHO, self.ALTO - self.ENCABEZADO - self.PIEZAS_CAPTURADAS))

        # Dibujar fondo para las piezas capturadas
        pygame.draw.rect(self.pantalla, color_fondo_piezas_capturadas, (0, self.ALTO - self.PIEZAS_CAPTURADAS, self.ANCHO, self.PIEZAS_CAPTURADAS))

        # Dibujar tableros base
        for tablero in range(2):
            offset_x = tablero * self.TAMANO_CASILLA * 8 + self.MARGEN
            for fila in range(8):
                for columna in range(8):
                    # Dibujar las casillas
                    color = color_claro if (fila + columna) % 2 == 0 else color_oscuro
                    pygame.draw.rect(self.pantalla, color,
                                   (offset_x + columna * self.TAMANO_CASILLA,
                                    fila * self.TAMANO_CASILLA + self.MARGEN + self.ENCABEZADO,
                                    self.TAMANO_CASILLA, self.TAMANO_CASILLA))

        # Resaltar el último movimiento
        if self.ultimo_movimiento:
            (tablero_origen, desde_pos, hasta_pos) = self.ultimo_movimiento
            desde_fila, desde_col = desde_pos
            hasta_fila, hasta_col = hasta_pos
            offset_x_origen = self.MARGEN if tablero_origen == 1 else self.TAMANO_CASILLA * 8 + self.MARGEN
            offset_x_destino = offset_x_origen

            # Dibujar rectángulo resaltado en la posición de origen
            pygame.draw.rect(self.pantalla, color_resaltado_origen,
                           (offset_x_origen + desde_col * self.TAMANO_CASILLA,
                            desde_fila * self.TAMANO_CASILLA + self.MARGEN + self.ENCABEZADO,
                            self.TAMANO_CASILLA, self.TAMANO_CASILLA), 5)

            # Dibujar rectángulo resaltado en la posición de destino
            pygame.draw.rect(self.pantalla, color_resaltado_destino,
                           (offset_x_destino + hasta_col * self.TAMANO_CASILLA,
                            hasta_fila * self.TAMANO_CASILLA + self.MARGEN + self.ENCABEZADO,
                            self.TAMANO_CASILLA, self.TAMANO_CASILLA), 5)

            # Dibujar rectángulo resaltado en la posición de destino del tablero opuesto
            offset_x_destino = self.MARGEN if tablero_origen == 2 else self.TAMANO_CASILLA * 8 + self.MARGEN
            pygame.draw.rect(self.pantalla, color_resaltado_destino,
                           (offset_x_destino + hasta_col * self.TAMANO_CASILLA,
                            hasta_fila * self.TAMANO_CASILLA + self.MARGEN + self.ENCABEZADO,
                            self.TAMANO_CASILLA, self.TAMANO_CASILLA), 5)

        # Agregar línea divisora entre los tableros
        pygame.draw.line(self.pantalla, color_fondo_indices, (self.TAMANO_CASILLA * 8 + self.MARGEN, self.MARGEN + self.ENCABEZADO), (self.TAMANO_CASILLA * 8 + self.MARGEN, self.ALTO - self.MARGEN - self.PIEZAS_CAPTURADAS), 5)

        # Dibujar contorno con índices de posiciones
        font = pygame.font.SysFont(None, int(24 * self.modificador_tamano))
        letras = 'abcdefgh'
        numeros = '12345678'

        for i in range(8):
            # Letras en la parte inferior y superior
            letra = font.render(letras[i], True, color_indices)
            self.pantalla.blit(letra, (i * self.TAMANO_CASILLA + self.TAMANO_CASILLA // 2 - letra.get_width() // 2 + self.MARGEN, self.ALTO - self.MARGEN - self.PIEZAS_CAPTURADAS + 10))
            self.pantalla.blit(letra, (i * self.TAMANO_CASILLA + self.TAMANO_CASILLA // 2 - letra.get_width() // 2 + self.MARGEN, self.MARGEN + self.ENCABEZADO - 30))

            # Números en la parte izquierda y derecha
            numero = font.render(numeros[7 - i], True, color_indices)
            self.pantalla.blit(numero, (self.MARGEN - 30, i * self.TAMANO_CASILLA + self.TAMANO_CASILLA // 2 - numero.get_height() // 2 + self.MARGEN + self.ENCABEZADO))
            self.pantalla.blit(numero, (self.ANCHO - self.MARGEN + 10, i * self.TAMANO_CASILLA + self.TAMANO_CASILLA // 2 - numero.get_height() // 2 + self.MARGEN + self.ENCABEZADO))

            # Letras y números para el segundo tablero
            self.pantalla.blit(letra, (i * self.TAMANO_CASILLA + self.TAMANO_CASILLA // 2 - letra.get_width() // 2 + self.TAMANO_CASILLA * 8 + self.MARGEN, self.ALTO - self.MARGEN - self.PIEZAS_CAPTURADAS + 10))
            self.pantalla.blit(letra, (i * self.TAMANO_CASILLA + self.TAMANO_CASILLA // 2 - letra.get_width() // 2 + self.TAMANO_CASILLA * 8 + self.MARGEN, self.MARGEN + self.ENCABEZADO - 30))

        # Dibujar encabezado
        font_titulo = pygame.font.Font(pygame.font.match_font('timesnewroman'), int(60 * self.modificador_tamano))
        font_indicaciones = pygame.font.Font(pygame.font.match_font('timesnewroman'), int(30 * self.modificador_tamano))
        font_equipo = pygame.font.Font(pygame.font.match_font('timesnewroman'), int(20 * self.modificador_tamano))  # Fuente para el nombre del equipo
        titulo = font_titulo.render("Alice Chess", True, color_indices)
        self.pantalla.blit(titulo, (self.ANCHO // 2 - titulo.get_width() // 2, int(20 * self.modificador_tamano)))

        # Dibujar nombre del equipo
        equipo = font_equipo.render("By LLJS Team", True, color_indices)
        self.pantalla.blit(equipo, (self.ANCHO // 2 - equipo.get_width() // 2, int(90 * self.modificador_tamano)))

        # Dibujar botón de menú en la esquina superior derecha
        self.pantalla.blit(self.boton_menu, (self.ANCHO - self.boton_menu.get_width() - 10, int(10 - self.modificador_tamano)))

        # Dibujar texto para piezas capturadas
        font_piezas_capturadas = pygame.font.Font(pygame.font.match_font('timesnewroman'), int(24 * self.modificador_tamano))  # Reducir tamaño de fuente en un 20%
        texto_piezas_capturadas_blancas = font_piezas_capturadas.render("Piezas capturadas (Blancas):", True, color_indices)
        texto_piezas_capturadas_negras = font_piezas_capturadas.render("Piezas capturadas (Negras):", True, color_indices)
        self.pantalla.blit(texto_piezas_capturadas_blancas, (self.MARGEN, self.ALTO - self.PIEZAS_CAPTURADAS + int(10 * self.modificador_tamano)))
        self.pantalla.blit(texto_piezas_capturadas_negras, (self.ANCHO - self.MARGEN - texto_piezas_capturadas_negras.get_width(), self.ALTO - self.PIEZAS_CAPTURADAS + int(10 * self.modificador_tamano)))

        # Dibujar indicaciones de turno entre los textos de piezas capturadas y el tablero
        if self.turno_actual == Color.BLANCO:
            indicaciones = "Mueven blancas"
        else:
            indicaciones = "Mueven negras"

        indicaciones_texto = font_indicaciones.render(indicaciones, True, color_indices)
        self.pantalla.blit(indicaciones_texto, (self.ANCHO // 2 - indicaciones_texto.get_width() // 2, self.ALTO - self.PIEZAS_CAPTURADAS + int(60 * (self.modificador_tamano / 6 ))))
        
        # Resaltar casilla seleccionada
        if self.pieza_seleccionada:
            fila, columna = self.pieza_seleccionada
            offset_x = self.MARGEN if self.tablero_seleccionado == 1 else self.TAMANO_CASILLA * 8 + self.MARGEN
            pygame.draw.rect(self.pantalla, (255, 44, 5),
                           (offset_x + columna * self.TAMANO_CASILLA,
                            fila * self.TAMANO_CASILLA + self.MARGEN + self.ENCABEZADO,
                            self.TAMANO_CASILLA, self.TAMANO_CASILLA), 3)

        # Resaltar movimientos válidos
        for fila, columna in self.movimientos_validos:
            offset_x = self.MARGEN if self.tablero_seleccionado == 1 else self.TAMANO_CASILLA * 8 + self.MARGEN
            pygame.draw.circle(self.pantalla, (0, 0, 0),
                             (offset_x + columna * self.TAMANO_CASILLA + self.TAMANO_CASILLA // 2,
                              fila * self.TAMANO_CASILLA + self.TAMANO_CASILLA // 2 + self.MARGEN + self.ENCABEZADO),
                             int(10 * self.modificador_tamano))

    def obtener_casilla_desde_mouse(self, pos_mouse):
        x, y = pos_mouse
        # Determinar en qué tablero se hizo clic
        if self.MARGEN <= x < self.TAMANO_CASILLA * 8 + self.MARGEN:
            tablero = 1
            columna = (x - self.MARGEN) // self.TAMANO_CASILLA
        elif self.TAMANO_CASILLA * 8 + self.MARGEN <= x < self.TAMANO_CASILLA * 16 + self.MARGEN:
            tablero = 2
            columna = (x - self.TAMANO_CASILLA * 8 - self.MARGEN) // self.TAMANO_CASILLA
        else:
            return None, None, None
        
        fila = (y - self.MARGEN - self.ENCABEZADO) // self.TAMANO_CASILLA
        return tablero, fila, columna

    def manejar_click(self):
        pos_mouse = pygame.mouse.get_pos()
        x, y = pos_mouse
        tablero, fila, columna = self.obtener_casilla_desde_mouse(pos_mouse)
        
        # Si está fuera del tablero, ignorar el click
        if tablero is None or not (0 <= fila < 8 and 0 <= columna < 8):
            # Verificar si se hizo clic en el botón de menú
            if self.ANCHO - self.boton_menu.get_width() - 10 <= x <= self.ANCHO - 10 and 10 <= y <= 10 + self.boton_menu.get_height():   
                pygame.mixer.Sound("sonidos/apuntarBoton.wav").play()
                menu.menu_configuracion(self)
                return
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
                self.moverFicha_Sound.play()
                self.ultimo_movimiento = (self.tablero_seleccionado, (desde_fila, desde_col), (fila, columna))
                pieza_capturada = self.tablero.obtener_pieza(tablero, fila, columna)
                if pieza_capturada:
                    if pieza_capturada[1] == Color.BLANCO:
                        self.piezas_capturadas_blancas.append(pieza_capturada)
                    else:
                        self.piezas_capturadas_negras.append(pieza_capturada)
                self.tablero.realizar_movimiento((
                    self.tablero_seleccionado,
                    (desde_fila, desde_col),
                    (fila, columna)
                ))
                self.turno_actual = Color.NEGRO if self.turno_actual == Color.BLANCO else Color.BLANCO
            
            self.pieza_seleccionada = None
            self.tablero_seleccionado = None
            self.movimientos_validos = []
            
        
        self.dibujar_tablero()
        self.dibujar_piezas()
        pygame.display.flip()

        # Después de realizar el movimiento del jugador
        if self.turno_actual == self.maquina.color:
            # Hacer que la IA realice su movimiento
            movimiento_ia = self.maquina.obtener_mejor_movimiento(self.tablero)
            if movimiento_ia:
                pieza_capturada = self.tablero.obtener_pieza(movimiento_ia[0], movimiento_ia[2][0], movimiento_ia[2][1])
                if pieza_capturada:
                    if pieza_capturada[1] == Color.BLANCO:
                        self.piezas_capturadas_blancas.append(pieza_capturada)
                    else:
                        self.piezas_capturadas_negras.append(pieza_capturada)
                self.tablero.realizar_movimiento(movimiento_ia)
                self.ultimo_movimiento = movimiento_ia
                self.moverFicha_Sound.play()
                self.turno_actual = Color.BLANCO if self.maquina.color == Color.NEGRO else Color.NEGRO



    def dibujar_piezas(self):
        # Dibujar piezas en tablero 1
        for fila in range(8):
            for columna in range(8):
                pieza = self.tablero.tablero1[fila][columna]
                if pieza:  # Si hay una pieza en esta posición
                    imagen = self.imagenes.get(pieza)  # Obtener la imagen correspondiente
                    if imagen:
                        self.pantalla.blit(imagen,
                                         (columna * self.TAMANO_CASILLA + self.MARGEN,
                                          fila * self.TAMANO_CASILLA + self.MARGEN + self.ENCABEZADO))
                      
        # Dibujar piezas en tablero 2
        for fila in range(8):
            for columna in range(8):
                pieza = self.tablero.tablero2[fila][columna]
                if pieza:  # Si hay una pieza en esta posición
                    imagen = self.imagenes.get(pieza)  # Obtener la imagen correspondiente
                    if imagen:
                        self.pantalla.blit(imagen,
                                         ((columna + 8) * self.TAMANO_CASILLA + self.MARGEN,
                                          fila * self.TAMANO_CASILLA + self.MARGEN + self.ENCABEZADO))

        # Dibujar piezas capturadas
        x_blancas = self.MARGEN
        x_negras = self.ANCHO - self.MARGEN - self.TAMANO_CASILLA
        y_piezas_capturadas_blancas = self.ALTO - self.PIEZAS_CAPTURADAS + 40
        y_piezas_capturadas_negras = self.ALTO - self.PIEZAS_CAPTURADAS + 40

        for i, pieza in enumerate(self.piezas_capturadas_blancas):
            imagen = self.imagenes.get(pieza)
            if imagen:
                self.pantalla.blit(imagen, (x_blancas, y_piezas_capturadas_blancas))
                x_blancas += self.TAMANO_CASILLA
                if (i + 1) % 8 == 0:
                    x_blancas = self.MARGEN
                    y_piezas_capturadas_blancas += self.TAMANO_CASILLA

        for i, pieza in enumerate(self.piezas_capturadas_negras):
            imagen = self.imagenes.get(pieza)
            if imagen:
                self.pantalla.blit(imagen, (x_negras, y_piezas_capturadas_negras))
                x_negras -= self.TAMANO_CASILLA
                if (i + 1) % 8 == 0:
                    x_negras = self.ANCHO - self.MARGEN - self.TAMANO_CASILLA
                    y_piezas_capturadas_negras += self.TAMANO_CASILLA

    def mostrar_confirmacion(self):
        # Crear una superficie para el cuadro de diologuiito
        dialogo_ancho = 600
        dialogo_alto = 200
        dialogo = pygame.Surface((dialogo_ancho, dialogo_alto))
        dialogo.set_alpha(200)
        dialogo.fill((0, 0, 0))
    
        
        font = pygame.font.Font(None, 36)
        texto = font.render("¿Seguro que quieres volver al menú?", True, (255, 255, 255))
        texto_rect = texto.get_rect(center=(dialogo_ancho // 2, 50))
        dialogo.blit(texto, texto_rect)
    
        # Crear botones
        boton_ancho = 80
        boton_alto = 40
        boton_si = pygame.Rect(dialogo_ancho // 4 - boton_ancho // 2, 120, boton_ancho, boton_alto)
        boton_no = pygame.Rect(3 * dialogo_ancho // 4 - boton_ancho // 2, 120, boton_ancho, boton_alto)
        pygame.draw.rect(dialogo, (0, 255, 0), boton_si)
        pygame.draw.rect(dialogo, (255, 0, 0), boton_no)
        texto_si = font.render("Sí", True, (0, 0, 0))
        texto_no = font.render("No", True, (0, 0, 0))
        dialogo.blit(texto_si, texto_si.get_rect(center=boton_si.center))
        dialogo.blit(texto_no, texto_no.get_rect(center=boton_no.center))
    
        # Centrar el cuadrito de diálogo
        dialogo_x = self.ANCHO // 2 - dialogo_ancho // 2
        dialogo_y = self.ALTO // 2 - dialogo_alto // 2
        self.pantalla.blit(dialogo, (dialogo_x, dialogo_y))
        pygame.display.flip()
    
    
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    clic_x, clic_y = evento.pos
                    # Ajustar las coordenadas del clic para la posición del cuadro de diálogo,tocó hacerlo
                    clic_x -= dialogo_x
                    clic_y -= dialogo_y
                    if boton_si.collidepoint((clic_x, clic_y)):
                        pygame.mixer.Sound("sonidos/apuntarBoton.wav").play()
                        menu.main_menu()
                        return
                    elif boton_no.collidepoint((clic_x, clic_y)):
                        pygame.mixer.Sound("sonidos/apuntarBoton.wav").play()
                        pygame.mixer.music.unpause()
                        return
    
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
            self.dibujar_piezas()
            pygame.display.flip()