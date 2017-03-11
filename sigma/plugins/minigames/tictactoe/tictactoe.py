from .nodes.board import Board

translation = {
    'a1': 0, 'b1': 1, 'c1': 2,
    'a2': 3, 'b2': 4, 'c2': 5,
    'a3': 6, 'b3': 7, 'c3': 8,
}


async def tictactoe(cmd, message, args):
    board = Board(3, 'X', 'O')
    board.set_piece([0, 1], 'X')
    await cmd.bot.send_message(message.channel, board.view())
