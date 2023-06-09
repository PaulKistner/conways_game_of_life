import sys
import numpy as np
import pygame
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QFrame, QPushButton, QSlider, QLineEdit, QHBoxLayout, QVBoxLayout
from scipy.signal import convolve2d

########################################################################################################################
##  PROJEKT_K_SCHNELL -- MAIN
########################################################################################################################

class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 200, 400)
        self.setWindowTitle('Game of Life Steuerung')

        self.frame = QFrame(self)
        self.frame.setGeometry(10, 10, 400, 400)

        self.active = False
        self.rect_col, self.fill_col = pygame.Color('grey'), pygame.Color('white')
        self.screen_width, self.screen_height = 1000, 1000
        self.array_now = np.zeros((100, 100), dtype=int)
        self.square_size = int(self.screen_width / len(self.array_now))
        self.speed = 10
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Conways game of Life - Kiste Edition")

        self.pause_button = QPushButton('Start', self)
        self.pause_button.clicked.connect(self.on_pause_click)
        self.pause_button.setStyleSheet('''
            QPushButton {
                background-color: #50C878;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 30px;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #3CB371;
                color: white;
            }
        ''')
        self.left_button = QPushButton('◀', self)
        self.left_button.clicked.connect(self.on_left_click)
        self.left_button.setStyleSheet('''
            QPushButton {
                background-color: #F08080;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 30px;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #CD5C5C;
                color: white;
            }
        ''')
        self.right_button = QPushButton('▶', self)
        self.right_button.clicked.connect(self.on_right_click)
        self.right_button.setStyleSheet('''
            QPushButton {
                background-color: #F08080;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 30px;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #CD5C5C;
                color: white;
            }
        ''')
        self.maxslider = 50
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(1, self.maxslider)
        self.slider.setValue(self.maxslider // 2)
        self.slider.valueChanged.connect(self.on_slider_change)
        self.slider.setStyleSheet('''
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #B1B1B1, stop:1 #c4c4c4);
                margin: 2px 0;
            }

            QSlider::handle:horizontal {
                background: #50C878;
                border: none;
                height: 30px;
                width: 30px;
                margin: -10px 0;
                border-radius: 20px;
            }

            QSlider::handle:horizontal:hover {
                background: #3CB371;
                border: none;
                height: 30px;
                width: 30px;
                margin: -10px 0;
                border-radius: 20px;
            }
        ''')

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(self.pause_button)
        main_layout.addSpacing(40)
        main_layout.addWidget(self.slider)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.left_button)
        button_layout.addWidget(self.right_button)
        button_layout.setContentsMargins(0, 20, 0, 0)

        main_layout.addLayout(button_layout)

        self.show()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    row = mouse_pos[1] // self.square_size
                    col = mouse_pos[0] // self.square_size
                    self.array_now[row][col] = 0 if self.array_now[row][col] == 1 else 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_PLUS:
                        self.on_right_click()
                    if event.key == pygame.K_KP_MINUS:
                        self.on_left_click()
                    if event.key == pygame.K_SPACE:
                        self.on_pause_click()
            self.screen.fill(pygame.Color('black'))
            self.draw_grid()
            self.Game_of_Life_Logic()
            pygame.display.flip()
            self.clock.tick(self.speed)

    def draw_grid(self):
        length = len(self.array_now)
        for row in range(length):
            for col in range(length):
                rect = pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size)
                pygame.draw.rect(self.screen, self.rect_col, rect, 1)
                if self.array_now[row][col] == 1:
                    pygame.draw.rect(self.screen, self.fill_col, rect)

    def Game_of_Life_Logic(self):
        if self.active:
            kernel = np.array([[1, 1, 1],
                               [1, 0, 1],
                               [1, 1, 1]])
            convolved = convolve2d(self.array_now, kernel, mode='same')
            self.array_now = np.where((self.array_now == 1) & ((convolved < 2) | (convolved > 3)), 0, self.array_now)
            self.array_now = np.where((self.array_now == 1) & ((convolved == 2) | (convolved == 3)), 1, self.array_now)
            self.array_now = np.where((self.array_now == 0) & (convolved == 3), 1, self.array_now)

    def on_pause_click(self):
        self.active = not self.active
        self.pause_button.setText('⏸️' if self.active else '▶️')

    def on_slider_change(self, value):
        self.speed = value

    def on_left_click(self):
        if self.slider.value() > 1:
            self.slider.setValue(self.slider.value() - 1)
        else:
            print('Verlangsamung nicht möglich!')

    def on_right_click(self):
        if self.slider.value() < self.maxslider:
            self.slider.setValue(self.slider.value() + 1)
        else:
            print('Beschleunigung nicht möglich!')

    def closeEvent(self, event):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = Main()
    Main.run()
    sys.exit(app.exec())