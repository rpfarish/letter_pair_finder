"""letter pair optimal solver"""
import subprocess
import sys

from button import Button
from database import get_all, insert_pair

try:
    import pygame
except ModuleNotFoundError as e:
    print(e)
    version = input('What version of pygame do you want?: ')
    module = 'pygame' if version.startswith('1') else 'pygame==2.0.0.dev8'
    print('Installing Pygame', module)
    subprocess.call([sys.executable, "-m", "pip", "install", module])
    import pygame

pygame.font.init()
WIDTH, HEIGHT = 800, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"letter pair optimal solver")
pygame.display.set_icon(WIN)
FPS = 60
light_gray = (175, 175, 175)

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = True

    def handle_event(self, event):
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     # If the user clicked on the input_box rect.
        #     if self.rect.collidepoint(event.pos):
        #         # Toggle the active variable.
        #         self.active = not self.active
        #     else:
        #         self.active = False
        #     # Change the current color of the input box.
        #     self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                # TODO what this is so smart i didn't think to ever do this
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width


def main():
    """main handling function"""
    run = True
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("mscomicsans", 50)
    label = main_font.render(f"Label", True, (255, 255, 255))
    bfs_b = Button(WIN, light_gray, x=100, y=100, width=200, height=25, win_w=WIDTH,
                   win_h=HEIGHT, text="Insert/update pair in database", font_size=15, button_value="BFS")

    input_box1 = InputBox(x=100, y=100, w=140, h=32)
    input_boxes = [input_box1]
    user_label = FONT.render(input_box1.text, True, (255, 0, 0))

    def redraw_window():
        """redraws the entire display"""
        WIN.fill((0, 0, 0))
        # Put updating objects here
        WIN.blit(label, (10, 10))
        bfs_b.draw_resize(WIDTH, HEIGHT, -.05, .15)
        WIN.blit(user_label, ((WIDTH // 2) - user_label.get_width() // 2, HEIGHT // 2))
        pygame.display.update()

    while run:
        redraw_window()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        keys = pygame.key.get_pressed()
        click = pygame.mouse.get_pressed(num_buttons=3)
        mouse = pygame.mouse.get_pos()
        Button.update_all_buttons(mouse, click[0])
        user_label = FONT.render(input_box1.text, True, (255, 0, 0))

        if input_box1.text.count(',') == 1:
            a, b = input_box1.text.split(',')
            print(a, b)
            try:
                b = float(b)
            except ValueError:
                continue

            inserted = bfs_b.call_func(insert_pair, click[0] or keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER],
                                       'edges_cycle_averages', a, b)
            r = get_all('edges_cycle_averages')
            if r is not None and a in dict(r):
                label = main_font.render(f"'{input_box1.text}' is in the database!!", True, (255, 255, 255))
                # todo add to api,
            else:
                label = main_font.render(f"'{input_box1.text}' is not in the database!!", True, (255, 255, 255))

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

        if click[0]:
            pass

        elif click[1]:
            pass

        if mouse:
            pass


if __name__ == '__main__':
    main()
