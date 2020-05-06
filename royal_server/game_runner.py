from time import sleep

import sys
sys.path.append("..")
from poker_classes import (
    app,
    db,
    User,
    Game,
    Player,
    Update,
)
from encryption import (
    generateKeys,
    generateSessionKey,
    generateB64SessionKey,
    rsa_encrypt,
    ASCII_to_binary as a2b,
    binary_to_ASCII as b2a
    )

if __name__ == "__main__":

    # 1. Drop all the tables

    db.drop_all()

    # 2. (Re)create the database tables.
    db.create_all()

    # Create the game
    poker = Game()
    db.session.add(poker)
    db.session.commit()


    #######################################
    # Comment out these lines if you don't
    # want users precreated on the server.
    #######################################

    # Add users
    usernames = [
        # 'wearnold',
        'ksbains',
        'junlan66',
        'smannan']
    users = []
    for un in usernames:
        # Try and read the file for speed
        try:
            with open('pubkey_%s' % un, 'rb') as f:
                pubkey = f.read()
                b64_pubkey = b2a(pubkey)
        except:
            prikey, pubkey = generateKeys()
            with open('prikey_%s' % un, 'wb') as f:
                f.write(prikey)
            with open('pubkey_%s' % un, 'wb') as f:
                f.write(pubkey)
            b64_pubkey = b2a(pubkey)
        user_dict = {
            'username':un,
            'pubkey':b64_pubkey
        }
        user = User(**user_dict)
        db.session.add(user)
        users.append(user)
    db.session.commit()
    
    for user in users:
        print(user.username)
        print(poker.id)
        player = Player(username = user.username, gameid = poker.id)
        db.session.add(player)
        db.session.commit()
        poker.addPlayer(player)
        db.session.commit()
    
    #########################################

    waiting = True
    while waiting:
        # TODO: multiple games
        game_id = 1
        result = db.session.query(Player).filter_by(gameid=game_id).all()
        if len(result) == 4:
            waiting = False
        else:
            sleep(1)
            print("%d players in lobby, waiting..." % len(result))
        
        # GET Check number of players in the game

    # #start the game
    poker.start()
