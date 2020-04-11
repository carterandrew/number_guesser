"""Number Guesser gRPC server."""


from concurrent import futures
import time
import threading

import grpc

import guessing_game
import number_guesser_pb2
import number_guesser_pb2_grpc


_EXPIRATION = 600  # time in seconds a game will remain in memory.
_DIFFICULTIES = {
  number_guesser_pb2.DIFFICULTY_EASY: 100,
  number_guesser_pb2.DIFFICULTY_MEDIUM: 100000,
  number_guesser_pb2.DIFFICULTY_HARD: None,
}


class NumberGuesser(number_guesser_pb2_grpc.NumberGuesserServicer):
  
  def __init__(self, games=None):
    super(NumberGuesser, self).__init__()
    if games is None:
      games = {}
    self._games = games
    self._expiration_worker = threading.Thread(target = self._expire_games)
    self._expiration_worker.daemon = True
    self._expiration_worker.start()
    
  def _expire_games(self):
    while True:
      time.sleep(10)
      now = time.time()
      to_delete = []
      for game_id, game_tuple in self._games.iteritems():
        _, start_time = game_tuple
        if now >= start_time + _EXPIRATION:
          to_delete.append(game_id)
      
      for d in to_delete:
        del self._games[d]

  def StartGame(self, request, context):
    game = guessing_game.Game(_DIFFICULTIES[request.difficulty])
    self._games[game.game_id] = (game, time.time())
    response = number_guesser_pb2.StartGameResponse()
    response.game_id = game.game_id
    response.lower = game.lower
    response.upper = game.upper
    return response

  def Guess(self, request, context):
    response = number_guesser_pb2.GuessResponse()
    if not request.game_id:
      context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
      context.set_details('game_id is required.')
      return response
    game_id = request.game_id
    if game_id not in self._games:
      context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
      context.set_details(
          'game_id %s not found! Please call StartGame first.' % game_id)
      return response
    game, start_time = self._games[game_id]
    response.result = game.Guess(request.guess)
    return response
      

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  number_guesser_pb2_grpc.add_NumberGuesserServicer_to_server(
      NumberGuesser(), server)
  server.add_insecure_port('[::]:20308')
  server.start()
  try:
    while True:
      time.sleep(1000)
  except KeyboardInterrupt:
    server.stop(0)


if __name__ == '__main__':
  serve()