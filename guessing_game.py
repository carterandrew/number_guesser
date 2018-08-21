"""Module to manage a number guessing game."""

import random
import uuid

import number_guesser_pb2

_MAX_INT = 4294967295


class Game(object):
  
  def __init__(self, interval=None):
    self._game_id = self._GenerateId()
    self._lower = 0
    if not interval:
      self._upper = _MAX_INT
    else:
      self._upper = self._lower + interval
    self._target = self._PickTarget()
  
  @property
  def game_id(self):
    return self._game_id
    
  @property
  def lower(self):
    return self._lower
    
  @property
  def upper(self):
    return self._upper
    
  def _GenerateId(self):
    return str(uuid.uuid4())
    
  def _PickTarget(self):
    return random.randint(self._lower, self._upper)
    
  def Guess(self, guess):
    if guess > self._target:
      return number_guesser_pb2.RESULT_HIGH
    elif guess < self._target:
      return number_guesser_pb2.RESULT_LOW
    return number_guesser_pb2.RESULT_CORRECT