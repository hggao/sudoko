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

def find_single_line_possible(blk_row, blk_col):
  ''' Search a 3x3 block, find out if there's a undermined number appears only
      on a single row or column.
  '''
  all_poss = []
  for rr in range(3):
    for cc in range(3):
      poss = table[blk_row*3+rr][blk_col*3+cc].possibles
      if len(poss) > 1:
       all_poss += poss

  result = []
  for nn in all_poss:
    nn_rows = []
    nn_cols = []
    for rr in range(3):
      for cc in range(3):
        rrr = blk_row*3+rr
        ccc = blk_col*3+cc
        poss = table[rrr][ccc].possibles
        if nn in poss:
          if rrr not in nn_rows:
            nn_rows.append(rrr)
          if ccc not in nn_cols:
            nn_cols.append(ccc)
    if len(nn_rows) == 1 and len(nn_cols) > 1:
      result.append((nn, nn_rows[0], None))
    if len(nn_cols) == 1 and len(nn_rows) > 1:
      result.append((nn, None, nn_cols[0]))

  return result

def reduce_row_of_other_blocks(num, row, blk_col):
  for col in range(9):
    if col < blk_col*3 or col >= blk_col*3+3:
      if num in table[row][col].possibles:
        table[row][col].possibles.remove(num)

def reduce_col_of_other_blocks(num, col, blk_row):
  for row in range(9):
    if row < blk_row*3 or row >= blk_row*3+3:
      if num in table[row][col].possibles:
        table[row][col].possibles.remove(num)

def reduce_possible_by_block():
  for blk_row in range(3):
    for blk_col in range(3):
      all_finds = find_single_line_possible(blk_row, blk_col)
      for (num, row, col) in all_finds:
        if row is not None:
          reduce_row_of_other_blocks(num, row, blk_col)
        else:
          reduce_col_of_other_blocks(num, col, blk_row)

if __name__ == "__main__":
  # Get the commandline arguements
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--input", type=str, default="71.txt", help="Specify input file")
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
    print "=== 1 === Applying rule 1 ......"
    reduce_possible_by_determines()
    num_now = get_determined_num()
    if num_now == 81 or num_now == num_start:
      print "Stopped at %d numbers done!" % num_now
      if num_now != 81:
        print_table(debug=True)
      break

    num_start = num_now
    print "=== 2 === Applying rule 2 ......"
    reduce_possible_by_possibles()

    print "=== 3 === Applying rule 3 ......"
    reduce_possible_by_block()
