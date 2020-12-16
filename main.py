import table as T

def decorator(char):
    print(char * 15)

def view_table(table):
    decorator('#')
    print('Current table')
    decorator('#')
    for player in table.players:
        decorator('-')
        decorator('*')
        print(f'{player.name} - {player.wallet}')
        if player.hands:
            decorator('-')
            for hand in player.hands:
                print(f'{hand.cards} - {hand.bet} - {hand.value}')
    decorator('-')
    if table.dealer.hands:
        print('Dealer:')
        print (f'{table.dealer.hands[0].cards} - {table.dealer.hands[0].value}')
        decorator('-')

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

def stand(player, hand, table):
    hand.active = False

def hit(player, hand, table):
    take_card(hand, table)

def hand_value(hand):
    for card in hand.cards:
        hand.value += card.value
    if hand.value > 21:
        for card in hand.cards:
            if card.value == 11:
                card.value = 1
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
        hand_value(dealer.hands[0])

def player_move(player,table):
    available_options = ['h','s','d','t']

    decorator('*')
    print (f'Player {player.name} on the move')
    decorator('-')
    for idx, hand in enumerate(player.hands):
        print(f'This is your hand No. {idx + 1}: ')
        decorator('-')
        print(hand.cards)
        print(f'Current bet: {hand.bet}')
        decorator('-')
        while hand.active:
            if not 'd' in available_options:
                available_options.append('d')
            print ('Your options: Hit (H), Split (S), Double Down (D), Stand (T)') #todo dynamically remove unavailable options
            option = ''
            while not option:
                option = input('Your move options: ').lower()
                if option not in available_options:
                    option = ''
                    print ('Invalid entry, try again')
            if option == 'h':
                hit(player,hand,table)
                if 'd' in available_options:
                    available_options.remove('d')
            elif option == 's':
                split(player,hand,table)
            elif option == 'd':
                double(player,hand,table)
            elif option == 't':
                stand(player,hand,table)
            if 's' in available_options:
                available_options.remove('s')
            decorator('-')
            print(hand.cards)
            print(f'Current bet: {hand.bet}')
            decorator('-')
        hand_value(hand)


def endgame(table):
    dealer_value = table.dealer.hands[0].value
    if dealer_value > 21:
        dealer_value = 0
    for player in table.players:
        for hand in player.hands:
            if hand.value > 21:
                hand.bet = 0
            else:
                if hand.value > dealer_value:
                    player.wallet += hand.bet * 2
                elif hand.value == dealer_value:
                    player.wallet += hand.bet
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
    view_table(table)

def main():
    table = T.Table(2)
    names = ('Mates', 'Jura', 'Johny')
    for i in range(3):                      #todo create players
        table.players.append(T.Player(1000, name=names[i]))

    while len(table.deck.deck) > table.cut:
        game(table)
        print(f'cards in deck left - {len(table.deck.deck)}')

main()
    
    

