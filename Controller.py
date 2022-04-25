from Model import Connect4
from View import View


class Controller:
    def __init__(self):
        self.view = View()
        view = self.view
        view.welcome()
        while True:
            self.game = Connect4()
            game = self.game
            loaded_save = False
            if game.save_files and self.ask_input(self.view.load_savegame_console):
                # unless a user wants to quit or loads a save game, the console asks more commands. 
                loaded_save = self.view.set_saved_games()
                self.save_game_console()

            if not loaded_save:
                # TODO maybe add custom token symbols?? or even  r a n d o m  ones...
                if self.ask_input(view.AI_opponent):

                    i = 0
                    game.create_player(i, i, self.ask_input(self.view.AI_match))
                    i = 1
                    game.create_player(i, i, True)
                else:
                    for i in range(2):
                        game.create_player(i, i, False)

            """actually play the game"""
            view.print_playingField(game)
            while not game.check_win() and not game.check_draw():

                view.print_players_turn(game.current_player,
                                             game.players[game.current_player].is_AI)   # print who has to play.

                if game.players[game.current_player].is_AI:   # if current player is AI, calculate best turn.
                    # to make game more authentic, AI does random turns, it has a while loop until the AI makes a valid turn
                    while not game.play_turn(game.AI_make_turn()):   
                        continue
                    view.print_playingField(game)
                    continue

                player_turn = self.ask_input(view.choose_column)   # ask for player turn
                if player_turn == "s":   # save game
                    if self.ask_input(self.view.confirmation):
                        name = self.ask_input(self.view.ask_name)
                        game.save_game(name)
                    break
                game.play_turn(int(player_turn))
                view.print_playingField(game)    # show playing field

            # check how the game was won and print a message.
            if game.check_draw():
                view.print_draw()
            elif game.check_win():
                game.swap_players()
                view.print_winner(game.current_player,
                                       game.players[game.current_player].is_AI)

            # check if player wants to play another game.
            if not (self.ask_input(view.another_game)):
                view.print_goodbye()
                break

    def ask_input(self, view_function):
        """Ask client for a response and validate said response.
           Will return the client input for instructions and
           True/False for Questions"""

        def check_input_bool(input_query: str, inputs: list, true_statements: list) -> bool:
            """converts input to True/False"""
            if check_input(input_query, inputs) in true_statements:
                return True
            return False

        def check_input(input_query: str, valid_inputs: list) -> str:
            """repeat input until correct response has been given"""
            answer = input(input_query)
            while answer not in valid_inputs:
                answer = input(self.view.wrong_input()).lower()
            return answer

        def check_names(input_query: str, valid_inputs: list) -> str:
            """checks if input only consists of legal characters"""
            answer = input(input_query)
            while True:
                name_correct = True
                for character in answer:
                    if character not in valid_inputs:
                        name_correct = False
                        break
                if name_correct:
                    return answer
                answer = input(self.view.wrong_input())
        
        query = view_function()   # ["Query", [accepted responses]]
        try:
            # query[2] != False for [y/n], query[2] = False for names.
            if query[2]:
                return check_input_bool(query[0], query[1], query[2])
            return check_names(query[0], query[1])
        except IndexError:
            return check_input(query[0], query[1])

    def save_game_console(self):

        def create_preview(name):
            preview_game = Connect4()
            preview_game.load_game(name)
            self.view.print_playingField(preview_game)

        def get_command():
            while True:   # loop until you get a command.
                query = input("-> ").split(" -")
                try:
                    # first check if commands are present, then check if name is valid.
                    assert query[1]
                    for i in range(1,len(query)):   # should someone chain: name -d -l ...
                        for command in query[i]:
                            # prevent doubled commands and invalid commands
                            if command not in valid_commands or command in used_commands:   
                                raise ValueError
                            used_commands.append(command)
                    
                    if query[0] not in self.view.save_games:
                        self.view.wrong_filename()
                        continue
                    return query[0], used_commands

                except IndexError:
                    # if no name/command has been specified, check for special commands.
                    # give error message if if no special command has been used
                    if query[0] in ['q', 'quit']:
                        return None
                    if query[0] in special_commands.keys():
                        special_commands[query[0]]()
                        continue
                    print(self.view.wrong_input())
                except ValueError:
                    self.view.wrong_command()

        # l: load, d: delete, p: preview
        file_name = None
        valid_commands = {
            'p': create_preview,
            'l': self.game.load_game,
            'd': self.game.delete_save
        }
        special_commands = {
            'help': self.view.manpage,
            'ls':   self.view.show_saved_games
        }

        no_game_loaded = True
        self.view.save_game_info()
        while no_game_loaded:
            used_commands = []
            try:
                file_name, commands = get_command()
                if 'l' in commands:
                    no_game_loaded = False
                # will execute commands in declaration order of valid_commands
                for key in valid_commands.keys(): 
                    if key in commands:
                        valid_commands[key](file_name)
            except TypeError:   # this happens if "None" (for quit) is returned and will close the console..
                break
        return no_game_loaded
