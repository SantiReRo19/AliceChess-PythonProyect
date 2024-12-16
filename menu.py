import pygame
import sys
from juego import Juego, Color

def piece_selection_menu(screen_width=800, screen_height=600):
    # Inicializar pygame
    pygame.init()

    # Configurar pantalla de selección de piezas
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Selección de Piezas - Alice Chess")

    # Cargar fondo
    background_image = pygame.image.load("imagenes/fondoMenu.png")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Colores
    wood_color = (82, 47, 35)
    hover_color = (210, 135, 50)
    white = (255, 255, 255)

    # Fuentes
    font_title = pygame.font.Font(pygame.font.match_font('timesnewroman'), 40)
    font_button = pygame.font.Font(pygame.font.match_font('timesnewroman'), 20)

    # Cargar imágenes de piezas (asegúrate de tener estas imágenes)
    piece_images = {
        'blancas': pygame.image.load("imagenes/piezas_blancas.png"),
        'negras': pygame.image.load("imagenes/piezas_negras.png")
    }

    # Dimensiones de los rectángulos
    rect_width, rect_height = 280, 200

    # Crear rectángulos para selección
    blancas_rect = pygame.Rect(100, 280, rect_width, rect_height)
    negras_rect = pygame.Rect(400, 280, rect_width, rect_height)

    # Escalar imágenes de piezas manteniendo relación de aspecto
    for key in piece_images:
        img = piece_images[key]
        img_width, img_height = img.get_width(), img.get_height()

        # Calcular factor de escala
        scale_factor = min(rect_width / img_width, rect_height / img_height)
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)

        # Escalar la imagen
        piece_images[key] = pygame.transform.scale(img, (new_width, new_height))

    # Variables para seguimiento de estado
    blancas_hovered = False
    negras_hovered = False
    player_color = None

    while True:
        screen.blit(background_image, (0, 0))

        # Título
        title_text = font_title.render("Elige tus Piezas", True, white)
        title_rect = title_text.get_rect(center=(screen_width // 2, 100))
        screen.blit(title_text, title_rect)

        # Obtener posición del mouse
        mouse_pos = pygame.mouse.get_pos()

        # Verificar hover
        blancas_hovered = blancas_rect.collidepoint(mouse_pos)
        negras_hovered = negras_rect.collidepoint(mouse_pos)

        # Dibujar rectángulos de selección
        color_blancas = hover_color if blancas_hovered else wood_color
        color_negras = hover_color if negras_hovered else wood_color

        pygame.draw.rect(screen, color_blancas, blancas_rect)
        pygame.draw.rect(screen, color_negras, negras_rect)

        # Dibujar imágenes de piezas centradas en los rectángulos
        for key, rect in zip(['blancas', 'negras'], [blancas_rect, negras_rect]):
            img = piece_images[key]
            img_width, img_height = img.get_width(), img.get_height()

            # Calcular posición centrada
            offset_x = rect.x + (rect_width - img_width) // 2
            offset_y = rect.y + (rect_height - img_height) // 2

            # Dibujar imagen
            screen.blit(img, (offset_x, offset_y))

        # Etiquetas
        blancas_label = font_button.render("Piezas Blancas", True, white)
        negras_label = font_button.render("Piezas Negras", True, white)
        
        screen.blit(blancas_label, (200, 250))
        screen.blit(negras_label, (500, 250))

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if blancas_rect.collidepoint(event.pos):
                    player_color = 'blancas'
                    break
                elif negras_rect.collidepoint(event.pos):
                    player_color = 'negras'
                    break

        # Salir del bucle si se seleccionó un color
        if player_color:
            break

        pygame.display.flip()

    # Iniciar juego con el color seleccionado
    if player_color:
        juego = Juego(player_color=Color.BLANCO if player_color == 'blancas' else Color.NEGRO)
        juego.ejecutar()


def main_menu():
    # Inicializar pygame
    pygame.init()

    # Inicializar sonido
    pygame.mixer.init()

    pygame.mixer.music.load("sonidos/menuInicio.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1)

    hover_sound = pygame.mixer.Sound("sonidos/apuntarBoton.wav")
    hover_sound.set_volume(0.5)
    play_sound = pygame.mixer.Sound("sonidos/iniciar.wav")  

    # Configurar pantalla
    dialogo_width, dialogo_height = 800, 600
    dialogo = pygame.display.set_mode((dialogo_width, dialogo_height))
    pygame.display.set_caption("Alice Chess")

    # Cargar fondo
    background_image = pygame.image.load("imagenes/fondoMenu.png")
    background_image = pygame.transform.scale(background_image, (dialogo_width, dialogo_height))

    # Colores y fuentes
    wood_color = (82, 47, 35)
    hover_color = (210, 135, 50)
    click_color = (150, 75, 20)
    white = (255, 255, 255)
    font_title = pygame.font.Font(pygame.font.match_font('timesnewroman'), 80)
    font_button = pygame.font.Font(pygame.font.match_font('timesnewroman'), 20)

    # Crear texto del título
    title_text = font_title.render("Alice Chess", True, white)
    title_rect = title_text.get_rect(center=(dialogo_width // 2, 150))

    # Crear texto de subtitulo con el nombre del equipo mas perron
    subtitle_text = font_button.render("By JLLS Team", True, white)
    subtitle_rect = subtitle_text.get_rect(center=(dialogo_width // 2, 200))

    # Crear botones
    button_width, button_height = 200, 50

    play_button_rect = pygame.Rect((dialogo_width // 2 - button_width // 2, 300), (button_width, button_height))
    quit_button_rect = pygame.Rect((dialogo_width // 2 - button_width // 2, 400), (button_width, button_height))

    # Estado para controlar el sonido al pasar por los botones
    play_hovered = False
    quit_hovered = False

    # Función para renderizar botones
    def render_button(text, rect, is_hovered=False):
        color = hover_color if is_hovered else wood_color
        pygame.draw.rect(dialogo, color, rect)
        button_text = font_button.render(text, True, white)
        button_text_rect = button_text.get_rect(center=rect.center)
        dialogo.blit(button_text, button_text_rect)

    while True:
        dialogo.blit(background_image, (0, 0))
        dialogo.blit(title_text, title_rect)
        dialogo.blit(subtitle_text, subtitle_rect)

        mouse_pos = pygame.mouse.get_pos()

        # Revisar si el cursor está sobre los botones
        is_play_hovered = play_button_rect.collidepoint(mouse_pos)
        is_quit_hovered = quit_button_rect.collidepoint(mouse_pos)

        if is_play_hovered and not play_hovered:
            hover_sound.play()
        if is_quit_hovered and not quit_hovered:
            hover_sound.play()

        # Actualizar el estado de los botones
        play_hovered = is_play_hovered
        quit_hovered = is_quit_hovered

        render_button("Jugar", play_button_rect, is_hovered=play_hovered)
        render_button("Salir", quit_button_rect, is_hovered=quit_hovered)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(event.pos):
                    play_sound.play()
                    """ juego = Juego()
                    juego.ejecutar() """
                    piece_selection_menu()
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

def menu_configuracion(juego):

    dialogo_ancho = int(800 * juego.modificador_tamano)
    dialogo_alto = int(600 * juego.modificador_tamano)

    # Crear una superficie semitransparente para el fondo
    fondo_transparente = pygame.Surface((juego.ANCHO, juego.ALTO))
    fondo_transparente.set_alpha(200)
    fondo_transparente.fill((0, 0, 0))

    # Cargar fuentes y colores
    fuente_titulo = pygame.font.Font(pygame.font.match_font('timesnewroman'), int(50 * juego.modificador_tamano))
    fuente_subtitulo = pygame.font.Font(pygame.font.match_font('timesnewroman'), int(30 * juego.modificador_tamano))
    fuente_texto = pygame.font.Font(pygame.font.match_font('timesnewroman'), int(20 * juego.modificador_tamano))

    blanco = (255, 255, 255)
    gris = (200, 200, 200)
    negro = (0, 0, 0)
    color_resaltado = (210, 135, 50)

    # Centrar el cuadro de diálogo
    dialogo_x = juego.ANCHO // 2 - dialogo_ancho // 2
    dialogo_y = juego.ALTO // 2 - dialogo_alto // 2

    # Encabezados
    texto_titulo = fuente_titulo.render("Configuración", True, blanco)
    rectangulo_titulo = texto_titulo.get_rect(center=(juego.ANCHO // 2, dialogo_y + 50))

    texto_resolucion = fuente_subtitulo.render("Resolución", True, blanco)
    rectangulo_resolucion = texto_resolucion.get_rect(topleft=(dialogo_x + 100, dialogo_y + 120))

    texto_musica = fuente_subtitulo.render("Música", True, blanco)
    rectangulo_musica = texto_musica.get_rect(topleft=(dialogo_x + 100, dialogo_y + 220))

    texto_volumen = fuente_subtitulo.render("Volumen", True, blanco)
    rectangulo_volumen = texto_volumen.get_rect(topleft=(dialogo_x + 100, dialogo_y + 320))

    # Botones de resolución
    resoluciones = ["Grande", "Mediano", "Pequeño"]
    botones_resolucion = []
    for i, res in enumerate(resoluciones):
        rectangulo_boton = pygame.Rect(dialogo_x + 120 + i * 150, dialogo_y + 160, 140, 40)
        botones_resolucion.append((rectangulo_boton, res))

    # Botones de música
    canciones = ["Cancion 1", "Cancion 2", "Cancion 3"]
    botones_musica = []
    for i, cancion in enumerate(canciones):
        rectangulo_boton = pygame.Rect(dialogo_x + 120 + i * 150, dialogo_y + 260, 140, 40)
        botones_musica.append((rectangulo_boton, cancion))

    # Barra deslizante de volumen
    barra_volumen = pygame.Rect(dialogo_x + 120, dialogo_y + 360, 400, int(20 * juego.modificador_tamano))
    # Volumen inicial
    volumen = juego.configuracion["volumen"]
    controlador_volumen = pygame.Rect(dialogo_x + 120 + volumen * barra_volumen.width, dialogo_y + 360, 20, int(20 * juego.modificador_tamano))

    # Botón de volver
    rectangulo_boton_volver = pygame.Rect(juego.ANCHO // 2 - 75, dialogo_y + 500, 150, int(50 * juego.modificador_tamano))

    # Botón de cerrar (X)
    rectangulo_boton_cerrar = pygame.Rect(dialogo_x + dialogo_ancho - 40, dialogo_y + 10, 30, int(30 * juego.modificador_tamano))

    

    corriendo = True

    # Dibujar fondo semitransparente
    juego.pantalla.blit(fondo_transparente, (0, 0))
    # Dibujar encabezados
    juego.pantalla.blit(texto_titulo, rectangulo_titulo)
    juego.pantalla.blit(texto_resolucion, rectangulo_resolucion)
    juego.pantalla.blit(texto_musica, rectangulo_musica)
    juego.pantalla.blit(texto_volumen, rectangulo_volumen)

    while corriendo:

        # Dibujar botones de resolución
        for rectangulo_boton, res in botones_resolucion:
            color = color_resaltado if rectangulo_boton.collidepoint(pygame.mouse.get_pos()) else gris
            pygame.draw.rect(juego.pantalla, color, rectangulo_boton)
            texto = fuente_texto.render(res, True, negro)
            rectangulo_texto = texto.get_rect(center=rectangulo_boton.center)
            juego.pantalla.blit(texto, rectangulo_texto)

        # Dibujar botones de música
        for rectangulo_boton, cancion in botones_musica:
            color = color_resaltado if rectangulo_boton.collidepoint(pygame.mouse.get_pos()) else gris
            pygame.draw.rect(juego.pantalla, color, rectangulo_boton)
            texto = fuente_texto.render(cancion, True, negro)
            rectangulo_texto = texto.get_rect(center=rectangulo_boton.center)
            juego.pantalla.blit(texto, rectangulo_texto)

        # Dibujar barra de volumen
        pygame.draw.rect(juego.pantalla, blanco, barra_volumen)
        pygame.draw.rect(juego.pantalla, color_resaltado, controlador_volumen)

        # Dibujar botón de volver al menu principal
        color_volver = color_resaltado if rectangulo_boton_volver.collidepoint(pygame.mouse.get_pos()) else gris
        pygame.draw.rect(juego.pantalla, color_volver, rectangulo_boton_volver)
        texto_volver = fuente_texto.render("Salir", True, negro)
        rectangulo_texto_volver = texto_volver.get_rect(center=rectangulo_boton_volver.center)
        juego.pantalla.blit(texto_volver, rectangulo_texto_volver)

        # Dibujar botón de cerrar el menu
        color_cerrar = color_resaltado if rectangulo_boton_cerrar.collidepoint(pygame.mouse.get_pos()) else gris
        pygame.draw.rect(juego.pantalla, color_cerrar, rectangulo_boton_cerrar)
        texto_cerrar = fuente_texto.render("X", True, negro)
        rectangulo_texto_cerrar = texto_cerrar.get_rect(center=rectangulo_boton_cerrar.center)
        juego.pantalla.blit(texto_cerrar, rectangulo_texto_cerrar)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                guardar_configuracion(juego.configuracion)
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clic izquierdo
                    if rectangulo_boton_volver.collidepoint(evento.pos):
                        guardar_configuracion(juego.configuracion)
                        main_menu()

                    if rectangulo_boton_cerrar.collidepoint(evento.pos):
                        guardar_configuracion(juego.configuracion)
                        corriendo = False
                        
                    for rectangulo_boton, res in botones_resolucion:
                        if rectangulo_boton.collidepoint(evento.pos):
                            pygame.mixer.Sound("sonidos/apuntarBoton.wav").play()

                            if res == "Grande":
                                res = 1
                            elif res == "Mediano":
                                res = 0.8
                            elif res == "Pequeño":
                                res = 0.6 

                            juego.configuracion["tamano"] = res
                            print(f"Resolución seleccionada: {res}")

                    for rectangulo_boton, cancion in botones_musica:
                        if rectangulo_boton.collidepoint(evento.pos):
                            pygame.mixer.Sound("sonidos/apuntarBoton.wav").play()
                            print(f"Canción seleccionada: {cancion}")
                            if cancion == "Cancion 1":
                                ruta_cancion = "sonidos/menu.mp3"
                                pygame.mixer.music.load("sonidos/menu.mp3")
                                pygame.mixer.music.play(loops=-1)
                            elif cancion == "Cancion 2":
                                ruta_cancion = "sonidos/menu2.mp3"
                                pygame.mixer.music.load("sonidos/menu2.mp3")
                                pygame.mixer.music.set_volume(0.8)
                                pygame.mixer.music.play(loops=-1)
                            elif cancion == "Cancion 3":
                                ruta_cancion = "sonidos/menu3.mp3"
                                pygame.mixer.music.load("sonidos/menu3.mp3")
                                pygame.mixer.music.play(loops=-1)
                            juego.configuracion["cancion"] = ruta_cancion

            if evento.type == pygame.MOUSEMOTION:
                # Mover el handle de la barra de volumen
                if evento.buttons[0] == 1 and barra_volumen.collidepoint(evento.pos):
                    controlador_volumen.centerx = max(min(evento.pos[0], barra_volumen.right), barra_volumen.left)
                    volumen = (controlador_volumen.centerx - barra_volumen.left) / barra_volumen.width
                    juego.configuracion["volumen"] = volumen
                    pygame.mixer.music.set_volume(volumen)


CONFIG_FILE = "config.json"

def cargar_configuracion():
    try:
        with open(CONFIG_FILE, 'r') as archivo:
            configuracion = json.load(archivo)
        return configuracion
    except FileNotFoundError:
        return {
            "tamano": 0.8,
            "volumen": 0.5,
            "cancion": "sonidos/menu.mp3"
        }

def guardar_configuracion(configuracion):
    with open(CONFIG_FILE, 'w') as archivo:
        json.dump(configuracion, archivo, indent=4)
    

    
                    
