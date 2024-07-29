import multiprocessing


def gui(running):
    import pygame

    WIDTH = 1440
    HEIGHT = 810

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("BatPU2 VM")

    clock = pygame.time.Clock()

    font_char_display = pygame.font.SysFont('RobotoMono-Regular', 30)
    font_number_display = pygame.font.SysFont('RobotoMono-Regular', 60)
    font_lamp_type = pygame.font.SysFont('RobotoMono-Regular', 15)
    font_credits = pygame.font.SysFont('RobotoMono-Regular', 17)
    font_controls = pygame.font.SysFont('RobotoMono-Regular', 25)
    font_debug = pygame.font.SysFont('Arial', 50)
    font_menu = pygame.font.SysFont('Arial', 50)

    background_color = "#1D2229"
    background_rect_color = "#252B34"
    controls_color = "#1B1D1F"
    controls_hover_color = "#2E3033"
    lamp_type_color = "#25272D"
    lamp_type_hover_color = "#363D4A"

    background_rects_radius = 7
    inside_rects_radius = 3
    rectangles = {
        "char_display_rect": (background_rect_color, pygame.Rect(10, 10, 250, 125), background_rects_radius),
        "number_display_rect": (background_rect_color, pygame.Rect(270, 10, 140, 125), background_rects_radius),
        "lamp_display_rect": (background_rect_color, pygame.Rect(10, 145, 400, 440), background_rects_radius),
        "display_type_rect": (lamp_type_hover_color, pygame.Rect(18, 547, 384, 30), inside_rects_radius),
        "lamp1x1_type_rect": (lamp_type_color, pygame.Rect(148, 549, 78, 26), inside_rects_radius),
        "lamp2x2_type_rect": (lamp_type_color, pygame.Rect(228, 549, 80, 26), inside_rects_radius),
        "lampflat_type_rect": (lamp_type_color, pygame.Rect(310, 549, 90, 26), inside_rects_radius),
        "inputs_rect": (background_rect_color, pygame.Rect(10, 595, 400, 150), background_rects_radius),
        "credits1_rect": (background_color, pygame.Rect(10, 0, 400, 0), background_rects_radius),
        "credits2_rect": (background_color, pygame.Rect(10, 0, 400, 0), background_rects_radius),
        "program_counter_rect": (background_rect_color, pygame.Rect(420, 10, 400, 50), background_rects_radius),
        "start_stop_rect": (controls_color, pygame.Rect(420, 70, 400, 50), inside_rects_radius),
        "step_rect": (controls_color, pygame.Rect(420, 130, 195, 50), inside_rects_radius),
        "pause_resume_rect": (controls_color, pygame.Rect(625, 130, 195, 50), inside_rects_radius),
        "execution_rate_rect": (background_rect_color, pygame.Rect(420, 190, 400, 110), background_rects_radius),
        "flags_rect": (background_rect_color, pygame.Rect(420, 310, 400, 60), background_rects_radius),
        "registers_rect": (background_rect_color, pygame.Rect(420, 380, 400, 160), background_rects_radius),
        "ram_rect": (background_rect_color, pygame.Rect(420, 550, 400, 180), background_rects_radius),
        "settings_rect": (background_rect_color, pygame.Rect(420, 740, 400, 60), background_rects_radius),
        "editor_rect": (background_rect_color, pygame.Rect(830, 10, 600, 790), background_rects_radius),
        "editor_fle_name_rect": (controls_color, pygame.Rect(840, 20, 580, 30), inside_rects_radius),
        "editor_code_rect": (controls_color, pygame.Rect(840, 55, 580, 735), inside_rects_radius)
    }

    hoverable_rects = {
        "start_stop_rect": (controls_color, controls_hover_color),
        "step_rect": (controls_color, controls_hover_color),
        "pause_resume_rect": (controls_color, controls_hover_color),
        "lamp1x1_type_rect": (lamp_type_color, lamp_type_hover_color),
        "lamp2x2_type_rect": (lamp_type_color, lamp_type_hover_color),
        "lampflat_type_rect": (lamp_type_color, lamp_type_hover_color)
    }

    number = 0
    number_str = str(number)

    start_stop = "-Start-"
    pause_resume = "|Pause|"

    text_color = "white"
    text_color_gray = "#6F7580"

    text_surfaces = {
        "number_display_surface": font_number_display.render(str(number), True, text_color),
        "display_type_surface": font_lamp_type.render("Display type: 1x1 Lamp 2x2 Lamp Flat Lamp", True, text_color),
        "credits1_surface": font_credits.render("BatPU2 Virtual Machine", True, text_color),
        "credits2_surface": font_credits.render("By zPippo", True, text_color),
        "program_counter_surface": font_controls.render("Program Counter:", True, text_color),
        "start_stop_surface": font_controls.render(start_stop, True, text_color),
        "step_surface": font_controls.render("<Step>", True, text_color),
        "pause_resume_surface": font_controls.render(pause_resume, True, text_color)
    }

    text_positions = {
        "number_display": (-1, -1, 0, 0),
        "display_type": (25, -1, 0, 0),
        "credits1": (-1, 755, 0, 0),
        "credits2": (-1, 780, 0, 0),
        "program_counter": (-1, -1, -50, -2),
        "start_stop": (-1, -1, 0, -2),
        "step": (-1, -1, 0, -2),
        "pause_resume": (-1, -1, 0, -2),
    }

    lamp_off = pygame.image.load("lamps/lamp_off.png").convert()
    lamp_on = pygame.image.load("lamps/lamp_on.png").convert()
    lamp_off_double = pygame.image.load("lamps/lamp_off_double.png").convert()
    lamp_on_double = pygame.image.load("lamps/lamp_on_double.png").convert()
    lamp_off_flat = pygame.image.load("lamps/lamp_off_flat.png").convert()
    lamp_on_flat = pygame.image.load("lamps/lamp_on_flat.png").convert()

    lamp_type = lamp_off

    buffer_lamps = [[False for x in range(32)] for y in range(32)]
    lamps = buffer_lamps

    buffer_chars = ['_' for _ in range(20)]
    chars = buffer_chars

    while not running.is_set():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running.set()

        screen.fill(background_color)

        for rectangle in rectangles:
            pygame.draw.rect(
                screen,
                rectangles[rectangle][0],
                rectangles[rectangle][1],
                width=0,
                border_radius=rectangles[rectangle][2]
            )

        for y in range(32):
            for x in range(32):
                screen.blit(lamp_type, (x * 12 + 18, y * 12 + 155))

        for x in range(10):
            char = font_char_display.render(chars[x], True, text_color)
            screen.blit(char, (24 * x + 18, 24))
            char = font_char_display.render(chars[x + 10], True, text_color)
            screen.blit(char, (24 * x + 18, 79))

        number_str = str(number)

        for text in text_positions:
            text_position = (rectangles[text + "_rect"][1].centerx - (text_surfaces[text + "_surface"].get_rect().right / 2) + text_positions[text][2]
                             if text_positions[text][0] == -1 else text_positions[text][0],

                             rectangles[text + "_rect"][1].centery - (text_surfaces[text + "_surface"].get_rect().bottom / 2) + text_positions[text][3]
                             if text_positions[text][1] == -1 else text_positions[text][1])

            screen.blit(text_surfaces[text + "_surface"], text_position)


        mouse_pos = pygame.mouse.get_pos()

        for hoverable_rect in hoverable_rects:
            if rectangles[hoverable_rect][1][0] < mouse_pos[0] < rectangles[hoverable_rect][1][0] + rectangles[hoverable_rect][1][2] and\
               rectangles[hoverable_rect][1][1] < mouse_pos[1] < rectangles[hoverable_rect][1][1] + rectangles[hoverable_rect][1][3]:
                rectangles[hoverable_rect] = (hoverable_rects[hoverable_rect][1], rectangles[hoverable_rect][1], rectangles[hoverable_rect][2])
            else:
                rectangles[hoverable_rect] = (hoverable_rects[hoverable_rect][0], rectangles[hoverable_rect][1], rectangles[hoverable_rect][2])

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def vm(running):
    while not running.is_set():
        ...


if __name__ == "__main__":
    running = multiprocessing.Event()

    gui_process = multiprocessing.Process(target=gui, args=(running,))
    vm_process = multiprocessing.Process(target=vm, args=(running,))

    gui_process.start()
    vm_process.start()

    gui_process.join()
    vm_process.join()
