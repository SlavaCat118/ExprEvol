import random

from allowed_operators import FUNCTIONS, OPERATORS, STOPS

FULL = FUNCTIONS | {i:2 for i in OPERATORS}

class Expression(object):
	"""docstring for Expression"""

	def __init__(self, operator, args=None):
		self.operator = operator
		self.args = list() if args is None else args
		self.var_names = ["x","y"]
		self.spacing = ""

	def generate_expression(self):
		operator = None
		needed_args = 0
		args = list()

		if random.random() < 0.6:
			if random.random() < 0.5:
				operator = random.choice(list(FUNCTIONS.keys()))
			else:
				operator = random.choice(OPERATORS)
		else:
			operator = random.choice(STOPS)

		if operator not in STOPS:
			if operator in FUNCTIONS:
				needed_args = FUNCTIONS[operator]
				if needed_args == -1:
					needed_args = random.randrange(1,3)
				elif needed_args < -1:
					needed_args = random.randrange(1,-needed_args)
			elif operator in OPERATORS:
				needed_args = 2

			for i in range(needed_args):
				arg = self.generate_expression()
				args.append(arg)
		else:
			if operator == "var":
				operator = random.choice(self.var_names)
			elif operator == "":
				args = [random.randrange(-100,100)]


		return Expression(operator, args)

	def __str__(self):
		if self.operator in FUNCTIONS: 
			base_string = self.operator+"(" + self.spacing
			for n, arg in enumerate(self.args):
				base_string += str(arg)
				if n != len(self.args)-1:
					base_string += "," + self.spacing
			return base_string + self.spacing + ")"
		elif self.operator in OPERATORS:
			base_string = str(self.args[0]) + self.spacing + self.operator + self.spacing + str(self.args[1])
			return base_string
		else:
			if self.operator == "":
				return str(self.args[0])
			else:
				return self.operator

	def get_gmic_function(self, width, height):
		return f"gmic {width},{height},1,1,\""+str(self)+"\""

test = Expression("sin")
test = test.generate_expression()
print(test.get_gmic_function(200,200))	