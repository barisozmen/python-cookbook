
from copy import deepcopy

class Piece:
    def __init__(self, color, kind):
        self.color = color  # 'W' or 'B'
        self.kind = kind    # 'P','R','N','B','Q','K'
        self.has_moved = False

    def __repr__(self):
        return self.kind if self.color=='W' else self.kind.lower()

class ChessBoard:
    def __init__(self):
        self.board = self.create_initial_board()
        self.turn = 'W'
        self.castling_rights = {'W': {'K': True, 'Q': True}, 'B': {'K': True, 'Q': True}}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.move_history = []

    def create_initial_board(self):
        b = [[None]*8 for _ in range(8)]
        # Pawns
        for i in range(8):
            b[1][i] = Piece('B','P')
            b[6][i] = Piece('W','P')
        # Rooks
        b[0][0] = b[0][7] = Piece('B','R')
        b[7][0] = b[7][7] = Piece('W','R')
        # Knights
        b[0][1] = b[0][6] = Piece('B','N')
        b[7][1] = b[7][6] = Piece('W','N')
        # Bishops
        b[0][2] = b[0][5] = Piece('B','B')
        b[7][2] = b[7][5] = Piece('W','B')
        # Queens
        b[0][3] = Piece('B','Q')
        b[7][3] = Piece('W','Q')
        # Kings
        b[0][4] = Piece('B','K')
        b[7][4] = Piece('W','K')
        return b

    def in_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def is_empty(self, row, col):
        return self.in_bounds(row, col) and self.board[row][col] is None

    def is_opponent(self, row, col, color):
        return self.in_bounds(row, col) and self.board[row][col] and self.board[row][col].color != color

    def generate_moves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece.color == self.turn:
                    moves.extend(self.generate_piece_moves(r, c, piece))
        return moves

    def generate_piece_moves(self, r, c, piece):
        moves = []
        if piece.kind == 'P':
            direction = -1 if piece.color == 'W' else 1
            # One step forward
            if self.is_empty(r+direction, c):
                moves.append(((r,c),(r+direction,c)))
                # Two steps if first move
                if not piece.has_moved and self.is_empty(r+2*direction, c):
                    moves.append(((r,c),(r+2*direction,c)))
            # Captures
            for dc in [-1,1]:
                nr, nc = r+direction, c+dc
                if self.is_opponent(nr, nc, piece.color):
                    moves.append(((r,c),(nr,nc)))
                # En passant
                if (nr,nc) == self.en_passant_target:
                    moves.append(((r,c),(nr,nc)))

        elif piece.kind == 'R':
            moves.extend(self.generate_sliding_moves(r,c,piece,[(1,0),(-1,0),(0,1),(0,-1)]))
        elif piece.kind == 'B':
            moves.extend(self.generate_sliding_moves(r,c,piece,[(1,1),(1,-1),(-1,1),(-1,-1)]))
        elif piece.kind == 'Q':
            moves.extend(self.generate_sliding_moves(r,c,piece,[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]))
        elif piece.kind == 'N':
            for dr, dc in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
                nr, nc = r+dr, c+dc
                if self.in_bounds(nr,nc) and (self.is_empty(nr,nc) or self.is_opponent(nr,nc,piece.color)):
                    moves.append(((r,c),(nr,nc)))
        elif piece.kind == 'K':
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    if dr == 0 and dc == 0: continue
                    nr, nc = r+dr, c+dc
                    if self.in_bounds(nr,nc) and (self.is_empty(nr,nc) or self.is_opponent(nr,nc,piece.color)):
                        moves.append(((r,c),(nr,nc)))
            moves.extend(self.generate_castling_moves(r,c,piece))
        return moves

    def generate_sliding_moves(self,r,c,piece,directions):
        moves = []
        for dr,dc in directions:
            nr, nc = r+dr, c+dc
            while self.in_bounds(nr,nc):
                if self.is_empty(nr,nc):
                    moves.append(((r,c),(nr,nc)))
                elif self.is_opponent(nr,nc,piece.color):
                    moves.append(((r,c),(nr,nc)))
                    break
                else:
                    break
                nr += dr
                nc += dc
        return moves

    def generate_castling_moves(self,r,c,piece):
        moves = []
        if piece.has_moved:
            return moves
        row = r
        # Kingside
        if self.castling_rights[piece.color]['K']:
            if all(self.is_empty(row,col) for col in range(c+1,7)):
                moves.append(((r,c),(row,6)))
        # Queenside
        if self.castling_rights[piece.color]['Q']:
            if all(self.is_empty(row,col) for col in range(1,c)):
                moves.append(((r,c),(row,2)))
        return moves

    def make_move(self, move):
        # Validate move is in legal moves
        legal_moves = self.generate_moves()
        if move not in legal_moves:
            raise ValueError(f"Illegal move: {move}")
            
        (r1,c1),(r2,c2) = move
        piece = self.board[r1][c1]
        captured = self.board[r2][c2]
        self.move_history.append((deepcopy(self.board), self.turn, deepcopy(self.castling_rights), self.en_passant_target, self.halfmove_clock, self.fullmove_number))
        
        # Move piece
        self.board[r2][c2] = piece
        self.board[r1][c1] = None

        # Pawn two-step sets en passant target
        if piece.kind == 'P' and abs(r2-r1) == 2:
            self.en_passant_target = ((r1+r2)//2,c1)
        else:
            self.en_passant_target = None

        # Update castling rights
        if piece.kind == 'K':
            self.castling_rights[piece.color]['K'] = False
            self.castling_rights[piece.color]['Q'] = False
        if piece.kind == 'R':
            if c1 == 0:
                self.castling_rights[piece.color]['Q'] = False
            elif c1 == 7:
                self.castling_rights[piece.color]['K'] = False

        piece.has_moved = True

        # Halfmove clock
        if piece.kind == 'P' or captured:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        # Fullmove
        if self.turn == 'B':
            self.fullmove_number += 1

        # Switch turn
        self.turn = 'B' if self.turn == 'W' else 'W'

    def undo_move(self):
        self.board, self.turn, self.castling_rights, self.en_passant_target, self.halfmove_clock, self.fullmove_number = self.move_history.pop()

    def print_board(self):
        
        NX = 33
        
        print('\n' + '-'*NX)
        for row in self.board:
            print('| ', end='')
            print(' '.join([str(p) + ' |' if p else '. |' for p in row]))
            print('-'*NX)
        print(f"Turn: {self.turn}")
        print(f"Castling rights: {self.castling_rights}")
        print(f"En passant target: {self.en_passant_target}")
        print(f"Halfmove clock: {self.halfmove_clock}, Fullmove number: {self.fullmove_number}\n")

def explain_move(board, move):
    
    long_piece_names = {
        'P': 'Pawn',
        'R': 'Rook',
        'N': 'Knight',
        'B': 'Bishop',
        'Q': 'Queen',
        'K': 'King'
    }
    
    (r1,c1),(r2,c2) = move
    piece = board.board[r1][c1]
    return f"{long_piece_names[piece.kind]}, {chr(ord('a')+c1)}{8-r1} > {chr(ord('a')+c2)}{8-r2}"


# Example usage
board = ChessBoard()
board.print_board()
moves = board.generate_moves()
print(f"Total legal moves at start: {len(moves)}")
print(moves)


while True:
    board.print_board()
    moves = board.generate_moves()
    print(f"Legal moves: {len(moves)}")
    for i,move in enumerate(moves):
        print(f"{i} - {explain_move(board, move)}")
        
        
    move_no = input("Turn: " + board.turn + "\nEnter move number: ")
    if move_no == 'undo':
        board.undo_move()
    else:
        board.make_move(moves[int(move_no)])