# CMPE209-RoyalStraight
Network Security Poker Game on the Internet

## Server operations

- Manage users/keys
- Manage game state (current bet, whose turn is it, what operations are legal)
- Draw cards (generate entropy)

## Client operations

- Get state on a regular basis (need to know when it's your turn)
- Provide actions/decisions
- Understand mechanisms, what options are available (this could also be explicitly provided by the server: "you can fold or call")
- Manage user data including pubkey
- Be able to encrypt/decrypt using pubkey and session key.

## Attributes

- UserId: Unique username
- PublicKey: User's public key. Required to create a username.
- SessionKey: Unique per-user, per-game session key used to encrypt bet operations.

## Crypto sources

- Pycryptodome https://pycryptodome.readthedocs.io/en/latest/index.html
  - Can generate RSA keys / do AES encryption/decryption
- Requests SSL client cert: https://requests.readthedocs.io/en/master/api/#requests.request
  - See "cert" parameter. You can generate an SSL cert on the client (With pycryptodome, or openssl) and provide it as an argument. Seems like it may be hard to enforce this with flask, but maybe it's an option for transporting the certificate to the server.

## Classes to implement

### User `/users/<user_id>`
- `GET` Get user by ID
- `POST` Register user
  - Error if user already exists
- (Optional?) `PUT` Update pubkey

### TableIndex `/tables`
  - `POST` Join Table / Get session key. Session key encrypted with user's pubkey.
  - `DELETE` Leave Table / Delete session key
  - (Optional) `GET` Get current table state / session key, if necessary. Client should store this anyway.
  - (Optional) make `GET /tables` list open tables and users at each, and give user option to pick.

### Game `/game/<table_id>` (All transactions authenticated with session key)
- `GET` Current state
  - Game states
    - Waiting for players (game not started)
    - Other's turn
    - Your turn
  - History (provide last transaction ID to get all transactions since then)
    - 4: "user5 joins the game"
    - 84: "User3 raises"
    - 85: "User4 calls"
    - 101: "User1 leaves the table"
  - Your Balance
  - Cards in play
    - Your cards
    - Flop
    - Turn
    - River
  - Current bet
  - Total money in pot
  - User ID list/state
    - big/small blind
    - in/out (i.e. have they folded)
- `POST` Interact
  - Check
  - Bet `amount`
  - Raise `amount`
  - Call 
  - Fold