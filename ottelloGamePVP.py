import tkinter as tk
# A list of all 8 directions (north, northeast, east, southeast, south, southwest, west, northwest).
directions = [(-1, 0),(-1, 1),(0, 1),(1, 1),(1, 0),(1, -1),(0, -1),(-1, -1)]
class OthelloPVP():
    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.geometry('560x400')
        self.root.resizable(width=False,height=False)
        self.root.title("Othello PVP Mode")
        self.player = 'B'
        self.color='green'
        # Setting up canvas for the game board.
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="grey")
        self.canvas.grid(row=1, column=1)
        # Frame for side information
        self.side_frame = tk.Frame(self.root, height=400, bg="black")
        self.side_frame.grid(row=0, rowspan=10, column=2, sticky="nsew")
        # Info label to indicate whose turn it is.
        self.info_label = tk.Label(self.side_frame, text="Black's Turn", bg="black", fg="white", font=('Arial', 20))
        self.info_label.pack(pady=20)
        # Labels to display white current piece counts.
        self.white_count_label = tk.Label(self.side_frame, text="White: 2", bg="black", fg="white", font=('Arial', 15))
        self.white_count_label.pack(pady=5)
        # Labels to display current black piece counts.
        self.black_count_label = tk.Label(self.side_frame, text="Black: 2", bg="black", fg="white", font=('Arial', 15))
        self.black_count_label.pack(pady=5)
        # Button to restart the game.
        self.restart_button = tk.Button(self.side_frame, text="Restart Game", bg="grey", fg="white", font='5', command=self.restart_game)
        self.restart_button.pack(side="bottom", pady=10)
        # Add a button to change board color
        self.change_color_button = tk.Button(self.side_frame, text="Change Board Color", bg="grey", fg="white", font='5', command=self.change_board_color)
        self.change_color_button.pack(pady=5)
        # Button to exit the game.
        self.quit_button = tk.Button(self.side_frame, text="Quit", bg="grey", fg="white", font='5',command=self.root.destroy)
        self.quit_button.pack(pady=10)        
        
        #ตั้งตัวเริ่ม
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'

        self.draw_board()
        #กำหนดให้canvasตอบสนองกับ left click
        self.canvas.bind("<Button-1>", self.handle_click)
        
        #ตัวเพิ่มเวลา
        self.timer_running = False
        self.elapsed_time = 0
        self.timer_label = tk.Label(self.side_frame, text="Time: 0:0", bg="black", fg="white", font= 15)
        self.timer_label.pack(pady=5)
        self.start_timer()
        self.root.mainloop()
        
    def draw_board(self):
        # Setting the size for each square of the board.
        size = 45
        # Clearing any previous drawings from the canvas.
        self.canvas.delete("all")        
        self.canvas.config(background='grey')
         #Draws the board and all the pieces
        for row in range(8):
            for col in range(8):
                x1, y1 = (col * size)+25, (row * size)+25
                x2, y2 = (x1 + size), (y1 + size)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.color, outline="black")
                 # If the square has a black piece, draw a black circle.
                if self.board[row][col] == 'B':
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="black")
                 # If the square has a white piece, draw a white circle.
                elif self.board[row][col] == 'W':
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="white")
                # If the square is a valid move, outline the possible move with a circle.
                elif self.valid_move(col, row, self.player):
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline='black')
        # Add letters (A to H) at the top of the board.
        for col in range(8):
            self.canvas.create_text(col *size + 50,15, text=chr(col + 65))
        # Add numbers (1 to 8) on the left side of the board.
        for row in range(8):
            self.canvas.create_text(15, row * size + 50, text=str(row + 1))
        #update piece
        self.update_piece_count()
        # Check if the game has ended.
        if self.check_end_game(self.player):
            white_count = sum(row.count('W') for row in self.board)
            black_count = sum(row.count('B') for row in self.board)
            if white_count > black_count:
                self.info_label.config(text="White Wins!")
            elif white_count < black_count:
                self.info_label.config(text="Black Wins!")
            else:
                self.info_label.config(text="It's a Tie!")     
       
        
    def handle_click(self, event):
        #Handles the canvas click event
        x, y = (event.x-25) //45 , (event.y-25)// 45
        discs_to_flip = self.valid_move(x, y, self.player)
        if discs_to_flip:
            self.board[y][x] = self.player
            for fx, fy in discs_to_flip:
                self.board[fy][fx] = self.player
            self.player = 'B' if self.player == 'W' else 'W'
            self.info_label.config(text="White's Turn" if self.player == 'W' else "Black's Turn")
            self.draw_board()
    def update_piece_count(self):
        #Updates the displayed piece counts for both players
        white_count = sum(row.count('W') for row in self.board)
        black_count = sum(row.count('B') for row in self.board)
        self.white_count_label.config(text=f"White: {white_count}")
        self.black_count_label.config(text=f"Black: {black_count}")
    
    def valid_move(self, x, y, player):
        #Checks if the move is valid for the given player.
        if self.board[y][x] != ' ':
            return []
        opponent = 'B' if player == 'W' else 'W'
        discs_to_flip = []
        #Checks in a given direction for discs to flip.
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            temp_flip = []

            while 0 <= nx < 8 and 0 <= ny < 8 and self.board[ny][nx] == opponent:
                temp_flip.append((nx, ny))
                nx, ny = nx + dx, ny + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and self.board[ny][nx] == player and temp_flip:
                discs_to_flip.extend(temp_flip)
        return discs_to_flip
    # Timer setup.
    def start_timer(self):
        """Starts the timer."""
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        # Updates the timer every second
        if self.timer_running:
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            if seconds<10:
                seconds='0'+str(seconds)
            self.timer_label.config(text=f"Time: {minutes} : {seconds}")
            self.elapsed_time += 1
            self.root.after(1000, self.update_timer)
    def stop_timer(self):
        # Stops the timer
        self.timer_running = False

    def change_board_color(self):
        # Changes the board color
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
    

    def check_end_game(self,turn):
        #Checks if the game has ended.
        for row in range(8):
            for col in range(8):
                if self.valid_move(col, row, turn):
                    return False
        self.stop_timer()
        return True
        
    
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
            self.elapsed_time = 0
        else:
            self.elapsed_time = 0
            self.start_timer()

    def on_closing(self):
        self.stop_timer()
        self.root.destroy()
def main():
    game = OthelloPVP()

if __name__ == '__main__':
    main()
