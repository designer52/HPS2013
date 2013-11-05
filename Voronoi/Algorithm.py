import random
import Moves
from subprocess import call

class Algorithm:
  CURRENT_PLAYER = 0
  PLAYER_ONE = 1
  PLAYER_TWO = 2
  def __init__(self, currPlayer):
    self.CURRENT_PLAYER = currPlayer

  def playMove(board):
    # ??? how to do empty statement ???
    a = 1 + 1

class CPlusPlusAlgorithm:
  CURRENT_PLAYER = None
  __PROGRAM_NAME = ".\Voronoi.exe"
  def __init__(self, playerId):
    self.CURRENT_PLAYER = playerId

  def playMove(self, moves):
    
    call (self.__PROGRAM_NAME)
    f = open('input.txt', 'w')
    f.write(str(self.CURRENT_PLAYER))
    for move in moves.getMoves():
      f.write(',' + str(move[0]) + ',' + str(move[1]) + ',' + str(move[2]))
    f.close()
    
    f = open('output.txt', 'r')
    lines = f.readlines()
    f.close()
    result = lines[0].split(',')
    return (int(result[0]), int(result[1]))
    
class GreedyAlgorithm(Algorithm):
  def __init__(self, currPlayer):
    Algorithm.__init__(self, currPlayer)
    random.seed()

  def __findRandomMoveToPlay(self, moves):
    randomMove = ()
    while (len(randomMove) == 0):
      x = random.randint(0, moves.GRID_LENGTH - 1)
      y = random.randint(0, moves.GRID_LENGTH - 1)
      if moves.isValidMove(x, y):
        randomMove = (x, y)

    return randomMove
  
  def playMove(self, moves):
    move = ()
    bestScore = (0, 0)
    if moves.isFirstMove():
      #move = self.__findRandomMoveToPlay(moves)
      move = (moves.GRID_LENGTH / 2, moves.GRID_LENGTH / 2)
    else:
      for x in range(0, moves.GRID_LENGTH):
        for y in range(0, moves.GRID_LENGTH):
          if moves.isValidMove(x, y):
            moves.addMove(self.CURRENT_PLAYER, x, y)
            score = moves.calcScore()
            if (score[self.CURRENT_PLAYER - 1] > bestScore[self.CURRENT_PLAYER - 1]):
              bestScore = score
              move = (x, y)
              #print 'found new best move ' + str(move) + ' for best score ' + str(bestScore)

            moves.unplayMove()
            
    moves.addMove(self.CURRENT_PLAYER, move[0], move[1])
    print str(moves.getMoves())
            
class RandomAlgorithm():
  CURRENT_PLAYER = 0
  def __init__(self, currPlayer):
    self.CURRENT_PLAYER = currPlayer
    random.seed(0)

  def playMove(self, moves):
    x = random.randint(0, moves.GRID_LENGTH - 1)
    y = random.randint(0, moves.GRID_LENGTH - 1)
    moves.addMove(self.CURRENT_PLAYER, x, y)
    return (x, y)

class RandomAlgorithmImp():
  PLAYER_ONE = 1
  PLAYER_TWO = 2
  CURRENT_PLAYER = 0
  
  def __init__(self, currPlayer):
    self.CURRENT_PLAYER = currPlayer
    random.seed(0)

  def playMove(self, moves):
    # pick coordinates to play
    x = 0
    y = 0
    bestMove = ()
    bestScore = 0
    movesToPlay = []
    while (len(movesToPlay) <= 1):
      x = random.randint(0, moves.GRID_LENGTH - 1)
      y = random.randint(0, moves.GRID_LENGTH - 1)
      if moves.isValidMove(x, y):
        movesToPlay.append((x, y))

    for (x, y) in movesToPlay:
      moves.addMove(self.CURRENT_PLAYER, x, y)
      scores = moves.calcScore()
      if scores[self.CURRENT_PLAYER - 1] > bestScore:
        bestScore = scores[self.CURRENT_PLAYER - 1]
        bestMove = (x, y)
      moves.unplayMove()

    moves.addMove(self.CURRENT_PLAYER, bestMove[0], bestMove[1])
    return (bestMove[0], bestMove[1])

class RandomAlgorithmLookAhead():
  PLAYER_ONE = 1
  PLAYER_TWO = 2
  CURRENT_PLAYER = 0
  LOOK_AHEAD = 4
  __bestMove = ()
  
  def __init__(self, currPlayer):
    self.CURRENT_PLAYER = currPlayer
    random.seed(0)

  def __otherPlayer(self, player):
    if (player == self.PLAYER_ONE):
      return self.PLAYER_TWO

    return self.PLAYER_ONE

  def __findRandomMoveToPlay(self, moves):
    randomMove = ()
    while (len(randomMove) == 0):
      x = random.randint(0, moves.GRID_LENGTH - 1)
      y = random.randint(0, moves.GRID_LENGTH - 1)
      if moves.isValidMove(x, y):
        randomMove = (x, y)

    return randomMove
        
  def playMove(self, moves):
    self.__bestMove = ()
    self.playMoveLookAhead(self.CURRENT_PLAYER, self.LOOK_AHEAD, moves)
    if len(self.__bestMove) == 0:
      # we are losing, just find any random move to play
      self.__bestMove = self.__findRandomMoveToPlay(moves)
      print 'we are losing, playing a random move ' + str(self.__bestMove)
      
    moves.addMove(self.CURRENT_PLAYER, self.__bestMove[0], self.__bestMove[1])

  def __isCurrPlayerWinning(self, score):
    if (self.CURRENT_PLAYER == self.PLAYER_ONE):
      return score[0] > score[1]

    return score[1] > score[0]
  
  def playMoveLookAhead(self, player, lookAhead, moves):
    #print 'look ahead = ' + str(lookAhead) + ' player = ' + str(player) + ' moves ' + str(moves)
    if (lookAhead <= 0 or moves.movesLeft() == 0):
      score = moves.calcScore()
      #print 'returning score ' + str(score)
      return score
    
    # pick coordinates to play
    x = 0
    y = 0
    bestScore = (0, 0)
    movesToPlay = []
    while (len(movesToPlay) < 3):
      x = random.randint(0, moves.GRID_LENGTH - 1)
      y = random.randint(0, moves.GRID_LENGTH - 1)
      if moves.isValidMove(x, y):
        movesToPlay.append((x, y))

    for (x, y) in movesToPlay:
      #print 'playing move ' + str((x, y))
      moves.addMove(player, x, y)
      score = self.playMoveLookAhead(self.__otherPlayer(player), lookAhead - 1, moves)
      #print 'score is ' + str(score)
      if self.__isCurrPlayerWinning(score) and \
         score[self.CURRENT_PLAYER - 1] > bestScore[self.CURRENT_PLAYER - 1]:
        bestScore = score
        self.__bestMove = (x, y)
        print 'found new best move ' + str(self.__bestMove) + ' for best score ' + str(bestScore)
      moves.unplayMove()

    return bestScore

    #moves.addMove(self.CURRENT_PLAYER, bestMove[0], bestMove[1])
