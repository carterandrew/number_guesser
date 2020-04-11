"""Simple CLI client for the NumberGuesser service."""

from __future__ import print_function

import sys

import grpc

import number_guesser_pb2
import number_guesser_pb2_grpc

_NUMBER_GUESSER_SPEC = 'localhost:20308'
_DIFFICULTY = number_guesser_pb2.DIFFICULTY_EASY


def main():
  with grpc.insecure_channel(_NUMBER_GUESSER_SPEC) as channel:
    stub = number_guesser_pb2_grpc.NumberGuesserStub(channel)
    
    response = stub.StartGame(number_guesser_pb2.StartGameRequest(
        difficulty=_DIFFICULTY))
    game_id = response.game_id
    lower = response.lower
    upper = response.upper
    print("Game id: %s started!\nYou are guessing in the range: %d to %d" % (
        str(game_id), lower, upper))
    try:
      while True:
        guess = int(input('Make your guess: '))
        request = number_guesser_pb2.GuessRequest(game_id=game_id, guess=guess)
        response = stub.Guess(request)
        if response.result == number_guesser_pb2.RESULT_CORRECT:
          print('Woohoo! You guessed correctly!')
          sys.exit(0)
        elif response.result == number_guesser_pb2.RESULT_LOW:
          print('WRONG! Your guess was too LOW. Please try again.')
        elif response.result == number_guesser_pb2.RESULT_HIGH:
          print('WRONG! Your guess was too HIGH. Please try again.')
    except KeyboardInterrupt:
      sys.exit(0)


if __name__ == '__main__':
  main()