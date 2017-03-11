class Board(object):
    def __init__(self, size, player, cpu):
        self.rows = [Row(size)] * size
        self.player = player
        self.cpu = cpu
        self.won = False
        self.lost = False
        self.draw = False
        self.total_fields = size ** 2
        self.empty_fields = [Field()] * (size ** 2)
        self.taken_fields = []
        self.number_of_empty_fields = size ** 2
        self.number_of_taken_fields = 0

    def set_piece(self, coordinates, piece):
        self.rows[coordinates[0]].fields[coordinates[1]].piece = piece

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
            else:
                if self.number_of_empty_fields == 0:
                    self.draw = True

    def check_matching(self, data_set):
        for set in data_set:
            p1 = self.get_piece(set[0])
            p2 = self.get_piece(set[1])
            p3 = self.get_piece(set[2])
            if not p1 or not p2 or not p3:
                return False
            else:
                if p1 == p2 == p3:
                    return True
                else:
                    return False


class Row(object):
    def __init__(self, size):
        self.fields = [Field()] * size


class Field(object):
    def __init__(self):
        self.piece = None
        self.empty = bool(self.piece)
