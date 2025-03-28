import re
from term import Term

class Equation:
	def __init__(self):
		self.terms = []
		self.reduced_terms = []
		self.degree_max = -1

	def parse_polynomial(self, input: str) -> bool:
		polynomial = input.replace(" ", "")
		try:
			left, right = polynomial.split('=')
		except ValueError:
			print("Invalid input: no \"=\" sign found.")
			return False
		term_pattern = re.compile(r"(-?\d+(?:\.\d+)?)\s*\*\s*(\w+)\^(-?\d+)")
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
			if int(degree) < 0:
				print("Invalid input: Degree is negative.")
				return False
			if coefficient != '0':
				self.terms.append((Term(float(coefficient), variable, int(degree))))
		# Negate coefficient of terms on right side of equation
		for coefficient, variable, degree in right_terms:
			if int(degree) < 0:
				print("Invalid input: Degree is negative.")
				return False
			if coefficient != '0':
				self.terms.append((Term(-float(coefficient), variable, int(degree))))
		return True

	def build_equation_string(self, terms) -> str:
		output = ""
		for i, term in enumerate(terms):
			if term.coefficient != 0:
				if term.coefficient < 0:
					if i == 0:
						output += '-'
					else:
						output += "- "
				else:
					if i > 0:
						output += "+ "
				output += f'{str(term)} '
		return output

	def find_highest_degree(self):
		for term in self.reduced_terms:
			if term.degree > self.degree_max:
				self.degree_max = term.degree

	def reduce(self):
		term_map = {}
		for term in self.terms:
			key = (term.variable, term.degree)
			if key in term_map:
				sum = term_map[key].coefficient + term.coefficient
				if sum != 0:
					term_map[key].coefficient = sum
				else:
					del term_map[key]
			else:
				term_map[key] = term
		self.reduced_terms = sorted(term_map.values(), key=lambda term: term.degree)
		output = self.build_equation_string(self.reduced_terms)
		print(f'Reduced form: {output}= 0')

	def solve_constant(self):
		if self.reduced_terms[0].coefficient == 0:
			print("Any real number is a solution.")
		else:
			print("No solution.")

	def solve_linear(self):
		a = self.reduced_terms[1].coefficient
		b = self.reduced_terms[0].coefficient
		if a == 0:
			print("No solution.")
		else:
			print(f"The solution is:\n{(-b / a):.6f}")

	def solve_quadratic(self):
		if len(self.reduced_terms) == 1:
			print("The solution is:\n0")
			return
		elif len(self.reduced_terms) == 2:
			right_side = self.reduced_terms[0].coefficient
			print(f'The solutions are:\n+√{right_side}\n-√{right_side}')
			return
		a = self.reduced_terms[2].coefficient
		b = self.reduced_terms[1].coefficient
		c = self.reduced_terms[0].coefficient
		discriminant = b ** 2 - 4 * a * c
		if discriminant > 0:
			x1 = (-b - discriminant ** 0.5) / (2 * a)
			x2 = (-b + discriminant ** 0.5) / (2 * a)
			print(f"Discriminant is strictly positive, the two solutions are:\n{x1:.6f}\n{x2:.6f}")
		elif discriminant == 0:
			x = -b / (2 * a)
			print(f"Discriminant is zero, the solution is:\n{x}")
		else:
			real = -b / (2 * a)
			imaginary = (-discriminant) ** 0.5 / (2 * a)
			print(f"Discriminant is strictly negative, the two complex solutions are:\n{real} + {imaginary}i\n{real} - {imaginary}i")

	def solve(self):
		self.find_highest_degree()
		if self.degree_max > 0:
			print(f"Polynomial degree: {self.degree_max}")
		if not self.reduced_terms:
			print("Any real number is a solution.")
			return
		if self.degree_max < 0:
			print("Input error, check polynomial syntax.")
		elif self.degree_max == 0:
			self.solve_constant()
		elif self.degree_max == 1:
			self.solve_linear()
		elif self.degree_max == 2:
			self.solve_quadratic()
		else:
			print("The polynomial degree is strictly greater than 2, I can't solve.")