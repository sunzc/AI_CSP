#!/usr/bin/env python3

# Project: AI Assignment#2
# Description: CSP with 1)Depth first w/backtracking (DFSB). 2) DFSB++
# Author: Zhichuang Sun
# SBUID: 110345185
# E-mail: zhisun@cs.stonybrook.edu

import sys

def usage():
	print('python dfsb.py <input_file> <output_file> <mode_flag>')
	print('Note: <mode_flag> can be 0, means plain DFS-B; or 1 means improved DFS-B')

class CSP:
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
		print(self._adj_array_)
		print(self._asgn_array_)

	# basic version, no optimization
	def dfsb(self, idx):
		if idx == self.n:
			self.print_res(self._asgn_array_)
			return True

		tag = False
		for color in range(self.k):
			if self.check(idx, color):
				tag = True
				self._asgn_array_[idx] = color
				if self.dfsb(idx+1):
					break
			else:
				continue

		if tag == False:
			return False
		else:
			return True

	# compare color at @idx with every assigned variable to check conflicts
	def check(self, idx, color):
		for adj in self._adj_array_[idx]:
			if adj >= idx:
				continue
			else:
				if color == self._asgn_array_[adj]:
					return False
		return True

	# prune using odering variables and values
	def dfsb_order_var_wrapper(self):
		#possible_value_array
		pva = []
		for x in range(self.n):
			a = []
			for c in range(self.k):
				a.append(c)
			pva.append(a)

		# find variable with MRV(minimum remaining values)
		asgn_array = [-1] * self.n		
		self.dfsb_order_var(pva, asgn_array)

	def dfsb_order_var(self, pva, asgn_array)
		var = self.find_var(pva)
		color = self.find_color(pva, var)
		new_pva = self.construct_new_pva(pva, var, color)
		asgn_array[var] = color
		pass


		
	def find_color(pva, var):
		# least pruned number
		lpn = self.k + 1
		c = -1
		for color in pva[var]:
			pn = 0
			for neighbor in self._adj_array_[var]:
				if color in pva[neighbor]:
					pn += 1
			if pn < lpn:
				lpn = pn
				c = color
		return c
		
	# find variable with MRV(minimum remaining values)
	def find_var(self, pva):
		idx = -1
		min_count = self.k + 1
		for i in range(self.n):
			if len(pva[i]) == 0:
				continue
			if len(pva[i]) < min_count:
				min_count = len(pva[i])
				idx = i
		return idx


	# prune using arc consistency
	def dfsb_ac(self):
		pass
	def print_res(self, arr):
		print("Success, a possible assignment:")
		for x in arr:
			print(x, end=" ")
		print("")

if __name__ == '__main__':

	fd_in = 0
	fd_out = 0
	mode = -1

	if len(sys.argv) == 4:
		try:
			fd_in = open(sys.argv[1], 'r')
			fd_out = open(sys.argv[2], 'w')
			mode = int(sys.argv[3])
			assert(mode == 1 or mode == 0)
		except:
			usage()
			exit(1)
	else:
		usage()
		exit(1)

	csp = CSP(fd_in, fd_out)
	csp.dfsb(0)
