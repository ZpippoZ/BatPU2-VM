import multiprocessing
from multiprocessing import shared_memory
from time import perf_counter


def gui(running, lock, pc):
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
    font_debug = pygame.font.SysFont('RobotoMono-Regular', 20)

    background_color = "#1D2229"
    background_rect_color = "#252B34"
    controls_color = "#1B1D1F"
    controls_hover_color = "#2E3033"
    controls_pressed_color = "#0C0E10"
    lamp_type_color = "#25272D"
    lamp_type_hover_color = "#363D4A"
    lamp_type_pressed_color = "#16181E"

    width = 0
    background_rects_radius = 7
    inside_rects_radius = 3
    rectangles = {
        "char_display_rect": (background_rect_color, pygame.Rect(10, 10, 250, 125), width, background_rects_radius),
        "number_display_rect": (background_rect_color, pygame.Rect(270, 10, 140, 125), width, background_rects_radius),
        "lamp_display_rect": (background_rect_color, pygame.Rect(10, 145, 400, 440), width, background_rects_radius),
        "display_type_rect": (lamp_type_hover_color, pygame.Rect(18, 547, 384, 30), width, inside_rects_radius),
        "lamp1x1_type_rect": (lamp_type_color, pygame.Rect(148, 549, 78, 26), width, inside_rects_radius),
        "lamp2x2_type_rect": (lamp_type_color, pygame.Rect(228, 549, 80, 26), width, inside_rects_radius),
        "lampflat_type_rect": (lamp_type_color, pygame.Rect(310, 549, 90, 26), width, inside_rects_radius),
        "inputs_rect": (background_rect_color, pygame.Rect(10, 595, 400, 150), width, background_rects_radius),
        "credits1_rect": (background_color, pygame.Rect(10, 0, 400, 0), width, background_rects_radius),
        "credits2_rect": (background_color, pygame.Rect(10, 0, 400, 0), width, background_rects_radius),
        "program_counter_rect": (background_rect_color, pygame.Rect(420, 10, 400, 50), width, background_rects_radius),
        "pc_rect": (background_rect_color, pygame.Rect(450, 10, 0, 0), width, background_rects_radius),
        "started_rect": (controls_color, pygame.Rect(420, 70, 400, 50), width, inside_rects_radius),
        "step_rect": (controls_color, pygame.Rect(420, 130, 195, 50), width, inside_rects_radius),
        "paused_rect": (controls_color, pygame.Rect(625, 130, 195, 50), width, inside_rects_radius),
        "execution_rate_rect": (background_rect_color, pygame.Rect(420, 190, 400, 130), width, background_rects_radius),
        "instructions_second_rect": (background_rect_color, pygame.Rect(420, 260, 400, 0), width, background_rects_radius),
        "flags_rect": (background_rect_color, pygame.Rect(420, 330, 400, 60), width, background_rects_radius),
        "registers_rect": (background_rect_color, pygame.Rect(420, 400, 400, 140), width, background_rects_radius),
        "ram_rect": (background_rect_color, pygame.Rect(420, 550, 400, 180), width, background_rects_radius),
        "settings_rect": (background_rect_color, pygame.Rect(420, 740, 400, 60), width, background_rects_radius),
        "editor_rect": (background_rect_color, pygame.Rect(830, 10, 600, 790), width, background_rects_radius),
        "editor_fle_name_rect": (controls_color, pygame.Rect(840, 20, 580, 30), width, inside_rects_radius),
        "editor_code_rect": (controls_color, pygame.Rect(840, 55, 580, 735), width, inside_rects_radius),
        "white_border_rect": ("white", pygame.Rect(0, 0, 0, 0), 1, inside_rects_radius)
    }

    hoverable_rects = {
        "started_rect": (controls_color, controls_hover_color, controls_pressed_color),
        "step_rect": (controls_color, controls_hover_color, controls_pressed_color),
        "paused_rect": (controls_color, controls_hover_color, controls_pressed_color),
        "lamp1x1_type_rect": (lamp_type_color, lamp_type_hover_color, lamp_type_pressed_color),
        "lamp2x2_type_rect": (lamp_type_color, lamp_type_hover_color, lamp_type_pressed_color),
        "lampflat_type_rect": (lamp_type_color, lamp_type_hover_color, lamp_type_pressed_color)
    }

    number = 0
    number_str = str(number)

    started = False
    paused = False

    text_color = "white"
    text_color_gray = "#6F7580"

    text_surfaces = {
        "number_display_surface": font_number_display.render(str(number), True, text_color, background_rect_color),
        "display_type_surface": font_lamp_type.render("Display type: 1x1 Lamp 2x2 Lamp Flat Lamp", True, text_color, None),
        "credits1_surface": font_credits.render("BatPU2 Virtual Machine", True, text_color, background_color),
        "credits2_surface": font_credits.render("By zPippo", True, text_color, background_color),
        "program_counter_surface": font_controls.render("Program Counter:", True, text_color, background_rect_color),
        "pc_surface": font_controls.render(str(pc[0]), True, text_color, background_rect_color),
        "started_surface": font_controls.render("-Start-", True, text_color, None),
        "step_surface": font_controls.render("<Step>", True, text_color, None),
        "paused_surface": font_controls.render("|Pause|", True, text_color, None),
        "execution_rate_surface": font_debug.render("Execution Rate:", True, text_color, background_rect_color),
        "instructions_second_surface": font_debug.render("(Instructions Per Second)", True, text_color, background_rect_color),
        "flags_surface": font_debug.render("Flags", True, text_color, background_rect_color),
        "registers_surface": font_debug.render("Registers", True, text_color, background_rect_color),
        "ram_surface": font_debug.render("RAM (Address:Value)", True, text_color, background_rect_color),
        "settings_surface": font_debug.render("Settings (soon™)", True, text_color, background_rect_color)
    }

    text_positions = {
        "number_display": (-1, -1, 0, 0),
        "display_type": (25, -1, 0, 0),
        "credits1": (-1, 755, 0, 0),
        "credits2": (-1, 780, 0, 0),
        "program_counter": (-1, -1, -50, -2),
        "pc": (-1, -1, 0, 0),
        "started": (-1, -1, 0, -2),
        "step": (-1, -1, 0, -2),
        "paused": (-1, -1, 0, -2),
        "execution_rate": (-1, -1, 0, -47),
        "instructions_second": (-1, -1, 0, 0),
        "flags": (-1, -1, 0, -15),
        "registers": (-1, -1, 0, -50),
        "ram": (-1, -1, 0, -70),
        "settings": (-1, -1, 0, -15)
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

        mouse_pressed = False
        mouse_released = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running.set()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_released = True

        screen.fill(background_color)

        #with lock:
            #print(pc)
        text_surfaces["pc"] = font_controls.render(str(pc), True, text_color, background_rect_color)
        text_surfaces["started_surface"] = font_controls.render("-Start-", True, text_color, None) if not started\
            else font_controls.render("-Stop-", True, text_color, None)
        text_surfaces["paused_surface"] = font_controls.render("|Pause|", True, text_color, None) if not paused\
            else font_controls.render("|Resume|", True, text_color, None)

        for rectangle in rectangles:
            pygame.draw.rect(
                screen,
                rectangles[rectangle][0],
                rectangles[rectangle][1],
                width=rectangles[rectangle][2],
                border_radius=rectangles[rectangle][3]
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

        rectangles["white_border_rect"] = ("white", pygame.Rect(0, 0, 0, 0), 1, inside_rects_radius)

        for hoverable_rect in hoverable_rects:
            if rectangles[hoverable_rect][1][0] < mouse_pos[0] < rectangles[hoverable_rect][1][0] + rectangles[hoverable_rect][1][2] and\
               rectangles[hoverable_rect][1][1] < mouse_pos[1] < rectangles[hoverable_rect][1][1] + rectangles[hoverable_rect][1][3]:
                rectangles[hoverable_rect] = (hoverable_rects[hoverable_rect][1],
                                              rectangles[hoverable_rect][1],
                                              rectangles[hoverable_rect][2],
                                              rectangles[hoverable_rect][3])
                if mouse_pressed and pygame.mouse.get_pressed()[0]:
                    pressed_button = hoverable_rect
                    match pressed_button[:-5]:
                        case "started":
                            started = not started
                            break
                        case "paused":
                            paused = not paused
                            break
                        case "lamp1x1_type":
                            lamp_type = lamp_off
                            break
                        case "lamp2x2_type":
                            lamp_type = lamp_off_double
                            break
                        case "lampflat_type":
                            lamp_type = lamp_off_flat
                            break
                if pygame.mouse.get_pressed()[0] and pressed_button == hoverable_rect:
                    rectangles[hoverable_rect] = (hoverable_rects[hoverable_rect][2],
                                                  rectangles[hoverable_rect][1],
                                                  rectangles[hoverable_rect][2],
                                                  rectangles[hoverable_rect][3])
                    rectangles["white_border_rect"] = ("white", rectangles[hoverable_rect][1], 1, inside_rects_radius)

            else:
                rectangles[hoverable_rect] = (hoverable_rects[hoverable_rect][0],
                                              rectangles[hoverable_rect][1],
                                              rectangles[hoverable_rect][2],
                                              rectangles[hoverable_rect][3])

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def vm(running, lock, pc):
    flags = shared_memory.SharedMemory(create=True, size=2)
    registers = shared_memory.SharedMemory(create=True, size=16)
    ram = shared_memory.SharedMemory(create=True, size=256)

    stack = []
    flags_buf = flags.buf
    regs_buf = registers.buf
    ram_buf = ram.buf

    with open("programs/test.mc", 'r') as file:
        lines = file.read().split()
        lines = [int(line, 2) for line in lines]

    cycles = 0
    start_time = perf_counter()
    min_time = [1]
    max_time = [0]
    
    opcodes = [
        "nop",
        "hlt",
        "add",
        "sub",
        "nor",
        "and",
        "xor",
        "rsh",
        "ldi",
        "adi",
        "jmp",
        "brh",
        "cal",
        "ret",
        "lod",
        "str"
    ]

    while not running.is_set():
        time = perf_counter()
        regs_buf[0] = 0

        instruction = lines[pc[0]]

        opcode = instruction >> 12
        regA = instruction >> 8 & 15
        regB = instruction >> 4 & 15
        regDest = instruction & 15
        immediate = instruction & 255
        condition = instruction >> 10 & 3
        address = instruction & 1023
        ram_offset = instruction & 15
        ram_offset -= 16 if ram_offset & 8 else ram_offset

        pc[0] += 1
        cycles += 1
        #with lock:
            #print(regs_buf[3])

        match opcode:
            case 1:
                break
            case 2:
                result = regs_buf[regA] + regs_buf[regB]
                regs_buf[regDest] = result & 255
                flags_buf[0] = result > 255
                flags_buf[1] = not regs_buf[regDest]
            case 3:
                result = regs_buf[regA] - regs_buf[regB]
                flags_buf[0] = regs_buf[regA] >= regs_buf[regB]
                regs_buf[regDest] = result & 255
                flags_buf[1] = not regs_buf[regDest]
            case 4:
                result = 0b11111111 ^ (regs_buf[regA] | regs_buf[regB])
                regs_buf[regDest] = result
                flags_buf[1] = not regs_buf[regDest]
            case 5:
                result = regs_buf[regA] & regs_buf[regB]
                regs_buf[regDest] = result
                flags_buf[1] = not regs_buf[regDest]
            case 6:
                result = regs_buf[regA] ^ regs_buf[regB]
                regs_buf[regDest] = result
                flags_buf[1] = not regs_buf[regDest]
            case 7:
                regs_buf[regDest] = regs_buf[regA] >> 1
            case 8:
                regs_buf[regDest] = immediate
            case 9:
                result = regs_buf[regDest] + immediate
                regs_buf[regDest] = result & 255
                flags_buf[0] = result > 255
                flags_buf[1] = not regs_buf[regDest]
            case 10:
                pc[0] = address
            case 11:
                match condition:
                    case 0:
                        pc[0] = address if flags_buf[1] else pc[0]
                    case 1:
                        pc[0] = address if not flags_buf[1] else pc[0]
                    case 2:
                        pc[0] = address if flags_buf[0] else pc[0]
                    case 3:
                        pc[0] = address if not flags_buf[0] else pc[0]
            case 12:
                stack.insert(0, pc[0])
                pc[0] = address
            case 13:
                pc[0] = stack.pop(0)
            case 14:
                regs_buf[regB] = ram_buf[regA + ram_offset]
            case 15:
                ram_buf[regA + ram_offset] = regB

        min_time = [perf_counter() - time, opcodes[opcode]] if perf_counter() - time < min_time[0] else min_time
        max_time = [perf_counter() - time, opcodes[opcode]] if perf_counter() - time > max_time[0] else max_time


    end_time = perf_counter()

    flags.close()
    registers.close()
    ram.close()
    
    time = end_time - start_time
    print(f"\n{cycles} cycles executed")
    print(f"The program ran for {round(time, 3)} seconds")
    print(f"\nAverage instruction time: {time / cycles:.9f} seconds")
    print(f"\nFastest instruction time: {min_time[0]:.9f} seconds, opcode: {min_time[1]}")
    print(f"Slowest instruction time: {max_time[0]:.9f} seconds, opcode: {max_time[1]}")
    print(f"\nAverage instructions per second: {cycles / time:.9f}\n")


if __name__ == "__main__":
    running = multiprocessing.Event()
    lock = multiprocessing.Lock()
    pc = shared_memory.ShareableList([0])

    gui_process = multiprocessing.Process(target=gui, args=(running, lock, pc), name="BatPU2 GUI")

    gui_process.start()

    multiprocessing.current_process().name = "BatPU2 VM"
    vm(running, lock, pc)

    gui_process.join()
    gui_process.close()
