# Author: Javier Hernandez
# GitHub username: javihrz
# Date: 6/5/2024
# Description: A replication of atomic chess, but with no check or checkmate,
#              castling, en passant, or pawn promotion implementation.
#              Piece movements are made using the make_move() method.

class ChessVar:
    """
    Blueprint for creating and playing a game of atomic chess.
    """
    def __init__(self):
        self._chessboard = ["    a     b     c     d     e     f     g     h",
                            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
                            ["wP"] * 8,
                            ["  "] * 8, ["  "] * 8, ["  "] * 8, ["  "] * 8,
                            ["bP"] * 8,
                            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]]

        self._game_state = "UNFINISHED"
        self._turn_counter = 0
        self._squares = set()  # Will be used to filter invalid moves.

        for letter in ("a", "b", "c", "d", "e", "f", "g", "h"):
            for num in range(1, 9):
                self._squares.add(letter + str(num))

    def get_game_state(self) -> str:
        """
        Returns the current state of a game.
        """
        return self._game_state

    def set_game_state(self, game_state: str):
        """
        Updates a game state when a king is captured or exploded.
        :param game_state: The current state of the game.
        """
        self._game_state = game_state

    def get_piece(self, square: str) -> str:
        """
        Returns the chess piece located on a selected square.
        :param square: The square on the chessboard.
        """
        row = self.get_row(square)
        col = self.column_num(square)

        return row[col]

    def get_row(self, square: str) -> list[str]:
        """
        Returns the row where a selected square is located.
        :param square: The location on the chessboard.
        """
        row_num = int(square[1])
        row = self._chessboard[row_num]

        return row

    @staticmethod
    def column_num(square: str) -> int:
        """
        Returns the column (as a number) where a selected square is located.
        :param square: The location on the chessboard.
        """
        match square[0]:
            case "a":
                num = 0
            case "b":
                num = 1
            case "c":
                num = 2
            case "d":
                num = 3
            case "e":
                num = 4
            case "f":
                num = 5
            case "g":
                num = 6
            case "h":
                num = 7
            case _:
                num = -1

        return num

    @staticmethod
    def column_letter(col_num: int) -> str:
        """
        Returns the column (as a letter) where a selected square is located.
        :param col_num: The column represented as a number.
        """
        match col_num:
            case 0:
                letter = "a"
            case 1:
                letter = "b"
            case 2:
                letter = "c"
            case 3:
                letter = "d"
            case 4:
                letter = "e"
            case 5:
                letter = "f"
            case 6:
                letter = "g"
            case 7:
                letter = "h"
            case _:
                letter = "z"

        return letter

    def rook_moves(self, col_num: int, row_num: int, moves: set):
        """
        Adds to a set all 'squares' a rook can move to.
        :param col_num: The column represented as a number.
        :param row_num: The row represented as a number.
        :param moves: Set of all squares the piece can move to without restriction.
        """
        for num in range(row_num + 1, 9):  # Squares above rook.
            up_rows = self.column_letter(col_num) + str(num)
            if self.get_piece(up_rows) == "  ":
                moves.add(up_rows)
            else:
                moves.add(up_rows)
                break

        for num in range(row_num - 1, 0, -1):  # Squares below rook.
            down_rows = self.column_letter(col_num) + str(num)
            if self.get_piece(down_rows) == "  ":
                moves.add(down_rows)
            else:
                moves.add(down_rows)
                break

        for num in range(col_num + 1, 8):  # Rook's right squares.
            right_cols = self.column_letter(num) + str(row_num)
            if self.get_piece(right_cols) == "  ":
                moves.add(right_cols)
            else:
                moves.add(right_cols)
                break

        for num in range(col_num - 1, -1, -1):  # Rook's left squares.
            left_cols = self.column_letter(num) + str(row_num)
            if self.get_piece(left_cols) == "  ":
                moves.add(left_cols)
            else:
                moves.add(left_cols)
                break

    def bishop_moves(self, col_num: int, row_num: int, moves: set):
        """
        Adds to a set all 'squares' a bishop can move to.
        :param col_num: The column represented as a number.
        :param row_num: The row represented as a number.
        :param moves: Set of all squares the piece can move to without restriction.
        """
        rows_up, rows_down = 1, 1  # Sets variables for bishop's right side.

        for num in range(col_num + 1, 8):  # Upper-right diagonal.
            up_right_dgn = self.column_letter(num) + str(row_num + rows_up)
            rows_up += 1
            if int(up_right_dgn[1]) > 8:
                continue
            if self.get_piece(up_right_dgn) == "  ":
                moves.add(up_right_dgn)
            else:
                moves.add(up_right_dgn)
                break

        for num in range(col_num + 1, 8):  # Lower-right diagonal.
            down_right_dgn = self.column_letter(num) + str(row_num - rows_down)
            rows_down += 1
            if self.get_piece(down_right_dgn) == "  ":
                moves.add(down_right_dgn)
            else:
                moves.add(down_right_dgn)
                break

        rows_up, rows_down = 1, 1  # Resets variables for bishop's left side.

        for num in range(col_num - 1, -1, -1):  # Upper-left diagonal.
            up_left_dgn = self.column_letter(num) + str(row_num + rows_up)
            rows_up += 1
            if int(up_left_dgn[1]) > 8:
                continue
            if self.get_piece(up_left_dgn) == "  ":
                moves.add(up_left_dgn)
            else:
                moves.add(up_left_dgn)
                break

        for num in range(col_num - 1, -1, -1):  # Lower-left diagonal.
            down_left_dgn = self.column_letter(num) + str(row_num - rows_down)
            rows_down += 1
            if self.get_piece(down_left_dgn) == "  ":
                moves.add(down_left_dgn)
            else:
                moves.add(down_left_dgn)
                break

    def knight_moves(self, col_num: int, row_num: int, moves: set):
        """
        Adds to a set all 'squares' a knight can move to.
        :param col_num: The column represented as a number.
        :param row_num: The row represented as a number.
        :param moves: Set of all squares the piece can move to without restriction.
        """
        for num in range(row_num - 2, row_num + 3):
            if num == row_num or num <= 0 or num > 8:
                continue

            if abs((num - row_num)) % 2 == 0:  # Knight's inner range.
                one_left_ltr = self.column_letter(col_num - 1)
                one_right_ltr = self.column_letter(col_num + 1)

                if one_left_ltr != "z":
                    moves.add(one_left_ltr + str(num))
                if one_right_ltr != "z":
                    moves.add(one_right_ltr + str(num))

            elif abs(num - row_num) % 2 != 0:  # Knight's outer range.
                two_left_ltr = self.column_letter(col_num - 2)
                two_right_ltr = self.column_letter(col_num + 2)

                if two_left_ltr != "z":
                    moves.add(two_left_ltr + str(num))
                if two_right_ltr != "z":
                    moves.add(two_right_ltr + str(num))

    def king_moves(self, col_num: int, row_num: int, moves: set):
        """
        Adds to a set all 'squares' a king can move to.
        :param col_num: The column represented as a number.
        :param row_num: The row represented as a number.
        :param moves: Set of all squares the piece can move to without restriction.
        """
        for num in range(col_num - 1, col_num + 2):  # 3x3 radius.
            col_letter = self.column_letter(num)

            if col_letter == "z":
                continue

            moves.add(col_letter + str(row_num))
            if row_num - 1 != 0:
                moves.add(col_letter + str(row_num - 1))
            if row_num + 1 != 9:
                moves.add(col_letter + str(row_num + 1))

    def pawn_moves(self, piece: str, col_num: int, row_num: int, moves: set):
        """
        Adds to a set all 'squares' a pawn can move to.
        :param piece: A chess piece.
        :param col_num: The column represented as a number.
        :param row_num: The row represented as a number.
        :param moves: Set of all squares a piece can move to without restriction.
        """
        left_col = self.column_letter(col_num - 1)
        right_col = self.column_letter(col_num + 1)

        up_row, down_row = str(row_num + 1), str(row_num - 1)

        if piece == "wP":  # White pawn move checks.
            up_one_sq = self.column_letter(col_num) + up_row
            up_two_sq = self.column_letter(col_num) + str(row_num + 2)
            up_left_dgn, up_right_dgn = left_col + up_row, right_col + up_row

            if self.get_piece(up_one_sq) == "  ":  # Square above.
                moves.add(up_one_sq)

            if row_num == 2 and self.get_piece(up_two_sq) == "  ":  # 2 squares above.
                moves.add(up_two_sq)

            if self.get_piece(up_left_dgn) != "  ":  # Upper-left diagonal.
                moves.add(up_left_dgn)

            if self.get_piece(up_right_dgn) != "  ":  # Upper-right diagonal.
                moves.add(up_right_dgn)

        elif piece == "bP":  # Black pawn move checks.
            down_one_sq = self.column_letter(col_num) + str(row_num - 1)
            down_two_sq = self.column_letter(col_num) + str(row_num - 2)
            down_left_dgn, down_right_dgn = left_col + down_row, right_col + down_row

            if self.get_piece(down_one_sq) == "  ":  # Square below.
                moves.add(down_one_sq)

            if row_num == 7 and self.get_piece(down_two_sq) == "  ":  # 2 squares below.
                moves.add(down_two_sq)

            if self.get_piece(down_left_dgn) != "  ":  # Lower-left diagonal.
                moves.add(down_left_dgn)

            if self.get_piece(down_right_dgn) != "  ":  # Lower-right diagonal.
                moves.add(down_right_dgn)

    def find_squares(self, piece: str, sq_from: str) -> set:
        """
        Returns a set of squares a piece can move to after filtering invalid moves.
        :param piece: A chess piece.
        :param sq_from: The square the chess piece is moving from.
        """
        col_num, row_num = self.column_num(sq_from), int(sq_from[1])
        moves, valid_moves = set(), set()

        match piece[1]:
            case "Q":
                self.rook_moves(col_num, row_num, moves)
                self.bishop_moves(col_num, row_num, moves)
            case "R":
                self.rook_moves(col_num, row_num, moves)
            case "B":
                self.bishop_moves(col_num, row_num, moves)
            case "N":
                self.knight_moves(col_num, row_num, moves)
            case "K":
                self.king_moves(col_num, row_num, moves)
            case "P":
                self.pawn_moves(piece, col_num, row_num, moves)

        if sq_from in moves:  # Filters not moving a square.
            moves.remove(sq_from)

        for move in moves:  # Filters out-of-bounds board moves.
            if move in self._squares:
                valid_moves.add(move)

        return valid_moves

    def will_explode(self, sq_to: str):
        """
        Updates board after a movement. An explosion occurs if a capture is made.
        :param sq_to: The square the chess piece is moving to.
        """
        col_to, row_to = self.column_num(sq_to), int(sq_to[1])
        radius, dead_pieces, exploded_area = set(), set(), set()

        for num in range(col_to - 1, col_to + 2):  # Sets 3x3 explosion radius.
            col_letter = self.column_letter(num)

            if col_letter == "z":
                continue

            radius.add(col_letter + str(row_to))
            if row_to != 1:
                radius.add(col_letter + str(row_to - 1))
            if row_to != 8:
                radius.add(col_letter + str(row_to + 1))

        for square in radius:
            piece = self.get_piece(square)
            if piece[1] in (" ", "P"):  # Pawns will not be exploded.
                continue
            dead_pieces.add(piece), exploded_area.add(square)

        if {"bK", "wK"}.issubset(dead_pieces):  # Cannot explode both kings.
            return False
        if "bK" in dead_pieces and "wK" not in dead_pieces:
            self.set_game_state("WHITE_WON")
        elif "wK" in dead_pieces and "bK" not in dead_pieces:
            self.set_game_state("BLACK_WON")

        for square in exploded_area:
            col, row = int(self.column_num(square)), self.get_row(square)
            row[col] = "  "

    def is_move_valid(self, sq_from: str, sq_to: str, piece1: str, piece2: str) -> bool:
        """
        Returns False if any invalid cases apply before moving a piece.
        :param sq_from: The square the chess piece is moving from.
        :param sq_to: The square the chess piece is moving to.
        :param piece1: A chess piece on 'sq_from'.
        :param piece2: A chess piece or empty square on 'sq_to'.
        """
        if self.get_game_state() != "UNFINISHED":
            return False

        if piece1[0] == "b" and self._turn_counter % 2 == 0:  # Not black's turn.
            return False

        if piece1[0] == "w" and self._turn_counter % 2 != 0:  # Not white's turn.
            return False

        if piece1[0] == piece2[0]:  # Prevents w-to-w or b-to-b 'captures'.
            return False

        if piece1[1] == "K" and piece2 != "  ":  # Prevents kings from capturing.
            return False

        if int(sq_from[1]) in (1, 8) and piece1[1] == "P":  # Pawns stuck on outer rows.
            return False

        if sq_from == sq_to:
            return False

        if piece1 == "  ":
            return False

        if sq_to not in self.find_squares(piece1, sq_from):
            return False

        return True

    def make_move(self, sq_from: str, sq_to: str) -> bool:
        """
        Moves a piece from 'sq_from' to 'sq_to'. Returns True/False for valid/invalid moves.
        :param sq_from: The square the chess piece is moving from.
        :param sq_to: The square the chess piece is moving to.
        """
        if not {sq_from, sq_to}.issubset(self._squares):  # No moving outside board.
            return False

        piece1, piece2 = self.get_piece(sq_from), self.get_piece(sq_to)

        if self.is_move_valid(sq_from, sq_to, piece1, piece2) is False:
            return False

        if piece2 != "  ":  # Capture attempt.
            if self.will_explode(sq_to) is False:
                return False
            piece1 = "  "

        col_from, row_from = self.column_num(sq_from), self.get_row(sq_from)
        col_to, row_to = self.column_num(sq_to), self.get_row(sq_to)

        row_from[col_from], row_to[col_to] = "  ", piece1

        self._turn_counter += 1  # Keeps track of turns.
        return True

    def print_board(self):
        """
        Prints the current state of the chessboard.
        """
        print(self._chessboard[0])
        for row in range(8, 0, -1):
            print(str(row) + " " + str(self._chessboard[row]) + " " + str(row))
        print(self._chessboard[0])
