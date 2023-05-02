import random


### A Die is a integer between 1 and 6.
### A DiceTotal is an integer between 2 and 12
###    (the sum of two Die values)


## DO NOT CHANGE
def roll(debug_mode):
    '''
    Returns a random integer value between 1 and 6, inclusive,
    if debug_mode is False, and returns value entered by the
    player if debug_mode is True

    Effects:
       Reads in an integer if debug_mode is True

    roll: Bool -> Nat
    '''
    if debug_mode:
        debugging_prompt = "Enter a die value between 1 and 6: "
        die = input(debugging_prompt)
        while not (die.isdigit()) or (int(die) < 1 or int(die) > 6):
            die = input("Invalid entry. " + debugging_prompt)
        return (int(die))
    else:
        return random.randint(1, 6)

    ##COMPLETE BELOW


def pairs(d1, d2, d3, d4):
    '''
    Returns a list of combination totals of the four dice
    d1, d2, d3, d4 where each combination is distinct
    (independent of order) and is of length 2, and the first
    values in the inner lists are less than or equal to the
    second value. The inner lists may contain duplicates,
    while the returned list does not. The list is sorted in
    increasing order of the first value.

    pairs: Die Die Die Die -> (listof (list DiceTotal DiceTotal))

    Examples:
       pairs(3,3,3,3) => [[6,6]]
       pairs(4,4,3,5) => [[7,9],[8,8]])
       pairs(4,1,6,5) => [[5,11],[6,10],[7,9]])
    '''
    lst = [sorted([d1 + d2, d3 + d4]), sorted([d1 + d3, d2 + d4]), sorted([d1 + d4, d2 + d3])]

    lst.sort()

    pairs = []

    for i in lst:
        if i not in pairs:
            pairs.append(i)

    return pairs


## Tests to get you started
## All commented out with triple string quotes to start
'''
check.expect("pairs 1: three different pairs", pairs(4,1,6,5), [[3,8],[4,7],[5,6]])
## Add additional tests to cover different possibilities you need to consider for pairs
## Be sure to consider possibilties for different inputs and different numbers of 
## pairs in your returned list.
'''



class Player:
    '''
       Fields:
          name (Str)
                   [player's non-empty name]
          totals (dictof DiceTotal Nat) has length <= 11
                   [player's totals for each playable DiceTotal
                   keys are integers 2-12
                   (corresponding to the unclaimed columns of the board)
                   and the values are the playerâ€™s current
                   position in each column]
          claimed (listof DiceTotal)
                  [columns claimed by the player, kept in increasing order]
    '''

    def __init__(self, n):
        '''
        Creates a new Player with name n,
        totals set to dictionary with keys 2 through 12, and values 0,
        and no claimed columns

        Effects: Mutates Player

        __init__: Player Str -> None
        '''
        self.name = n

        self.totals = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}

        self.claimed = []

    ##DO NOT CHANGE __repr__
    def __repr__(self):
        '''
        Returns a string representation of Player

        __repr__: Player -> Str
        '''
        return ('Player {0} has totals {1} and has claimed columns {2}'.format(
            self.name, self.totals, self.claimed))

    def __eq__(self, other):
        '''
        Returns True if self and other are identical, and False if not

        __eq__ Player Any -> Bool
        '''
        if self.name == other.name and self.totals == other.totals \
                and self.claimed == other.claimed:
            return True

        else:
            return False

    def update_totals(self, current, targets):
        '''
        Updates self.totals to reflect the values that are
        in current, and updates self.claimed to include any columns
        for which the updated values in self.totals match the values in
        targets. The function returns the list of newly claimed
        columns, in increasing order.
        Note that
        * self.claimed must be in increasing order after being updated
        * the length of self.totals is not changed by update_totals
        * if current is empty, then the fields are not updated,
            and the empty list is returned.

        Effects:
           updates self.totals using current
           updates self.claimed using targets

        update_totals: Player (dictof DiceTotal Nat) (dictof DiceTotal Nat)
                         -> (listof DiceTotal)
        Requires:
           len(current) <= 3
           len(targets) == 11
           sorted(self.totals.keys()) == sorted(current.keys())
           The new value associated with c in current will always
              be greater than its value in self.totals.
           Values of targets are greater than or equal to associated
             values in current.

        Example:
           Suppose p has name "Lucy", with totals as
            {3:4, 5:2, 6:0, 7:4, 8:7, 10:1, 12:0},
            and claimed [2,11], then after calling
           p.update_totals({7:11, 12:3, 5:3},
             {2:3, 3:5, 4:7, 5:9, 6:11, 7:13,
              8:11, 9:9, 10:7, 11:5, 12:3}) => [12]
           p.totals is {3:4, 5:3, 6:0, 7:11, 8:7, 10:1, 12:3},
             and p.claimed = [2,11,12]
        '''

        new = []

        for i in current:

            self.totals[i] = current[i]
            if current[i] == targets[i]:
                new.append(i)
                self.claimed.append(i)

        self.claimed.sort()

        return sorted(new)

