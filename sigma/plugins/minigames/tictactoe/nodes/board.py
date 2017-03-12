class Board(object):
    def __init__(self,player, cpu):
        self.rows = [Row() for i in range(3)]
        self.player = player
        self.cpu = cpu
        self.won = False
        self.lost = False
        self.draw = False
        self.over = False
        self.total_fields = 3 ** 2
        self.empty_fields = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        self.taken_fields = []
        self.number_of_empty_fields = self.total_fields
        self.number_of_taken_fields = 0

    def view(self):
        top = [':arrow_lower_right:', ':regional_indicator_a:', ':regional_indicator_b:', ':regional_indicator_c:']
        left = [':one:', ':two:', ':three:']
        row_loc = 0
        out_text = ''.join(top)
        for row in self.rows:
            row_text = ''
            for field in row.fields:
                piece = field.piece
                if piece:
                    row_text += f':regional_indicator_{field.piece.lower()}:'
                else:
                    row_text += ':white_large_square:'
            out_text += f'\n{left[row_loc]}{row_text}'
            row_loc += 1
        return out_text

    def set_piece(self, coordinates, piece):
        self.rows[coordinates[0]].fields[coordinates[1]].set_piece(piece)
        self.taken_fields.append(coordinates)
        self.empty_fields.remove(coordinates)
        self.update_status()

    def player_move(self, coordinates):
        self.set_piece(coordinates, self.player)

    def cpu_move(self, coordinates):
        self.set_piece(coordinates, self.cpu)

    def get_piece(self, coordinates):
        return self.rows[coordinates[0]].fields[coordinates[1]].piece

    def update_status(self):
        win_combos = [[[[0, 0], [1, 0], [2, 0]], [[0, 1], [1, 1], [2, 1]], [[0, 2], [1, 2], [2, 2]]],  # Horizontal Wins
                      [[[0, 0], [0, 1], [0, 2]], [[1, 0], [1, 1], [1, 2]], [[2, 0], [2, 1], [2, 2]]],  # Vertical Wins
                      [[[0, 0], [1, 1], [2, 2]], [[0, 2], [1, 1], [2, 0]]]]  # Diagonal Wins
        for combo in win_combos:
            finish = self.check_matching(combo)
            if finish:
                checked_piece = self.get_piece(combo[0][0])
                if checked_piece == self.player:
                    self.won = True
                else:
                    self.lost = True
                self.over = True
            else:
                if self.number_of_empty_fields == 0:
                    self.draw = True
                    self.over = True

    def check_matching(self, data_set):
        results = []
        for coordinate in data_set:
            p1 = self.get_piece(coordinate[0])
            p2 = self.get_piece(coordinate[1])
            p3 = self.get_piece(coordinate[2])
            if not p1 or not p2 or not p3:
                results.append(False)
            else:
                if p1 == p2 == p3:
                    results.append(True)
                else:
                    results.append(False)
        for result in results:
            if result:
                return True


class Row(object):
    def __init__(self):
        self.fields = [Field() for i in range(3)]


class Field(object):
    def __init__(self):
        self.piece = None
        self.empty = bool(self.piece)

    def set_piece(self, piece):
        self.piece = piece
