from Model import Connect4, check_win
from View import View


class Controller:
    def __init__(self):
        self.view = View()
        self.view.welcome()
        while True:
            game = Connect4()
            if game.save_files and self.ask_input(self.view.load_game):
                self.view.show_saved_games()
                game.load_game(self.ask_input(self.view.choose_save_game))
            else:
                # TODO maybe add custom token symbols?? or even  r a n d o m  ones...
                i = 1
                if self.ask_input(self.view.AI_opponent):
                    game.create_player(i, i, True)
                    i = 2
                    game.create_player(i, i, self.ask_input(self.view.AI_match))
                else:
                    for i in range(2):
                        game.create_player(i, i, False)

            """actually play the game"""
            self.view.print_playingField(game)
            while not check_win(game) and not game.check_draw(game.tokens):

                self.view.print_players_turn(game.current_player)   # show playing field
                player_turn = self.ask_input(self.view.choose_column)   # ask for player turn
                if player_turn == "s":   # save game
                    if self.ask_input(self.view.confirmation):
                        name = self.ask_input(self.view.ask_name)
                        game.save_game(name)
                    break
                game.play_turn(int(player_turn))
                self.view.print_playingField(game)
            if game.check_draw(game.tokens):
                self.view.print_draw()
            elif check_win(game):
                self.view.print_winner((game.current_player + 1) % 2)

            if not (self.ask_input(self.view.another_game)):
                self.view.print_goodbye()
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
            answer = input(input_query)
            while True:
                name_correct = True
                for character in answer:
                    if character not in valid_inputs:
                        name_correct = False
                        break
                if name_correct:
                    return answer
                answer = input(self.view.wrong_input()).lower()

        query = view_function()   # ["Query", [accepted responses]]
        try:
            # query[2] = True for [y/n], query[2] = False for names.
            if query[2]:
                return check_input_bool(query[0], query[1], query[2])
            return check_names(query[0], query[1])
        except IndexError:
            return check_input(query[0], query[1])
