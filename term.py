class Term:
	def __init__(self, coefficient: float, variable: str, degree: int):
		self.coefficient = coefficient
		self.variable = variable
		self.degree = degree

	def __str__(self):
		return f"{abs(self.coefficient)} * {self.variable}^{self.degree}"