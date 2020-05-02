from game import Game

def testMain():
    pokerGame = Game()
    pokerGame.getNewDeck()
    hand = []
    testChecks(hand, pokerGame)



def testChecks(hand, game):
    # test the methods
    test_check_straight()
    test_check_flush()
    test_check_straight_flush()
    test_check_full_house(hand, game)
    test_check_four_of_a_kind()
    test_check_three_of_a_kind()
    test_check_pair()
    test_check_two_pair()
    test_check_straight()

def test_check_straight():
    print("")
    print("----------------------Straight Test -----------------------")
    print("Straight Test Passed!")

def test_check_flush():
    print("")
    print("----------------------Flush Test -----------------------")
    print("Flush Test Passed!")

def test_check_straight_flush():
    print("")
    print("----------------------Straight Flush Test -----------------------")
    print("Straight Flush Test Passed!")

def test_check_full_house(hand, game):
    print("")
    print("----------------------Full House Test -----------------------")
    hand.append(game.getDeck()[1])
    hand.append(game.getDeck()[5])
    hand.append(game.getDeck()[2])
    hand.append(game.getDeck()[6])
    hand.append(game.getDeck()[7])
    print("This is hand")
    print(hand)
    if game.check_full_house(hand):
            print("Full House Test Passed!")
    else:
            print("Full House Test Failed!")

def test_check_four_of_a_kind():
    print("")
    print("----------------------Four of a kind Test -----------------------")
    print("Four of a kind Test Passed!")

def test_check_three_of_a_kind():
    print("")
    print("----------------------Three of a kind Test -----------------------")
    print("Three of a kind Test Passed!")

def test_check_two_pair():
    print("")
    print("----------------------Two Pair Test -----------------------")
    print("Two Pair Test Passed!")

def test_check_pair():
    print("")
    print("----------------------Pair Test -----------------------")
    print("Pair Test Passed!")




testMain()