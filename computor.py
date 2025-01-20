import sys
import re

class Term:
	def __init__(self, coefficient: float, variable: str, degree: int):
		self.coefficient = coefficient
		self.variable = variable
		self.degree = degree

	def __str__(self):
		return f"{abs(self.coefficient)} * {self.variable}^{self.degree}"

class Equation:
	def __init__(self):
		self.terms = []
		self.reduced_terms = []
		self.degree_max = -1

	def build_equation_string(self, terms):
		output = ""
		for i, term in enumerate(terms):
			if term.coefficient < 0:
				output += "- "
			else:
				if i > 0:
					output += "+ "
			output += f'{str(term)} '
		return output

	def print_equation(self):
		output = self.build_equation_string(self.terms)
		print(output)

	def highest_degree(self):
		for term in self.terms:
			if term.degree > self.degree_max:
				self.degree_max = term.degree
		if self.degree_max > 0:
			print(f"Polynomial degree: {self.degree_max}")

	def reduce(self):
		for term in self.terms:
			if not self.reduced_terms:
				self.reduced_terms.append(term)
			else:
				for reduced_term in self.reduced_terms:
					if reduced_term.variable == term.variable and reduced_term.degree == term.degree:
						reduced_term.coefficient += term.coefficient
						break
				else:
					self.reduced_terms.append(term)
		self.reduced_terms.sort(key=lambda term: term.degree, reverse=True)
		output = self.build_equation_string(self.reduced_terms)
		print(f'{output}= 0')

	def solve_constant(self):
		if self.reduced_terms[0].coefficient == 0:
			print("All real numbers are solutions.")
		else:
			print("No solution")

	def solve_linear(self):
		a = self.reduced_terms[0].coefficient
		b = self.reduced_terms[1].coefficient
		if a == 0:
			print("No solution")
		else:
			print(f"The solution is:\n{-b / a}")

	def solve_quadratic(self):
		a = self.reduced_terms[0].coefficient
		b = self.reduced_terms[1].coefficient
		c = self.reduced_terms[2].coefficient
		discriminant = b ** 2 - 4 * a * c
		if discriminant > 0:
			x1 = (-b + discriminant ** 0.5) / (2 * a)
			x2 = (-b - discriminant ** 0.5) / (2 * a)
			print(f"Discriminant is strictly positive, the two solutions are:\n{x1:.6f}\n{x2:.6f}")
		elif discriminant == 0:
			x = -b / (2 * a)
			print(f"Discriminant is zero, the solution is:\n{x}")
		else:
			real = -b / (2 * a)
			imaginary = (-discriminant) ** 0.5 / (2 * a)
			print(f"Discriminant is strictly negative, the two solutions are:\n{real} + {imaginary}i\n{real} - {imaginary}i")

	def solve(self):
		self.highest_degree()
		if self.degree_max < 1:
			print("Input error, check polynomial syntax.")
		elif self.degree_max == 0:
			self.solve_constant()
		elif self.degree_max == 1:
			self.solve_linear()
		elif self.degree_max == 2:
			self.solve_quadratic()
		else:
			print("The polynomial degree is strictly greater than 2, I can't solve.")

	def parse_polynomial(self, input: str):
		polynomial = input.replace(" ", "")
		try:
			left, right = polynomial.split('=')
		except ValueError:
			print("Invalid input: no \"=\" sign found.")
			return False
		term_pattern = re.compile(r"(-?\d+(?:\.\d+)?)\s*\*\s*(\w+)\^(\d+)")
		left_terms = term_pattern.findall(left)
		right_terms = term_pattern.findall(right)
		if not left_terms:
			print("Invalid input: check term syntax.")
			return False
		if not right_terms:
			if right != '0':
				print("Invalid input: check term syntax.")
				return False
		for coefficient, variable, degree in left_terms:
			if coefficient == '0':
				continue
			self.terms.append((Term(float(coefficient), variable, int(degree))))
		# Negate coefficients of terms on right side of equation
		for coefficient, variable, degree in right_terms:
			if coefficient == '0':
				continue
			self.terms.append((Term(-float(coefficient), variable, int(degree))))
		return True

	def solve_polynomial(self):
		self.reduce()
		self.solve()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		equation = Equation()
		if not equation.parse_polynomial(sys.argv[1]):
			sys.exit(1)
		equation.solve_polynomial()
	else:
		print("Usage: python computor.py <polynomial>")