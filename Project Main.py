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

    # Now we need to replace logical operators with symbols for Python
        expr = expr.replace("∧", " and ")
        expr = expr.replace("∨", " or ")
        expr = expr.replace("¬", " not ")
        expr = expr.replace("→", " <= ")  # Shows that p → q is equivalent to ¬p ∨ q
        expr = expr.replace("↔", " == ")  # Equivalence

        try:
            result = eval(expr)
            return result
        except Exception as e:
            return f"Error evaluating expression: {e}"
        

#Descriptions for our variables
meanings = {
    "loyal": "Is loyal to the Jedi Code",
    "impulsive": "Acts without thinking or control",
    "patient": "Able to remain calm, composed and wait for great results"}

#Interactive interface for the Jedi to input their data about Padawans into a list and get results
padawan_list = []

print("Welcome to the Jedi Padawan Sorting Tool (JPST)")
print("Please input Padawan profiles to evaluate readiness for training.")
while True:
    print("\n--- New Padawan Entry ---")
    name = input("Enter Padawan name: ")
    age = int(input("Enter Padawan age: "))
    discipline = int(input("Enter discipline score (0–100): "))
    force = float(input("Enter Force sensitivity (0.0–100.0): "))
    
    print("\nPlease answer the following with True or False:")
    loyal = input("Is the Padawan loyal to the Jedi Code? ").strip().capitalize() == "True"
    impulsive = input("Is the Padawan impulsive? ").strip().capitalize() == "True"
    patient = input("Can the Padawan remain calm, composed and wait for great results? ").strip().capitalize() == "True"
    
    expression = "loyal ∧ ¬impulsive ∧ patient"
    truth_values = {
    "loyal": loyal,
    "impulsive": impulsive,
    "patient": patient}
    
    padawan = Padawan(name, age, discipline, force, expression, truth_values)
    padawan_list.append(padawan)
    
    cont = input("Would you like to add another Padawan? (y/n): ").strip().lower()
    if cont != "y":
        break

# Analyzing logic
logic = LogicalExpression(expression, truth_values)
result = logic.evaluate()

# Print results
print("\nPadawan Info:")
print(padawan)

print("\nLogic Evaluation:")
print(f"Expression: {expression}")
print("With values:")
for var, val in truth_values.items():
    meaning = meanings.get(var, "Unknown")
    print(f"  {var} = {val}  -->  {meaning}")
print(f"\nFinal Result: {result}")