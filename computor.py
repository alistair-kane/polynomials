#!/usr/bin/env python3
from equation import Equation
import sys

if __name__ == '__main__':
	if len(sys.argv) > 1:
		equation = Equation()
		if not equation.parse_polynomial(sys.argv[1]):
			sys.exit(1)
		equation.reduce()
		equation.solve()
	else:
		print("Usage: python computor.py <polynomial>")