class Game:
    '''
    functions and date for Game

    fields:
        players (listof Player)
            [list of Player objects, in the order of play,
               first player at position 0]
        curr_player (Nat)
            [position of the current player in players list]
        claimed (dictof DiceTotal Str)
            [dictionary keys are between 2 and 12, dictionary
              values are the names of players who have
              claimed that total]
    '''

    # Constant for the Game class
    targets = {2: 3, 3: 5, 4: 7, 5: 9, 6: 11, 7: 13, 8: 11, 9: 9, 10: 7, 11: 5, 12: 3}

    def __init__(self, names):  # DO NOT CHANGE
        '''
        Initializes self.players to be a list of Player objects
        created using the Player class for each name,
        self.claimed to be empty, and self.curr_player to be 0.
        The order in names corresponds to the order in which the players
        take turns, and the player with the first turn when play starts
        is in position 0 of the list.

        Effects: Mutates Game

        __init__: Game (listof Str) -> None
        '''
        self.players = []
        for i in range(len(names)):
            self.players.append(Player(names[i]))
        self.claimed = {}
        self.curr_player = 0

    def __repr__(self):  # DO NOT CHANGE
        '''
        Returns a string representation of the Game

        __repr__: Game -> Str
        '''
        s = ""
        for p in self.players:
            s += str(p) + "\n"
        s += "Claimed: " + str(self.claimed) + "\n"
        s += "Current Player: " + str(self.curr_player)
        return s

    def __eq__(self, other):  # DO NOT CHANGE
        '''
        Returns True if self is identical to other, and False otherwise.

        __eq__ Game Any -> Bool
        '''
        return isinstance(other, Game) and \
               (self.players == other.players) and \
               (self.claimed == other.claimed) and \
               (self.curr_player == other.curr_player)

    def print_board(self):
        '''
        Prints out the board according to the guidelines explained in the
        assignment description

        Effects:
            Prints the board represented by self

        print_board: Game -> None
        '''
        max_target = 13
        row_length = 67
        num_spaces = 27
        spaces = num_spaces * " "
        title = "C A N ' T   S T O P"
        bar = "-" * row_length
        first_column = 2
        last_column = 12
        block = 5
        blank = "     |"

        # beginning of header - do not change
        print(spaces + title + spaces)
        print(bar)
        line = "|"
        for i in range(first_column, last_column + 1):
            line += str(i).ljust(block) + "|"
        print(line)
        print(bar)
        # end of header

        ## Add code for middle of board
        ## first 3 rows
        for x in range(1, 4):
            line = '|'
            for i in range(first_column, last_column + 1):

                if i in self.claimed:
                    line += "".ljust(block) + "|"

                else:
                    lst = []
                    for j in range(len(self.players)):
                        if i in self.players[j].totals and self.players[j].totals[i] == x:
                            lst.append(self.players[j].name[0])
                    if lst == []:
                        line += str(x).ljust(block) + "|"
                    else:
                        lst.sort()
                        line += "".join(lst).ljust(block) + '|'

            print(line)

        for x in range(4, 6):
            line = '|'
            line += "".ljust(block) + "|"
            for i in range(first_column + 1, last_column + 1 - 1):

                if i in self.claimed:
                    line += "".ljust(block) + "|"

                else:
                    lst = []
                    for j in range(len(self.players)):
                        if i in self.players[j].totals and self.players[j].totals[i] == x:
                            lst.append(self.players[j].name[0])
                    if lst == []:
                        line += str(x).ljust(block) + "|"
                    else:
                        lst.sort()
                        line += "".join(lst).ljust(block) + '|'

            line += "".ljust(block) + "|"
            print(line)

        for x in range(6, 8):
            line = '|'
            line += ("".ljust(block) + "|") * 2
            for i in range(first_column + 2, last_column + 1 - 2):

                if i in self.claimed:
                    line += "".ljust(block) + "|"

                else:
                    lst = []
                    for j in range(len(self.players)):
                        if i in self.players[j].totals and self.players[j].totals[i] == x:
                            lst.append(self.players[j].name[0])
                    if lst == []:
                        line += str(x).ljust(block) + "|"
                    else:
                        lst.sort()
                        line += "".join(lst).ljust(block) + '|'

            line += ("".ljust(block) + "|") * 2
            print(line)

        for x in range(8, 10):
            line = '|'
            line += ("".ljust(block) + "|") * 3
            for i in range(first_column + 3, last_column + 1 - 3):

                if i in self.claimed:
                    line += "".ljust(block) + "|"

                else:
                    lst = []
                    for j in range(len(self.players)):
                        if i in self.players[j].totals and self.players[j].totals[i] == x:
                            lst.append(self.players[j].name[0])
                    if lst == []:
                        line += str(x).ljust(block) + "|"
                    else:
                        lst.sort()
                        line += "".join(lst).ljust(block) + '|'

            line += ("".ljust(block) + "|") * 3
            print(line)

        for x in range(10, 12):
            line = '|'
            line += ("".ljust(block) + "|") * 4
            for i in range(first_column + 4, last_column + 1 - 4):

                if i in self.claimed:
                    line += "".ljust(block) + "|"

                else:
                    lst = []
                    for j in range(len(self.players)):
                        if i in self.players[j].totals and self.players[j].totals[i] == x:
                            lst.append(self.players[j].name[0])
                    if lst == []:
                        line += str(x).ljust(block) + "|"
                    else:
                        lst.sort()
                        line += "".join(lst).ljust(block) + '|'

            line += ("".ljust(block) + "|") * 4
            print(line)

        for x in range(12, 14):
            line = '|'
            line += ("".ljust(block) + "|") * 5
            for i in range(first_column + 5, last_column + 1 - 5):

                if i in self.claimed:
                    line += "".ljust(block) + "|"

                else:
                    lst = []
                    for j in range(len(self.players)):
                        if i in self.players[j].totals and self.players[j].totals[i] == x:
                            lst.append(self.players[j].name[0])
                    if lst == []:
                        line += str(x).ljust(block) + "|"
                    else:
                        lst.sort()
                        line += "".join(lst).ljust(block) + '|'

            line += ("".ljust(block) + "|") * 5
            print(line)

        print(bar)
        # beginning of footer - do not change
        line = "|"
        for pos in range(first_column, last_column + 1):
            if pos in self.claimed:
                line += self.claimed[pos][0] + blank[1:]
            else:
                line += blank
        line += " Claimed"
        print(line)
        # end of footer

    def determine_options(self, possibles, current):
        '''
        Returns a dictionary of options for the player to choose to play,
        where the keys are numbers starting from 0, and the values are
        the lists (of length 1 or 2) for the player to choose. The options are
        based on the pairs in possibles, but are limited by which columns are
        claimed (as noted in self.claimed) and the current (active) columns
        for the player. The list of options inside the returned
        dictionary must be created according to the order of the
        values in possibles.

        determine_options:
          Game (listof (list DiceTotal DiceTotal)) (dictof DiceTotal Nat)
             -> (dictof Nat (union (list DiceTotal) (list DiceTotal DiceTotal)))

        Examples:
        *  Suppose poss = [[5,11],[6,10],[7,9]] and
             active = {}, and g.claimed = {11:"Mo"},
             then g.determine_options(poss, active)
               => {0:[5], 1: [6,10], 2:[7,9]}
        * Suppose poss = [[5,11],[6,10],[7,9]] and
             active = {7:5, 4:3}, and g.claimed = {10:"Xi"},
             then g.determine_options(poss, active)
               => {0:[5], 1:[11], 2:[6], 3:[7,9]}
        * Suppose poss = [[7,9],[8,8]] and active = {7:5, 4:3},
             and g.claimed = {},
             then g.determine_options(poss, active)
                    => {0: [7,9], 1:[8,8]}
        * Suppose poss = [[7,9],[8,8]] and active = {2:2, 3:5, 4:1}
             and g.claimed = {},
             then g.determine_options(poss, active) => {}

        '''
        ##YOUR CODE GOES HERE
        lst = []
        final = {}

        for i in possibles:
            if len(current) <= 1:
                lst2 = [j for j in i if j not in self.claimed]
                lst += [lst2]

            elif len(current) == 2:
                lst2 = [j for j in i if j not in self.claimed]
                if len(lst2) == 2:
                    if lst2[0] in current or lst2[1] in current:
                        lst += [lst2]
                    elif lst2[0] == lst2[1]:
                        lst += [lst2]
                    else:
                        lst += [[lst2[0]]]
                        lst += [[lst2[1]]]

                elif len(lst2) == 1:
                    lst += [[lst2[0]]]

            else:
                lst2 = [j for j in i if j not in self.claimed]
                if len(lst2) == 2:
                    if lst2[0] in current and lst2[1] in current:
                        lst += [lst2]
                    elif lst2[0] in current:
                        lst += [[lst2[0]]]
                    elif lst2[1] in current:
                        lst += [[lst2[1]]]

                else:
                    if lst2[0] in active:
                        lst += [[lst2[0]]]

        for i in range(len(lst)):
            final[i] = lst[i]

        return final

    def save_game(self, file_name):
        '''
        Saves the current game status to the file called file_name:
        * the information about each player is written on three lines:
           - the first line contains the player's name
           - the second line is their current positions on the board,
           in the form t:p, where t is the column number between 2 and 12,
           and p is the location in that column, where all column positions
           are on the same line and separated by a space, and the column
           positions are in increasing order
           - the third line is the column numbers claimed
              by that player, in increasing order.
           If the player has not claimed any columns,
            this line contains 0 instead.
        * the players appear in the order of their turns:
             first player saved rolls the dice next,
             then the player after them, etc.

        Effects: Writes game status to file_name

        save_game: Game Str -> None

        '''
        n = self.curr_player

        fout = open(file_name, "w")

        for i in range(len(self.players)):
            s = ""
            for j in self.players[(i + n) % (len(self.players))].totals:
                if j not in self.claimed:
                    s += str(j) + ":" + str(self.players[(i + n) % (len(self.players))].totals[j]) + " "

            z = ""
            for j in self.claimed:
                if self.claimed[j] == (self.players[(i + n) % (len(self.players))].name):
                    z += str(j) + " "

            if z == "":
                z += "0 "

            fout.write(str(self.players[(i + n) % (len(self.players))].name) + "\n")
            fout.write(s + "\n")
            fout.write(z + "\n")

        fout.close()

    def take_turn(self, debug):  ## DO NOT CHANGE
        '''
        plays one turn of the game for the current player

        Effects:
        * prints messages about the game
        * reads in game play information
        * mutates information about this Game and
          about the players playing the game
        '''

        turn_message = "{0}, it is now your turn"  # use format to add current player's name
        menu_prompt = "{0}: Enter (B or b) to see the board, (S or s) to suspend and save the game, anything else to roll dice: "  # Use format to add player's name
        roll_message = "{0}: Your roll was {1},{2},{3},{4}"  # use format to current player's name, and to add dice values
        pairs_message = "{0}: Combinations include: {1}"  # use format to add player name and value total combinations (result from Dice.pairs)
        no_options_message = '{0}: You cannot play. Your turn is over.'  # use format to add player name
        option_message = "Enter {0} to play {1}"  # Use format to add option number and option list
        choice_message = "{0}: Enter your choice now: "  # Use format to add player name
        current_begin = "Currently active for {0}: "  # Use format to add player name
        current_summary = "{0} (position {1} of {2}). "  # Use format to add active column number, position in column, and column length
        again_prompt = "{0}: Do you want to roll again? enter Y for Yes, Anything else for No. "  # Use format to enter player name
        yes = ['y', 'yes']
        game_won = '{0} has won the game.'  # Use format to add player name
        column_claimed = '{0} has just claimed {1}'  # Use format to add player name and column just claimed
        save_game_prompt = "{0} Enter name of file to save current game to:"  # Use format to add player's name
        save_game_confirmation = "Game saved to {0}"  # Use format to add save file name

        n = self.players[self.curr_player].name
        print(turn_message.format(n))
        ans = input(menu_prompt.format(n))
        while ans.lower() == "b":
            self.print_board()
            print(turn_message.format(n))
            ans = input(menu_prompt.format(n))

        if ans.lower() == "s":
            file_n = input(save_game_prompt.format(n))
            self.save_game(file_n)
            print(save_game_confirmation.format(file_n))
            return True

        again = True
        current = {}  # Initialize  active columns dictionary to be empty for current player
        while again:
            d1 = roll(debug)
            d2 = roll(debug)
            d3 = roll(debug)
            d4 = roll(debug)
            print(roll_message.format(n, d1, d2, d3, d4))
            possibles = pairs(d1, d2, d3, d4)
            print(pairs_message.format(n, possibles))

            choices_dir = self.determine_options(possibles, current)

            num_options = len(choices_dir)
            if num_options == 0:
                print(no_options_message.format(n))
                current = {}
                # do not adjust totals from current
                again = False
            else:
                for i in range(num_options):
                    print(option_message.format(i, choices_dir[i]))

                choice = input(choice_message.format(n))
                while not (choice.isdigit()) or (int(choice) < 0 or int(choice) >= num_options):
                    choice = input("Invalid choice. " + choice_message.format(n))

                ch = int(choice)
                will_play = choices_dir[ch]
                for d in will_play:
                    if d in current:
                        current[d] += 1
                    else:
                        current[d] = self.players[self.curr_player].totals[d] + 1
                    current[d] = min(current[d], self.targets[d])

                str_current = current_begin.format(n)
                curr_cols = list(current.keys())
                curr_cols.sort()
                for t in curr_cols:
                    str_current += current_summary.format(t, current[t], self.targets[t])
                print(str_current)

                answer = input(again_prompt.format(n))
                again = (answer.lower() in yes)

        just_claimed = self.players[self.curr_player].update_totals(current, self.targets)

        for loc in just_claimed:
            print(column_claimed.format(n, loc))
            self.claimed[loc] = n
            for p in self.players:
                p.totals.pop(loc)

        current = {}
        if len(self.players[self.curr_player].claimed) >= 3:
            print(game_won.format(n))
            return True
        else:
            self.curr_player = (self.curr_player + 1) % len(self.players)
            return False

