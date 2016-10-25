#!/usr/bin/env python3

# Project: AI Assignment#2
# Description: Local Search with minconflicts
# Author: Zhichuang Sun
# SBUID: 110345185
# E-mail: zhisun@cs.stonybrook.edu

import sys

def usage():
	print('python minconflicts.py <input_file> <output_file>') 

class LocalSearch:
	def __init__(self, input_file, output_file):
		'''
		Parse info from input file, like Variable Number N, constraints number M, and posible assignments K
		'''
		N = M = K = 0
		try:
			head_line = input_file.readline()
			fields = head_line.split()
			N = int(fields[0])
			M = int(fields[1])
			K = int(fields[2])
		except:
			print("input file format does not match!")
			exit(1)

		self._adj_array_ = [[] for i in range(N)]
		self._asgn_array_ = [-1] * N
		i = 0
		for line in input_file.readlines():
			fields = line.split()
			x, y = int(fields[0]), int(fields[1])
			self._adj_array_[x].append(y)
			self._adj_array_[y].append(x)
			i += 1

		# make sure there are M constraints as claimed in head line
		assert(i == M)

		self._adj_array_
		self._asgn_array_

	def search(self):
		pass

	def print_res(self):
		pass


if __name__ == '__main__':

	fd_in = 0
	fd_out = 0

	if len(sys.argv) == 3:
		try:
			fd_in = open(sys.argv[1], 'r')
			fd_out = open(sys.argv[2], 'w')
		except:
			usage()
			exit(1)
	else:
		usage()
		exit(1)

	ls = LocalSearch(fd_in, fd_out)
	ls.search()
	ls.print_res()