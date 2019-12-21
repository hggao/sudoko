#!/usr/bin/env python

import math
import time
import argparse
import sys

table = [
  [None, None, None, None, None, None, None, None, None],
  [None, None, None, None, None, None, None, None, None],
  [None, None, None, None, None, None, None, None, None],
  [None, None, None, None, None, None, None, None, None],
  [None, None, None, None, None, None, None, None, None],
  [None, None, None, None, None, None, None, None, None],
  [None, None, None, None, None, None, None, None, None],
  [None, None, None, None, None, None, None, None, None],
  [None, None, None, None, None, None, None, None, None]
]

class Cell(object):
  def __init__(self, ch):
    self.possibles = []
    self.used = False
    if ch == "*":
      self.possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    else:
      self.possibles.append(int(ch))

  def char(self):
    if len(self.possibles) > 1:
      return "*"
    return str(self.possibles[0])

  def printable(self, debug=False):
    if len(self.possibles) > 1:
      if debug:
        return str(self.possibles)
      else:
        return "*"
    return str(self.possibles[0])

def load_table(file_name):
  with open(file_name, "r") as ff:
    lines = ff.readlines()
  for ii in range(9):
    for jj in range(9):
      ch = lines[ii][jj:jj+1]
      table[ii][jj] = Cell(ch)

def print_table(debug=False):
  for ii in range(9):
    for jj in range(9):
      print(table[ii][jj].printable(debug)),
    print ""

def get_determined_num():
  num = 0
  for ii in range(9):
    for jj in range(9):
      if len(table[ii][jj].possibles) == 1:
        num += 1

  return num

def reduce_num_from_block(num, ii, jj):
  yeild = 0
  row_start = ii / 3 * 3
  col_start = jj / 3 * 3
  for row in range(row_start, row_start+3):
    for col in range(col_start, col_start+3):
      if not (row == ii and col == jj):
        if num in table[row][col].possibles:
          table[row][col].possibles.remove(num)
          if len(table[row][col].possibles) == 1:
            yeild += 1
  return yeild

def reduce_num_from_row(num, ii, jj):
  yeild = 0
  for col in range(9):
    if col != jj:
      if num in table[ii][col].possibles:
        table[ii][col].possibles.remove(num)
        if len(table[ii][col].possibles) == 1:
          yeild += 1
  return yeild
  
def reduce_num_from_col(num, ii, jj):
  yeild = 0
  for row in range(9):
    if row != ii:
      if num in table[row][jj].possibles:
        table[row][jj].possibles.remove(num)
        if len(table[row][jj].possibles) == 1:
          yeild += 1
  return yeild
  
def calculate_table_squares():
  yeild = 0
  for ii in range(9):
    for jj in range(9):
      ch = table[ii][jj].char()
      if ch != "*" and table[ii][jj].used == False:
        num = int(ch)
        # Reduce this num from its block
        yeild += reduce_num_from_block(num, ii, jj)
        # Reduce this num from its row
        yeild += reduce_num_from_row(num, ii, jj)
        # Reduce this num from its col
        yeild += reduce_num_from_col(num, ii, jj)
        table[ii][jj].used = True
  return yeild

def reduce_possible_by_determines():
  counter = 1
  while (True):
    print("Reducing possibility ......(%d)" % counter),
    yeild = calculate_table_squares()
    print "Determined %d." % yeild
    if yeild == 0:
      break
    print_table()
    counter += 1

def reduce_poss_from_block(ii, jj):
  base_set = set(table[ii][jj].possibles)
  row_start = ii / 3 * 3
  col_start = jj / 3 * 3
  for row in range(row_start, row_start+3):
    for col in range(col_start, col_start+3):
      if not (row == ii and col == jj):
        base_set -= set(table[row][col].possibles)
  base_poss = list(base_set)
  if len(base_poss) == 1:
    table[ii][jj].possibles = base_poss

def reduce_poss_from_row(ii, jj):
  base_set = set(table[ii][jj].possibles)
  for col in range(9):
    if col != jj:
      base_set -= set(table[ii][col].possibles)
  base_poss = list(base_set)
  if len(base_poss) == 1:
    table[ii][jj].possibles = base_poss
  
def reduce_poss_from_col(ii, jj):
  base_set = set(table[ii][jj].possibles)
  for row in range(9):
    if row != ii:
      base_set -= set(table[row][jj].possibles)
  base_poss = list(base_set)
  if len(base_poss) == 1:
    table[ii][jj].possibles = base_poss
  
def reduce_possible_by_possibles():
  for ii in range(9):
    for jj in range(9):
      ch = table[ii][jj].char()
      if ch == "*":
        reduce_poss_from_block(ii, jj)
        reduce_poss_from_row(ii, jj)
        reduce_poss_from_col(ii, jj)

if __name__ == "__main__":
  # Get the commandline arguements
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--input", type=str, default="37.txt", help="Specify input file")
  args = parser.parse_args()
  print "Input : " + args.input
  if not args.input:
    print "Usage:"
    print "  ./sudoku.py -i/--input"
    sys.exit(1)
  print "Load table ......"
  load_table(args.input)

  print "Initial status:"
  print_table()

  num_start = get_determined_num()
  while (True):
    reduce_possible_by_determines()
    num_now = get_determined_num()
    if num_now == 81 or num_now == num_start:
      print "Stopped at %d numbers done!" % num_now
      if num_now != 81:
        print_table(debug=True)
      break

    num_start = num_now
    reduce_possible_by_possibles()

