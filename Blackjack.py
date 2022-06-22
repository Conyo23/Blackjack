# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:26:16 2022

@author: c_con
"""

import random
import math
suits = ('Hearts','Diamonds','Clubs','Spades')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King', 'Ace')
values  ={'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,
          'King':10, 'Ace':1}

class Card:
    def __init__(self,suits, rank):
        self.suits = suits
        self.rank = rank
        self.value = values[rank]
    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    def __init__(self):
        self.all_cards = []
        
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                
                self.all_cards.append(created_card)
    def shuffle(self):
        random.shuffle(self.all_cards)
                
    def hit_me(self):
        return self.all_cards.pop()

class Players:
    def __init__(self,name):
        self.name=name
        self.all_cards = []
        
    def remove_all(self):
        self.all_cards.clear()
    def remove_one(self):
        self.all_cards.pop(-1)
    
    def add_cards(self,new_cards):
        if type(new_cards) == type([]):
            self.all_cards.extend(new_cards)
        else:
            self.all_cards.append(new_cards)
    def __str__(self):   
        return f'Player {self.name} has {len(self.all_cards)} cards.'
init_money = 100

def deckstuff():
    global new_deck
    new_deck = Deck()
    new_deck.shuffle()
    global Player
    Player=Players("Player")
    global Dealer
    Dealer=Players("Dealer")

def initialize(init_money): #start screen
    if init_money > 0:
        print(f"You have ${init_money}\nWould you like to play?")
        response = input("Yes or No: " )
        if yes_or_no(response) == 1:
            print("Let's Begin! \n")
            deckstuff()
            Start(Betting(init_money),init_money)
        elif yes_or_no(response) == 0:
            print("Goodbye then")
        elif yes_or_no(response) == 2:
            initialize(init_money)
    else:
        print("Sorry, I can't give credit.\nCome back when you're a little more mmmmmm richer!\n")
def Betting(init_money):
    Bet = input("How much would you like to bet?\n")
    if check_user_input(Bet):
        Bet=float(Bet)
        if Bet <= init_money and Bet > 0 :
            return Bet
        elif Bet>init_money and Bet > 0 :
            print("Too high of a bet! Try again.\n")
            Betting(init_money)
        elif Bet <= 0:
            print("Please type a positive number greater than 0 for your bet.\n")
            Betting(init_money)
    else:
        print("Please type a number.\n")
        Betting(init_money)


def Start(Bet, init_money):
    global player_total
    player_total=0
    global dealer_total
    dealer_total=0
    player_first_card=new_deck.hit_me()
    Player.add_cards(player_first_card)
    dealer_first_card=new_deck.hit_me()
    Dealer.add_cards(dealer_first_card)
    player_second_card=new_deck.hit_me()
    Player.add_cards(player_second_card)
    dealer_second_card=new_deck.hit_me()
    Dealer.add_cards(dealer_second_card)
    player_total=player_first_card.value + player_second_card.value
    dealer_total=dealer_first_card.value
    Init_Play(Bet, init_money, 0)

def Init_Play(bet,init_money, insurance):
    global Split_Player
    global player_total
    global dealer_total
    global head_down
    head_down = False
    Split_Player = Players("Split")
    print(f"Your cards are the {Player.all_cards[0].rank} of {Player.all_cards[0].suits} and the {Player.all_cards[1].rank} of {Player.all_cards[1].suits}\nThe Dealer's head-up card is the {Dealer.all_cards[0].rank} of {Dealer.all_cards[0].suits}.\n")
    outcome=3
    insurance_bet=0
    split_hands = False
    split_hand_one = 3
    split_hand_two = 3
    
    #If the Dealer has an ace, you may make an insurance for a small reward. They also will tell you what their head-down card is.
    if Dealer.all_cards[0].rank == "Ace" and init_money > 0 and insurance ==0:
        insurance = 1
        Init_Play(bet,init_money,insurance)
    elif insurance == 1:
        insurance_claim=input("Would you like to make an insurance bet?\n")
        if yes_or_no(insurance_claim)==1:
            insurance_bet = input("How much would you like to bet as insurance? (You can only bet up to half of your original bet)\n")
            if check_user_input(insurance_bet):
                insurance_bet=float(insurance_bet)
                if insurance_bet <= init_money and insurance_bet > 0 and insurance_bet <=0.5*bet:
                    init_money -=insurance_bet
                    dealer_total +=10+Dealer.all_cards[1].value
                    print(f"The Dealer's second card is the {Dealer.all_cards[1].rank} of {Dealer.all_cards[1].suits}.\n")
                    if dealer_total == 21:
                        print(f"Your insurance claim has been accepted.\n Your total money is {init_money+insurance_bet*2}.\n")
                        init_money+=insurance_bet*2
                        insurance = 2
                    elif dealer_total <21:
                        print(f"Your insurance claim has been denied!\n Your total money is {init_money}.\n")
                        insurance = 2
                elif insurance_bet>init_money and bet > 0 or insurance_bet>0.5*bet:
                    print("Too high of a bet! Try again\n")
                    Init_Play(bet,init_money, 1)
                elif insurance_bet <= 0:
                    print("Please type a positive number greater than 0 for your bet.\n")
                    Init_Play(bet,init_money, 1)
            else:
                print("Please type a number.\n")
                Init_Play(bet,init_money,1)
        elif yes_or_no(insurance_claim) == 0:
            print("Let's continue then!\n")
            insurance = 2
        elif yes_or_no(insurance_claim) == 2:
            Init_Play(bet,init_money,1)
    
    elif Dealer.all_cards[0].value == 10:
        print(f"The Dealer's second card is the {Dealer.all_cards[1].rank} of {Dealer.all_cards[1].suits}.\n")
        dealer_total += Dealer.all_cards[1].value
        head_down=True
        outcome = Blackjack(Player.all_cards[0].rank,Player.all_cards[1].rank, False) 
            
    #if the Player does not have a split-card
    elif Player.all_cards[0].rank != Player.all_cards[1].rank:
        #check to see if they have an ace in their first two cards
        if natural_ace():
            player_total += 10
            outcome = Blackjack(Player.all_cards[0].rank,Player.all_cards[1].rank,False)
        elif player_total >=9 and player_total <12 and bet*2<=init_money:
            play(bet,init_money, True)
        elif Dealer.all_cards[0].value == 10:
            print(f"The Dealer's second card is the {Dealer.all_cards[1].rank} of {Dealer.all_cards[1].suits}.\n")
            dealer_total += Dealer.all_cards[1].value
            outcome = Blackjack(Player.all_cards[0].rank,Player.all_cards[1].rank, False)
 

    
    #if the Player has the same cards and they are not aces
    elif Player.all_cards[0].rank == Player.all_cards[1].rank !="Ace" and bet*2 <=init_money:
        split_hands = split(bet, init_money)
        if split_hands:
            Split_Player.add_cards(Player.add_cards[1])
            Player.all_cards.remove_one()
            Split_Hands(3,3,bet,init_money)
        
    
    #if the Player has split aces
    elif Player.all_cards[0].rank == Player.all_cards[1].rank == "Ace" and bet*2 <= init_money:
        split_hands = split(bet, init_money)
        if split_hands:
            init_money-=bet

            Split_Player.add_cards(Player[1])
            Player.remove_one()
            Player.add_cards(new_deck.hit_me())
            Split_Player.add_cards(new_deck.hit_me())
            player_total=Player.all_cards[1].value + 11
            split_player_total=Split_Player.all_cards[1].value + 11

            split_hand_one = Blackjack(Player.all_cards[0].rank,Player.all_cards[1].rank,True)
            split_hand_two = Blackjack(Split_Player.all_cards[0].rank,Split_Player.all_cards[1].rank,True)

            Split_Hands(split_hand_one,split_hand_two, bet, init_money)

    if outcome == 3:
        play(bet,init_money, False)
    elif outcome == 2:
        print(f"Tie. Your money will be returned. Your total money is {init_money}.\n")
        initialize(init_money)
    elif outcome == 1:
        bet *= 2.5
        print(f"You win! Your total money is {bet+init_money}.\n")
        initialize(bet+init_money)
    elif outcome == 0:
        print(f"You lost! Your total money is {init_money-bet}.\n")
        initialize(init_money-bet)

#Of the first two cards, if there is at least one ace, they can make it an eleven. Otherwise we return False
def natural_ace():
    if Player.all_cards[0].rank == 'Ace' and Player.all_cards[1].rank !='Ace' or Player.all_cards[0].rank == Player.all_cards[1].rank == 'Ace':
        eleven = input("Would you like to make your ace an eleven?")
        if yes_or_no(eleven) == 1:
            return True
        elif yes_or_no(eleven)==0:
            print("Let's continue then!\n")
            return False
        elif yes_or_no(eleven)==2:
            return natural_ace()
    elif Player.all_cards[0].rank != 'Ace' and Player.all_cards[1].rank =='Ace':
        eleven = input("Would you like to make your ace an eleven?")
        if yes_or_no(eleven) == 1:
            return True
        elif yes_or_no(eleven) == 0:
            print("Let's continue then!\n")
            return False
        elif yes_or_no(eleven) == 2:
            return natural_ace()
    else:
        return False

def split(bet, init_money):
    if init_money >=2* bet:
        split_cards = input("Would you like to split your cards? It will cost an additional bet of the same value.\n")
        if yes_or_no(split_cards) == 1:
            return True
        elif yes_or_no(split_cards) == 0:
            return False
        elif yes_or_no(split_cards) == 2:
            return split(bet, init_money)
    else:
        return False
    return False

def play(bet,init_money, double_down):
    global player_total
    global dealer_total
    global head_down
    print(f"Your total card value is {player_total}. The Dealer's total card value is {dealer_total}.\n")
    Hit_me_option=3
    Stand_option=3
    if double_down:
        options = input("Would you like to double-down (increase your bet by double)?\n")
        if yes_or_no(options) == 1 and bet * 2 <=init_money:
            bet *=2
            print(f"Your bet is now {bet}.\n")
            play(bet,init_money, False)
        elif yes_or_no(options)==1 and bet * 2 > init_money:
            print("Too high of a bet!\n")
            play(bet,init_money,True)
        elif yes_or_no(options) == 0:
            play(bet, init_money, False)
        elif yes_or_no(options)==2:
            play(bet, init_money, True)
    else:
        options = input("What would you like to do?\n1) Hit me!   2) Stand   3) Walk-away (you will lose half your bet)\n")
        
        if options =="1":
            Player.add_cards(new_deck.hit_me())
            print(f"Your card drawn is the {Player.all_cards[-1].rank} of {Player.all_cards[-1].suits} and your total value is {player_total+Player.all_cards[-1].value}.\n")
            player_total+=Player.all_cards[-1].value
            Hit_me_option=Blackjack(Player.all_cards[0].rank,Player.all_cards[1].rank,False)
            if Hit_me_option== 1:
                bet *= 2.5
                print(f"You win! Your total money is {bet+init_money}.\n")
                initialize(bet+init_money)
            elif Hit_me_option == 0:
                print(f"You busted! Your total money is {init_money-bet}.\n")
                initialize(init_money-bet)
            elif Hit_me_option == 3 and Player.all_cards[-1].rank=="Ace" and player_total + 10 <=21:
                hit_ace = input("Would you like to make your ace an eleven?\n")
                if yes_or_no(hit_ace) == 1:
                    player_total+=10
                    Player.all_cards[-1].value=11
                play(bet,init_money, double_down)
            elif Hit_me_option == 3 and Player.all_cards[-1].rank != "Ace":
                play(bet,init_money, double_down)
        elif options == "2":
            if head_down == False:
                dealer_total += Dealer.all_cards[1].value
                print(f"The Dealer's head down card is the {Dealer.all_cards[1].rank} of {Dealer.all_cards[1].suits}. The Dealer's total is {dealer_total}.\n")
            Stand_option=Blackjack(Player.all_cards[0].rank,Player.all_cards[1].rank,True)

            if Stand_option == 1:
                bet *= 2.5
                print(f"You win! Your total money is {bet+init_money}.\n")
                initialize(bet+init_money)
            elif Stand_option == 0:
                print(f"You lost! Your total money is {init_money-bet}.\n")
                initialize(init_money-bet)
            elif Stand_option == 2:
                print(f"Tie. Your money will be returned. Your total money is {init_money}.\n")
                initialize(init_money)
        elif options == "3":
            print(f"You must now forfeit half your bet. Your total money is {init_money - 0.5*bet}.\n")
            initialize(init_money-0.5*bet)
        else:
            print("Please type the number choice of the options.\n")
            play(bet,init_money,False)

def Split_Play(bet, init_money, split_hand_one):            
    global player_total
    global split_player_total
    global dealer_total
    global head_down
    options=3
    Hit_me_option=3
    
    
    if split_hand_one != 4:
        print(f"Your total split-card value is {player_total}. The Dealer's total card value is {dealer_total}.\n")
        Hit_me_option=3
        
        options = input("What would you like to do?\n1) Hit me!   2) Stand   3) Walk-away (you will lose half your bet)\n")
        
        if options =="1":
            Player.add_cards(new_deck.hit_me())
            print(f"Your card drawn is the {Player.all_cards[-1].rank} of {Player.all_cards[-1].suits} and your total value is {player_total+Player.all_cards[-1].value}.\n")
            player_total+=Player.all_cards[-1].value
            Hit_me_option=Blackjack(Player.all_cards[0].rank,Player.all_cards[1].rank,False)
            if Hit_me_option== 1:
                Split_Hands(Hit_me_option,3,bet,init_money)
            elif Hit_me_option == 0:
                Split_Hands(Hit_me_option,3,bet,init_money)
            elif Hit_me_option == 3 and Player.all_cards[-1].rank=="Ace" and player_total + 10 <=21:
                hit_ace = input("Would you like to make your ace an eleven?\n")
                if yes_or_no(hit_ace) == 1:
                    player_total+=10
                    Player.all_cards[-1].value=11
                Split_Play(bet,init_money, split_hand_one)
            elif Hit_me_option == 3 and Player.all_cards[-1].rank != "Ace":
                Split_Play(bet,init_money, split_hand_one)
        elif options == "2":
            Split_Hands(4,3,bet,init_money)
        else:
            print("Please type the number choice of the options.\n")
            Split_Play(bet, init_money, split_hand_one)
    else:
        print(f"Your total split-card value is {split_player_total}. The Dealer's total card value is {dealer_total}.\n")
        Hit_me_option=3
        
        options = input("What would you like to do?\n1) Hit me!   2) Stand   3) Walk-away (you will lose half your bet)\n")
        
        if options =="1":
            Split_Player.add_cards(new_deck.hit_me())
            print(f"Your card drawn is the {Split_Player.all_cards[-1].rank} of {Split_Player.all_cards[-1].suits} and your total value is {player_total+Player.all_cards[-1].value}.\n")
            split_player_total+=Split_Player.all_cards[-1].value
            Hit_me_option=Blackjack(Split_Player.all_cards[0].rank,Split_Player.all_cards[1].rank,False)
            if Hit_me_option== 1:
                Split_Hands(Hit_me_option,3,bet,init_money)
            elif Hit_me_option == 0:
                Split_Hands(Hit_me_option,3,bet,init_money)
            elif Hit_me_option == 3 and Split_Player.all_cards[-1].rank=="Ace" and split_player_total + 10 <=21:
                hit_ace = input("Would you like to make your ace an eleven?\n")
                if yes_or_no(hit_ace) == 1:
                    player_total+=10
                    Split_Player.all_cards[-1].value=11
                Split_Play(bet,init_money, split_hand_one)
            elif Hit_me_option == 3 and Split_Player.all_cards[-1].rank != "Ace":
                Split_Play(bet,init_money, split_hand_one)
        elif options == "2":
            Stand_option_hand_one=Blackjack(Player.all_cards[0].rank,Player.all_cards[1].rank,True)
            Stand_option_hand_two=Blackjack(Split_Player.all_cards[0].rank,Split_Player.all_cards[1].rank,True)
            Split_Hands(Stand_option_hand_one,Stand_option_hand_two,bet,init_money)
        else:
            print("Please type the number choice of the options.\n")
            Split_Play(bet, init_money, split_hand_one)
        
def Split_Hands(split_hand_one,split_hand_two,bet,init_money):
    if split_hand_one ==1:
        print(f"You have won through one of your split hands! Your total money is {init_money + 2*bet}.\n")
        init_money+=2*bet
        split_hand_one=4
    elif split_hand_one == 0:
        print(f"Your split hand has lost! Your total money is now {init_money - bet}.\n")
        init_money-=bet
        split_hand_one=4
    elif split_hand_one ==2:
        print(f"Your split hand has tied. Your total money is now {init_money+bet}.\n")
        init_money+=bet
        split_hand_one=4
    elif split_hand_one == 3:
        Split_Play(bet,init_money,split_hand_one)
    if split_hand_two ==1 and split_hand_one==4:
        print(f"You have won through one of your split hands! Your total money is {init_money + 2*bet}.\n")
        init_money+=2*bet
        initialize(init_money)
    elif split_hand_two == 0 and split_hand_one==4:
        print(f"Your other split hand has lost! Your total money is now {init_money - bet}.\n")
        init_money-=bet
        initialize(init_money)
    elif split_hand_two ==2 and split_hand_one==4:
        print(f"Your other split hand has tied. Your total money is now {init_money}.\n")
        initialize(init_money)
    elif split_hand_two == 3 and split_hand_one==4:
        Split_Play(bet,init_money,split_hand_one)
    initialize(init_money)

def Blackjack(card1, card2, stand):
    global dealer_total
    global player_total
    ace_check=0
    ace_marker=0
    for x in Player.all_cards:
        if x.rank=="Ace" and x.value==11:
            ace_check=1
            ace_marker=x
            break;
    
    if player_total == 21 and dealer_total != 21 and (card1 == "Ace" or card2 == "Ace"):
        return 1
    elif player_total == 21 and dealer_total >= 17:
        return 1
    elif stand and dealer_total < 17:
        Dealer.add_cards(new_deck.hit_me())
        dealer_total+=Dealer.all_cards[-1].value
        print(f"The Dealer has drawn a {Dealer.all_cards[-1].rank} of {Dealer.all_cards[-1].suits}. Their total is {dealer_total}.\n")
        return Blackjack(card1,card2, stand)
    elif stand and dealer_total >=17 and dealer_total==player_total:
        return 2
    elif player_total == dealer_total == 21:
        return 2
    elif player_total < dealer_total and not stand and dealer_total<21 and player_total <=21:
        return 3
    elif player_total < dealer_total and dealer_total <=21 and stand:
        return 0
    elif dealer_total == 21 and player_total < 21 and ((Dealer.all_cards[0].rank == "Ace" and Dealer.all_cards[1].value=="10") or (Dealer[1].rank == "Ace" and Dealer[0].value == 10)):
        return 0
        
    elif player_total > 21 and ace_check==0:
        return 0
    elif player_total > 21 and ace_check==1:
        player_total-=10
        Player.all_cards[ace_marker].value = 1
        return 3
    elif dealer_total > 21:
        return 1
    elif player_total > dealer_total and player_total <=21 and stand:
        return 1
    else:
        return 3
    return 3
def check_user_input(input):
    try:
        # Convert it into integer
        
        return True
    except ValueError:
        return False
def yes_or_no(response):
    if response == "Yes" or response == "yes":
        return 1
    elif response == "No" or response =="no":
        return 0
    else:
        print('Please type "yes" or "no"\n')
        return 2

initialize(init_money)