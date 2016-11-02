#!/usr/bin/env python3

# Project: AI Assignment#2
# Description: Local Search with minconflicts
# Author: Zhichuang Sun
# SBUID: 110345185
# E-mail: zhisun@cs.stonybrook.edu

import sys
import random

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

		self.n = N
		self.m = M
		self.k = K

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

	def search(self, max_count):
		self.greedy_initial_assignment()
		print("greedy initial assignment:")
		self.print_res(self._asgn_array_)

		# TODO
		flag = False
		for i in range(max_count):
			var_list = self.find_conflicts_var_list()
			print("conflict var list")
			print(var_list)

			if (len(var_list) == 0):
				self.print_res(self._asgn_array_)
				flag = True
				break
				
			idx = random.randrange(0, len(var_list))
			var = var_list[idx]

			print("random var chosen, idx:%d var:%d"%(idx, var))

			color = self.find_assignment_with_min_conflicts(var)
			self._asgn_array_[var] = color
			is_final = self.check_result()
			if is_final == True:
				flag = True
				self.print_res(self._asgn_array_)
				break

		if flag == False:
			print("No Result")
			self.print_res(self._asgn_array_)

	def greedy_initial_assignment(self):
		for var in range(self.n):
			color = self.find_assignment_with_min_conflicts(var)
			self._asgn_array_[var] = color

	def find_conflicts_var_list(self):
		conflicts_vars = []
		for var in range(self.n):
			for neighbour in self._adj_array_[var]:
				if self._asgn_array_[var] == self._asgn_array_[neighbour]:
					conflicts_vars.append(var)
					break
		return conflicts_vars

	def find_assignment_with_min_conflicts(self, var):
		color = -1
		min_conflicts = self.n
		for clr in range(self.k):
			total_conflicts = 0
			for neighbour in self._adj_array_[var]:
				if clr == self._asgn_array_[neighbour]:
					total_conflicts += 1
			if total_conflicts < min_conflicts:
				color = clr
				min_conflicts = total_conflicts
		print("min_conflicts : %d color:%d" % (min_conflicts, color))
		return color

	def check_result(self):
		for var in range(self.n):
			for neighbour in self._adj_array_[var]:
				if self._asgn_array_[var] == self._asgn_array_[neighbour]:
					return False
		return True

	def print_res(self, arr):
		print("current assignment:")
		for x in arr:
			print(x, end=" ")
		print("")


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
	ls.search(50)
