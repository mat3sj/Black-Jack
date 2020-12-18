import table as T

def decorator(char):
    print(char * 15)

def show_hand(hand):
    evaluate_hand(hand)
    print(f'{hand.cards} - {hand.value}')
    print(f'Current bet: {hand.bet}')
    decorator('-')

def show_dealer(table):
    print('Dealer:')
    evaluate_hand(table.dealer.hands[0])
    print(f'{table.dealer.hands[0].cards} - {table.dealer.hands[0].value}')
    decorator('-')

def view_table(table):
    decorator('#')
    print('Current table')
    decorator('#')
    for player in table.players:
        decorator('*')
        print(f'{player.name} - {player.wallet}')
        if player.hands:
            decorator('-')
            for hand in player.hands:
                show_hand(hand)
    show_dealer(table)

def take_card(hand, table):
    hand.cards.append(table.deck.deck.pop(0))

def first_phase(table):
    for player in table.players:
        base_bet = 100
        player.wallet -= base_bet
        player.hands.append(T.Hand(base_bet))
        player.hands[0].cards.append(table.deck.deck.pop(0))
    table.dealer.hands.append(T.Hand(0))
    table.dealer.hands[0].cards.append(table.deck.deck.pop(0))
    for player in table.players:
        player.hands[0].cards.append(table.deck.deck.pop(0))

def split(player, hand, table):
    current_bet = hand.bet
    player.wallet -= current_bet
    player.hands.append(T.Hand(current_bet))
    player.hands[1].cards.append(player.hands[0].cards.pop())
    for hand in player.hands:
        take_card(hand,table)

def double(player, hand, table):
    current_bet = hand.bet
    player.wallet -= current_bet
    hand.bet *= 2
    take_card(hand, table)
    hand.active = False

def stand(hand):
    hand.active = False

def hit(hand, table):
    take_card(hand, table)

def evaluate_hand(hand):
    hand.value = 0
    for card in hand.cards:
        hand.value += card.value
    if hand.value > 21:
        for card in hand.cards:
            if card.value == 11:
                card.value = 1
                break
    hand.value = 0
    for card in hand.cards:
        hand.value += card.value
    if hand.value > 21:
        hand.active = False
        hand.bet = 0

def dealers_move(table):
    dealer = table.dealer
    while dealer.hands[0].value < 17:
        take_card(dealer.hands[0],table)
        evaluate_hand(dealer.hands[0])

def black_jack(player, hand):
    evaluate_hand(hand)
    if hand.value == 21 and len(hand.cards) == 2:
        hand.active = False
        player.wallet += int(hand.bet * 1.5)
        hand.black_jack = True
        return True
    else:
        return False



def player_move(player,table):
    available_options = ['h','s','d','t']

    decorator('*')
    print (f'Player {player.name} on the move - {player.wallet}')
    decorator('-')
    for idx, hand in enumerate(player.hands):
        print(f'This is your hand No. {idx + 1}: ')
        decorator('-')
        if 'd' not in available_options:
            available_options.append('d')
        while hand.active:
            show_hand(hand)
            if black_jack(player, hand):
                continue

            option_text = 'Your options: '
            options_dic = {'h':'Hit (H),', 's':'Split (S),', 'd':'Double Down (D),', 't':'Stand (T),'}
            for option in available_options:
                option_text += options_dic[option]

            print (option_text[:-1])
            option = ''
            while not option:
                option = input('Your move options: ').lower()
                if option not in available_options:
                    option = ''
                    print ('Invalid entry, try again')
            if option == 'h':
                hit(hand,table)
                if 'd' in available_options:
                    available_options.remove('d')
                if 's' in available_options:
                    available_options.remove('s')
            elif option == 's':
                split(player,hand,table)
                available_options.remove('s')
            elif option == 'd':
                double(player,hand,table)
                show_hand(hand)
            elif option == 't':
                stand(hand)
                show_hand(hand)
        evaluate_hand(hand)


def endgame(table):
    dealer_value = table.dealer.hands[0].value
    if dealer_value > 21:
        dealer_value = 0
    for player in table.players:
        for idx, hand in enumerate(player.hands):
            if hand.value > 21:
                print(f'{player.name} - hand No. {idx + 1} - {hand.value} - lost')
            else:
                if hand.black_jack:
                    print(f'{player.name} - hand No. {idx + 1} - Black Jack')
                    pass
                else:
                    if hand.value > dealer_value:
                        player.wallet += hand.bet * 2
                        print(f'{player.name} - hand No. {idx + 1} - {hand.value} - win')
                    elif hand.value == dealer_value:
                        player.wallet += hand.bet
                        print(f'{player.name} - hand No. {idx + 1} - {hand.value} - draw')
                    else:
                        print(f'{player.name} - hand No. {idx + 1} - {hand.value} - lost')
        player.hands = []
    table.dealer.hands = []




def game(table):
    first_phase(table)
    view_table(table)
    for player in table.players:
        player_move(player,table)
    dealers_move(table)
    view_table(table)
    endgame(table)
    print('End of Turn')
    # view_table(table)

def main():
    table = T.Table(2)
    names = ('Mates', 'Jura', 'Johny', 'Honni', 'Fanda', 'Jeff')
    for i in range(2):                      #todo create players
        table.players.append(T.Player(1000, name=names[i]))

    while len(table.deck.deck) > table.cut:
        game(table)
        print(f'cards in deck left - {len(table.deck.deck)}')

main()
    
    