def load_game(file_name):
    '''
    Reads the information about a suspended game from file_name, and returns a Game
    object created from that information, setting all fields in Game and for each
    Player.

    Effects: Reads game information from file_name

    load_game: Str -> Game
    Requires: file_name corresponds to a valid Can't Stop save game file.
    '''
    fin = open(file_name)
    txt = fin.readlines()
    fin.close

    names = []

    i = 0

    while i < len(txt):
        name = txt[i].replace("\n", "")

        names.append(name)

        i += 3

    g = Game(names)

    for i in range(len(g.players)):
        g.players[i].totals = {}

        txt2 = txt[3 * i + 1].replace("\n", "")

        a = txt2.split(" ")

        a = [i for i in a if i != ""]

        for x in range(len(a)):
            a[x] = a[x].split(":")

        for j in range(len(a)):
            g.players[i].totals[int(a[j][0])] = int(a[j][1])

        txt3 = txt[3 * i + 2].replace("\n", "")

        a = txt3.split(" ")

        a = [i for i in a if i != ""]

        for r in range(len(a)):
            if a[r] != "0":
                g.players[i].claimed.append(int(a[r]))
                g.claimed[int(a[r])] = g.players[i].name

    return g


def play_game():
    '''
    Sets up the game play by asking questions, and then calls take_turn for
    each player until the game is over (either by a player winning the game or
    saving it to a file).

    Effects:
      * prints messages and reads input to set up the game and dice rolls
      * may read from a file to set up the game
      * may save to a file

    play_game: None -> None
    '''

    welcome = "WELCOME TO CAN'T STOP"
    debug_prompt = "Enter D for debug mode, anything else for random play. "
    debug_yes = ['d', 'D']
    debug_message = "Playing debug mode - be prepared to enter all die values."
    game_prompt = "Enter R to re-load a game, Anything else for a new game. "
    reload_yes = ['r', 'R']
    name_message1 = "You will be asked for the number of players and each player's name."
    name_message2 = "Each player's name must start with a different letter."
    name_message3 = "Player names will be entered individually, and each must start with a different letter."
    name_message4 = "The order of play will correspond to the order in which they are entered."
    name_message5_prompt = "Enter player name (first letter must be unique): "
    name_message6_prompt = 'Each player name must start with a different letter. Enter a different name. '
    num_player_prompt = "Enter the number of players [2-4]: "
    invalid_num_player = "You entered '{0}' which is not acceptable."  # Use format to add what was entered for number
    load_file_prompt = "Enter filename to load game from: "

    ## YOUR CODE GOES HERE TO CREATE THE GAME (use the above strings for prompts and information).
    ## Be sure to create a Game called g and to assign a value to Boolean variable debug.
    print(welcome)
    x = input(debug_prompt)
    if x in debug_yes:
        debug = True
        print(debug_message)
    else:
        debug = False
    x = input(game_prompt)
    if x in reload_yes:
        y = input(load_file_prompt)
        g = load_game(y)

    else:
        print(name_message1)
        print(name_message2)
        go = True
        while go:
            num = input(num_player_prompt)
            if num not in ["2", "3", "4"]:
                print(invalid_num_player.format(num))
            else:
                go = False

        print(name_message3)
        print(name_message4)

        lst = []
        lon = []

        for i in range(int(num)):
            go = True
            name = input(name_message5_prompt)
            while go:
                if name[0] not in lst:
                    lst.append(name[0].upper())
                    lst.append(name[0].lower())
                    lon.append(name)
                    go = False
                else:
                    name = input(name_message6_prompt)
        g = Game(lon)

    ## THE FOLLOWING CODE ASSUMES
    ## * you have created a Game object called g, with appropriate field values
    ## * you have assigned a True or False value to a variable called debug corresponding to whether
    ##   or not you are playing in debug mode.
    over = False
    while not over:
        over = g.take_turn(debug)
    ## Do NOT add any additional code below this loop.


## basis for these tests.

play_game()