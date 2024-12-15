import pygame
import sys
from juego import Juego

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
                    juego = Juego()
                    juego.ejecutar()
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

