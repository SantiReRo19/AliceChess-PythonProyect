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

    pygame.mixer.music.load("sonidos/menu.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1)

    hover_sound = pygame.mixer.Sound("sonidos/apuntarBoton.wav")
    hover_sound.set_volume(0.5)
    play_sound = pygame.mixer.Sound("sonidos/iniciar.wav")  

    # Configurar pantalla
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Alice Chess")

    # Cargar fondo
    background_image = pygame.image.load("imagenes/fondoMenu.png")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Colores y fuentes
    wood_color = (82, 47, 35)
    hover_color = (210, 135, 50)
    click_color = (150, 75, 20)
    white = (255, 255, 255)
    font_title = pygame.font.Font(pygame.font.match_font('timesnewroman'), 80)
    font_button = pygame.font.Font(pygame.font.match_font('timesnewroman'), 20)

    # Crear texto del título
    title_text = font_title.render("Alice Chess", True, white)
    title_rect = title_text.get_rect(center=(screen_width // 2, 150))

    # Crear texto de subtitulo con el nombre del equipo mas perron
    subtitle_text = font_button.render("By JLLS Team", True, white)
    subtitle_rect = subtitle_text.get_rect(center=(screen_width // 2, 200))

    # Crear botones
    button_width, button_height = 200, 50

    play_button_rect = pygame.Rect((screen_width // 2 - button_width // 2, 300), (button_width, button_height))
    quit_button_rect = pygame.Rect((screen_width // 2 - button_width // 2, 400), (button_width, button_height))

    # Estado para controlar el sonido al pasar por los botones
    play_hovered = False
    quit_hovered = False

    # Función para renderizar botones
    def render_button(text, rect, is_hovered=False):
        color = hover_color if is_hovered else wood_color
        pygame.draw.rect(screen, color, rect)
        button_text = font_button.render(text, True, white)
        button_text_rect = button_text.get_rect(center=rect.center)
        screen.blit(button_text, button_text_rect)

    while True:
        screen.blit(background_image, (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(subtitle_text, subtitle_rect)

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

