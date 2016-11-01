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

	# wrapper for the recursive function
	# which prune using odering variables and values
	def dfsb_order_var_color_wrapper(self):
		#possible_value_array
		pva = []
		for x in range(self.n):
			a = []
			for c in range(self.k):
				a.append(c)
			pva.append(a)

		# find variable with MRV(minimum remaining values)
		asgn_array = [-1] * self.n		
		ret = self.dfsb_order_var_color(pva, 0)
		if ret == True:
			print("Find a solution!")
		else:
			print("Find no solution!")

	# do the job: prune using odering variables and values
	def dfsb_order_var_color(self, pva, depth):
		var = self.find_var(pva)
		color_list = self.get_ordered_color_list(pva, var)

		# no valid variable found
		if var == -1:
			return False

		flag = False
		for t in color_list:
			new_pva = self.construct_new_pva(pva, var, t[1])
			if (new_pva == None):
				# skip bad color
				continue

			self._asgn_array_[var] = t[1]
			if depth + 1 == self.n:
				self.print_res(self._asgn_array_)
				return True

			# use arc-pruning to reduce search domains
			self.ac_pruning(new_pva)
			ret = self.dfsb_order_var_color(new_pva, depth + 1)
			if ret == True:
				flag = True
				break

			# restore asgn_array and pva for next round
			self._asgn_array_[var] = -1

		return flag

	# update pva according to the variable and color we have chosen
	def construct_new_pva(self, pva, var, color):
		# copy pva to new pva
		new_pva = []
		for i in range(len(pva)):
			# for the assigned var, it has only one possible value, that is color
			if i == var:
				new_pva.append([color])
				continue

			a = []
			for e in pva[i]:
				a.append(e)
			new_pva.append(a)

		for neighbor in self._adj_array_[var]:
			if color in new_pva[neighbor]:
				new_pva[neighbor].remove(color)
			if len(new_pva[neighbor]) == 0:
				# reach dead end, we should back track
				return None
		return new_pva

	# order color according to how much it affect other variables 
	# return color list in ascending order like [1,2,3]
	def get_ordered_color_list(self, pva, var):
		# least pruned number
		clist = []
		for color in pva[var]:
			pn = 0
			for neighbor in self._adj_array_[var]:
				if color in pva[neighbor]:
					pn += 1
			# tuple (affects, color)
			clist.append((pn,color))
		return sorted(clist, key = lambda x: x[0])

	# find variable with MRV(minimum remaining values)
	def find_var(self, pva):
		idx = -1
		min_count = self.k + 1
		for i in range(self.n):
			if self._asgn_array_[i] != -1:
				# skip already assigned variable
				continue
			if len(pva[i]) == 0:
				# print("Warning! no remaining value means dead end, we should backtrack!")
				return -1
			if len(pva[i]) < min_count:
				min_count = len(pva[i])
				idx = i
		return idx

	# prune using arc consistency
	def ac_pruning(self, pva):
		# generate queue of arcs
		queue = []
		for i in range(self.n):
			for j in self._adj_array_[i]:
				queue.append((i,j))
		while len(queue) != 0:
			(xi, xj) = queue.pop(0)
			if self.remove_inconsistency_values(xi, xj, pva):
				for xk in self._adj_array_[xi]:
					queue.append((xk, xi))

	# return true if succeeds
	def remove_inconsistency_values(self, xi, xj, pva):
		removed = False
		for x in pva[xi]:
			if not self.arc_test(x, pva[xj]):
				pva[xi].remove(x)
				removed = True
		return removed

	# test any value in arr is consistent with x
	def arc_test(self, x, arr):
		for y in arr:
			if y != x:
				return True
		return False

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
	#csp.dfsb(0)
	csp.dfsb_order_var_color_wrapper()
