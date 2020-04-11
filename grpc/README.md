# Number guessing game

Simple guessing game implemented as a gRPC server and client.

## gRPC Server

The server respondes to two RPCs:

- StartGame: Starts a new game.
- Guess: Checks a guess against the game's target value.

## CLI client

A very simple CLI starts a game and then prompts the user for guesses until the
correct value has been found.