import random
import pygame
import sys
from settings import *


class SudokuGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SUDOKU")
        self.time = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 50)
        #Сгенерированная матрица
        self.matrix = [[str(num) for num in row] for row in DEFAULT_SUDOKU]
        #Решенная матраца
        self.solved_matrix = [[""] * 9 for _ in range(9)]
        #Матрица для ввода чисел от игрока
        self.game_matrix = [[""] * 9 for _ in range(9)]
        #Матрица для получения позиции
        self.coordinate_matrix = [[""] * 9 for _ in range(9)]
        #X позиция
        self.x_pos = 0
        #Y позиция
        self.y_pos = 0
        #Вводимое значение
        self.value = ""

    
    def transpose_matrix(self):
        """Транспонируем матрицу"""
        #Переменная, для транспонирования
        matrix_for_transpose = [[""] * 9 for _ in range(9)]
        for i in range(SIZE):
            for j in range(SIZE):
                matrix_for_transpose[i][j] = self.matrix[j][i]

        for i in range(SIZE):
            for j in range(SIZE):
                self.matrix[i][j] = matrix_for_transpose[i][j]


    def swap_rows(self):
        """Меняем местами строки"""   
        row_index = random.randint(0, 7)
        if 0 <= row_index <= 2:
            variants = list(range(0, 3))
            variants.remove(row_index)
            indx = random.choice(variants)
            self.matrix[indx], self.matrix[row_index] = self.matrix[row_index], self.matrix[indx]

        if 3 <= row_index <= 5:
            variants = list(range(3, 6))
            variants.remove(row_index)
            indx = random.choice(variants)
            self.matrix[indx], self.matrix[row_index] = self.matrix[row_index], self.matrix[indx]

        if 6 <= row_index <= 8:
            variants = list(range(6, 9))
            variants.remove(row_index)
            indx = random.choice(variants)
            self.matrix[indx], self.matrix[row_index] = self.matrix[row_index], self.matrix[indx]    


    def swap_column(self):
        """Меняем столбцы местами, используя функции transpose_matrix и swap_rows"""  
        self.transpose_matrix()
        self.swap_rows()
        self.transpose_matrix()


    def swap_vertical_blocks(self):
        """Меняем местами вертикальные блоки"""
        blocks = random.randint(1, 3)
        for row in range(SIZE):
            if blocks == 1 and row <= 2:
                (self.matrix[row], 
                 self.matrix[row + 6]) = (self.matrix[row + 6], 
                                               self.matrix[row])

            if blocks == 2 and 3 <= row <= 5:
                if random.random() == 0:
                    (self.matrix[row], 
                     self.matrix[row + 3]) = (self.matrix[row + 3], 
                                                  self.matrix[row])
                else:
                    (self.matrix[row], 
                     self.matrix[row - 3]) = (self.matrix[row - 3], 
                                                  self.matrix[row])

            if blocks == 3 and 6 <= row <= 8:
                (self.matrix[row], 
                 self.matrix[row - 6]) = (self.matrix[row - 6], 
                                              self.matrix[row])


    def swap_horizontal_blocks(self):
        """Меняем горизонтальные блоки используя transpose_matrix
        и swap_vertical_blocks"""
        self.transpose_matrix()
        self.swap_vertical_blocks()
        self.transpose_matrix()

    
    def generate_sudoku_for_game(self):
        """Генерируем матрицу"""
        #Записываем, все возможные методы, для генерации
        methods = [
                self.transpose_matrix(),
                self.swap_rows(),
                self.swap_column(),
                self.swap_vertical_blocks(),
                self.swap_horizontal_blocks()
                ]
        #Перемешиваем список
        random.shuffle(methods)
        #Генерируем
        for _ in range(random.randint(20, 40)):
            random.choice(methods)


    def remove_nums(self):
        """Удаляем элементы судоку"""
        all_index = list(range(9))
        iteration_list = [6, 7]

        for row in range(SIZE):
            remove_list = all_index[:]
            random.shuffle(remove_list)

            for _ in range(random.choice(iteration_list)):
                indx = random.choice(remove_list)
                self.matrix[row][indx] = ""
                remove_list.remove(indx)


    def print_matrix(self):
        """Функция для вывода матрицы в терминале"""
        for i in range(SIZE):
            for j in range(SIZE):
                print(self.matrix[i][j], end=" ")

            print()


    def draw_grid(self):
        """Рисуем сетку"""
        line_x_position, line_y_position = 10, 10
        for _ in range(4):
            pygame.draw.line(
                    self.screen, "black",
                    (line_x_position, 10),
                    (line_x_position, LINE_LENGTH), LINE_SIZE  
                    )

            pygame.draw.line(
                    self.screen, "black",
                    (10, line_y_position),
                    (LINE_LENGTH, line_y_position), LINE_SIZE
                    )

            line_x_position += BIG_BLOCK
            line_y_position += BIG_BLOCK


    def draw_rect(self):
        """Заполняем сетку квадратами"""
        rect_x_position, rect_y_position = 10, 10
        for _ in range(SIZE):
            for _ in range(SIZE):
                pygame.draw.rect(
                        self.screen, "black",
                        (rect_x_position, rect_y_position,
                         RECT_SIZE, RECT_SIZE),
                        RECT_MARGIN
                        )
                rect_y_position += SMALL_BLOCK

            rect_x_position += SMALL_BLOCK
            rect_y_position = 10


    def select_rect(self):
        for row in range(SIZE):
            for column in range(SIZE):
                get_x_position = column * (RECT_SIZE - RECT_MARGIN) + 10
                get_y_position = row * (RECT_SIZE - RECT_MARGIN) + 10
                if self.coordinate_matrix[row][column] == "1" and self.matrix[row][column] == "":
                    pygame.draw.rect(
                            self.screen, "black",
                            (get_x_position, get_y_position,
                             RECT_SIZE, RECT_SIZE),
                            RECT_MARGIN + 3
                    )

    
    def draw_matrix(self):
        text_position = [28, 9]

        for i in range(SIZE):
            for j in range(SIZE):

                self.text = self.font.render(
                        self.matrix[i][j],
                        True, TEXT_COLOR
                        )

                self.screen.blit(self.text, text_position)
                text_position[0] += SMALL_BLOCK

            text_position[1] += SMALL_BLOCK
            text_position[0] = 25


    def draw_input_numbers(self):
        text_position = [28, 9]

        for i in range(SIZE):
            for j in range(SIZE):

                if (self.coordinate_matrix[i][j] == "1" and 
                    self.matrix[i][j] == "" and self.value != "" and
                    self.value not in self.matrix[i]):
                    self.game_matrix[i][j] = self.value

                if self.game_matrix[i].count(self.game_matrix[i][j]) > 1:
                    text_color = WRONG_TEXT
                else:
                    text_color = INPUT_TEXT_COLOR

                self.text = self.font.render(
                        self.game_matrix[i][j],
                        True, text_color
                        )

                self.screen.blit(self.text, text_position)
                text_position[0] += SMALL_BLOCK

            text_position[1] += SMALL_BLOCK
            text_position[0] = 25
        self.value = ""


    def update(self):
        pygame.display.flip()
        self.time.tick(FPS)
        

    def draw_object(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_grid()
        self.draw_rect()
        self.draw_matrix()
        self.select_rect()
        self.draw_input_numbers()


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.x_pos += 1
                if event.key == pygame.K_LEFT:
                    self.x_pos -= 1
                if event.key == pygame.K_UP:
                    self.y_pos -= 1
                if event.key == pygame.K_DOWN:
                    self.y_pos += 1

            if self.x_pos > 8:
                self.x_pos = 0
            if self.x_pos < 0:
                self.x_pos = 8

            if self.y_pos > 8:
                self.y_pos = 0
            if self.y_pos < 0:
                self.y_pos = 8

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    self.value = "1"
                if event.key == pygame.K_2:
                    self.value = "2"
                if event.key == pygame.K_3:
                    self.value = "3"
                if event.key == pygame.K_4:
                    self.value = "4"
                if event.key == pygame.K_5:
                    self.value = "5"
                if event.key == pygame.K_6:
                    self.value = "6"
                if event.key == pygame.K_7:
                    self.value = "7"
                if event.key == pygame.K_8:
                    self.value = "8"
                if event.key == pygame.K_9:
                    self.value = "9"
                if event.key == pygame.K_SPACE:
                    self.value = " "
        self.coordinate_matrix[self.y_pos][self.x_pos] = "1"


    def run(self):  

        self.generate_sudoku_for_game()
        self.remove_nums()
        self.print_matrix()
        while True:
            self.check_events()
            self.update()
            self.draw_object()
            self.coordinate_matrix[self.y_pos][self.x_pos] = ""


if __name__ == "__main__":
    game = SudokuGame()
    game.run()
