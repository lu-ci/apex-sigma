import discord
import random
from .nodes.board import Board

games = {}


async def tictactoe(cmd, message, args):
    if args:
        player = message.author
        if args[0].lower() == 'start':
            if player.id in games:
                response = discord.Embed(color=0xFF9900, title='⚠ You are already in a game.')
                await message.channel.send(None, embed=response)
            else:
                coinflip = random.randint(0, 1)
                if coinflip == 0:
                    player_sign = 'X'
                    cpu_sign = 'O'
                    player_first = True
                else:
                    player_sign = 'O'
                    cpu_sign = 'X'
                    player_first = False
                board = Board(player_sign, cpu_sign)
                games.update({player.id: board})
                if player_first:
                    response = discord.Embed(color=0x1ABC9C)
                    response.add_field(name='🎲 You go first.', value=board.view())
                else:
                    corners = [[0, 0], [0, 2], [2, 0], [2, 2]]
                    coords = random.choice(corners)
                    board = games[player.id]
                    board.cpu_move(coords)
                    response = discord.Embed(color=0x1ABC9C)
                    response.add_field(name='🎲 Sigma goes first.', value=board.view())
                await message.channel.send(None, embed=response)
        elif args[0].lower() == 'quit':
            if player.id in games:
                del games[player.id]
                response = discord.Embed(color=0x66CC66, title='✅ Game purged.')
            else:
                response = discord.Embed(color=0xFF9900, title='⚠ You were not found in a game.')
            await message.channel.send(None, embed=response)
        else:
            translation = {
                'a1': [0, 0], 'b1': [0, 1], 'c1': [0, 2],
                'a2': [1, 0], 'b2': [1, 1], 'c2': [1, 2],
                'a3': [2, 0], 'b3': [2, 1], 'c3': [2, 2]
            }
            if player.id in games:
                board = games[player.id]
                coord = args[0].lower()
                if coord in translation:
                    coord = translation[coord]
                    if coord not in board.taken_fields:
                        board.player_move(coord)
                        if len(board.empty_fields) != 0:
                            if not board.over:
                                board.cpu_move(random.choice(board.empty_fields))
                        if board.over:
                            if board.won:
                                embed_color = 0x66CC66
                                embed_title = ':tada: You won!'
                            elif board.lost:
                                embed_color = 0xDB0000
                                embed_title = ':fire: You lost...'
                            elif board.draw:
                                embed_color = 0x696969
                                embed_title = ':link: It\'s a draw.'
                            else:
                                embed_color = 0x1ABC9C
                                embed_title = 'Tic Tac Toe'
                            del games[player.id]
                        else:
                            embed_color = 0x1ABC9C
                            embed_title = 'Tic Tac Toe'
                        response = discord.Embed(color=embed_color)
                        response.add_field(name=embed_title, value=board.view())
                    else:
                        response = discord.Embed(color=0xFF9900, title='⚠ Invalid coordinates.')
                else:
                    response = discord.Embed(color=0xFF9900, title='⚠ Invalid coordinates.')
            else:
                response = discord.Embed(color=0xFF9900, title='⚠ You were not found in a game.')
            await message.channel.send(None, embed=response)
