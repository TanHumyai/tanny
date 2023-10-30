import tkinter as tk
import random
directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]


class OthelloPVA():
    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.geometry('560x400')
        self.root.resizable(width=False,height=False)
        self.root.title("Othello PVA Medium Mode")
        self.player = 'B'
        self.color='green'
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="grey")
        self.canvas.grid(row=1, column=1)

        self.side_frame = tk.Frame(self.root, height=400, bg="black")
        self.side_frame.grid(row=0, rowspan=10, column=2, sticky="nsew")

        self.info_label = tk.Label(self.side_frame, text="Your Turn", bg="black", fg="white", font=('Arial', 20))
        self.info_label.pack(pady=20)

        self.white_count_label = tk.Label(self.side_frame, text="White: 2", bg="black", fg="white", font=('Arial', 15))
        self.white_count_label.pack(pady=5)

        self.black_count_label = tk.Label(self.side_frame, text="Black: 2", bg="black", fg="white", font=('Arial', 15))
        self.black_count_label.pack(pady=5)

        self.restart_button = tk.Button(self.side_frame, text="Restart Game", bg="grey", fg="white", font='5', command=self.restart_game)
        self.restart_button.pack(side="bottom", pady=10)
        #ตั้งตัวเริ่ม
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'

        self.draw_board()
        #กำหนดให้canvasตอบสนองกับ left click
        self.canvas.bind("<Button-1>", self.handle_click)
        
        # Add a button to change board color
        self.change_color_button = tk.Button(self.side_frame, text="Change Board Color", bg="grey", fg="white", font='5', command=self.change_board_color)
        self.change_color_button.pack(pady=5)
        #ตเพิ่มเวลา
        self.timer_running = False
        self.elapsed_time = 0
        self.timer_label = tk.Label(self.side_frame, text="Time: 0:0", bg="black", fg="white", font= 15)
        self.timer_label.pack(pady=5)
        self.quit_button = tk.Button(self.side_frame, text="Quit", bg="grey", fg="white", font='5',command=self.root.destroy)
        self.quit_button.pack(pady=10)   
        self.start_timer()
        self.root.mainloop()
    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            if seconds<10:
                seconds='0'+str(seconds)
            self.timer_label.config(text=f"Time: {minutes} : {seconds}")
            self.elapsed_time += 1
            self.root.after(1000, self.update_timer)

    def stop_timer(self):
        self.timer_running = False

    def change_board_color(self):
        # List of colors
        colors = ["green","lightblue", "red", "yellow", "violet","#98633B","pink"]
        
        # Get next color from the list
        next_index = (colors.index(self.color) + 1) % len(colors)
        new_color = colors[next_index]
        # Change the canvas background color
        self.canvas.config(bg=new_color)
        self.color=new_color
        print(self.color)
        # Redraw the board
        self.draw_board()

    def update_piece_count(self):
        white_count = sum(row.count('W') for row in self.board)
        black_count = sum(row.count('B') for row in self.board)
        self.white_count_label.config(text=f"White: {white_count}")
        self.black_count_label.config(text=f"Black: {black_count}")

    def check_end_game(self,turn):
        for row in range(8):
            for col in range(8):
                if self.valid_move(col, row, turn):
                    return False
        self.stop_timer()
        return True

    def draw_board(self):
        size = 45
        self.canvas.delete("all")        
        self.canvas.config(background='grey')
        if self.check_end_game(self.player):
            white_count = sum(row.count('W') for row in self.board)
            black_count = sum(row.count('B') for row in self.board)
            if white_count > black_count:
                self.info_label.config(text="White Wins!")
            elif white_count < black_count:
                self.info_label.config(text="Black Wins!")
            else:
                self.info_label.config(text="It's a Tie!")     
        for col in range(8):
            self.canvas.create_text(col *size + 50,15, text=chr(col + 65))

        for row in range(8):
            self.canvas.create_text(15, row * size + 50, text=str(row + 1))
        for row in range(8):
            for col in range(8):
                x1, y1 = (col * size)+25, (row * size)+25
                x2, y2 = (x1 + size), (y1 + size)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.color, outline="black")
                if self.board[row][col] == 'B':
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="black")
                elif self.board[row][col] == 'W':
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="white")
                elif self.valid_move(col, row, self.player):
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline='black')
        self.update_piece_count()
    def bot_move(self):
        best_move = None
        max_flips = 0
        discs_to_flip_best = []  
        for y in range(8):
            for x in range(8):
                discs_to_flip = self.valid_move(x, y, 'W')
                if discs_to_flip:
                    if len(discs_to_flip) > max_flips:
                        max_flips = len(discs_to_flip)
                        best_move = (x, y)
                        discs_to_flip_best = discs_to_flip  
        if best_move:
            x, y = best_move
            self.board[y][x] = 'W'
            for fx, fy in discs_to_flip_best:  
                self.board[fy][fx] = 'W'
            self.draw_board()

    def handle_click(self, event):
        x, y = (event.x-25) //45 , (event.y-25)// 45
        print(self.board)
        discs_to_flip = self.valid_move(x, y, self.player)
        if discs_to_flip:
            self.board[y][x] = self.player
            for fx, fy in discs_to_flip:
                self.board[fy][fx] = self.player
            if self.player == 'B':
                self.player = 'W'
                self.info_label.config(text="White's Turn")
                self.bot_move()
            
                self.player = 'B'
                self.info_label.config(text="Your Turn")
            else:
                self.player = 'B'
                self.info_label.config(text="Your Turn")
            self.draw_board()

            
    def restart_game(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        self.player = 'B'
        self.info_label.config(text="Black's Turn")
        self.draw_board()
        if self.timer_running==True:
            self.stop_timer()
            self.elapsed_time = 0
            self.timer_running=True
        else:
            self.elapsed_time = 0
            self.start_timer()
    def valid_move(self, x, y, player):
        if self.board[y][x] != ' ':
            return []

        opponent = 'B' if player == 'W' else 'W'
        discs_to_flip = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            temp_flip = []

            while 0 <= nx < 8 and 0 <= ny < 8 and self.board[ny][nx] == opponent:
                temp_flip.append((nx, ny))
                nx, ny = nx + dx, ny + dy

            if 0 <= nx < 8 and 0 <= ny < 8 and self.board[ny][nx] == player and temp_flip:
                discs_to_flip.extend(temp_flip)

        return discs_to_flip
    def on_closing(self):
        self.stop_timer()
        self.root.destroy()

    
def main():
    game = OthelloPVA()

if __name__ == '__main__':
    main()
