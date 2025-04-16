#JPST - Jedi Padawan Sorting Tool
# It is a tool for evaluating Padawan candidates using logic expressions
# and numerical attributes to assist Jedi Masters in selecting their apprentices.

class Padawan:
    
    #Represents a Padawan in the Jedi Order.
    #Contains both numerical properties (e.g., skill scores)
    #and logical expressions to evaluate compatibility with Jedi Masters.
    
    def __init__(self, name, age, discipline_score, force_sensitivity, expression, truth_values):
        self.name = name
        self.age = age
        self.discipline_score = discipline_score  # Number(1-100)
        self.force_sensitivity = force_sensitivity  # Number(1-100)
        self.expression = expression  # Represents the Padawan's decision logic or belief system
        self.truth_values = truth_values  # Assigns True/False values to each variable in the expression ("p": True, "q": False)


    def __str__(self):
        return f"{self.name} (Age: {self.age}) | Discipline: {self.discipline_score} | Force: {self.force_sensitivity}"
    
class LogicalExpression:
#Processes logical expressions for truth table evaluation.

    def __init__(self, expression, truth_values):
        self.expression = expression 
        self.truth_values = truth_values  

    def evaluate(self):
    #Evaluates the logical expression using truth values.

        expr = self.expression
        for var, val in self.truth_values.items():
            expr = expr.replace(var, str(val))