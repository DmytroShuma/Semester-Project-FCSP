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

def get_bool(prompt):
    answer = input(prompt).strip().lower()
    return answer.startswith("t")  # Accepts 't', 'true', etc.

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
    loyal = get_bool("Is the Padawan loyal to the Jedi Code? (t/f): ")
    impulsive = get_bool("Is the Padawan impulsive? (t/f): ")
    patient = get_bool("Can the Padawan remain calm and composed? (t/f): ")

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

def insertion_sort_by_discipline(padawans):
    # Evaluate logic for all Padawans before sorting
    for padawan in padawans:
        logic = LogicalExpression(padawan.expression, padawan.truth_values)
        padawan.logic_result = logic.evaluate()

    # Insertion sort by discipline_score (descending), then logic_result (True first)
    for i in range(1, len(padawans)):
        key = padawans[i]
        j = i - 1
        while j >= 0 and (
            padawans[j].discipline_score < key.discipline_score or
            (padawans[j].discipline_score == key.discipline_score and not padawans[j].logic_result and key.logic_result)
        ):
            padawans[j + 1] = padawans[j]
            j -= 1
        padawans[j + 1] = key

print("\n\nJedi Council Evaluation Report:\n")

insertion_sort_by_discipline(padawan_list)

for padawan in padawan_list:
    logic = LogicalExpression(padawan.expression, padawan.truth_values)
    result = logic.evaluate()

    print("--------------------------------------------------")
    print(padawan)
    print(f"Expression: {padawan.expression}")
    print("With values:")
    for var, val in padawan.truth_values.items():
        meaning = meanings.get(var, "Unknown")
        print(f"  {var} = {val}  -->  {meaning}")
    print(f"\nFinal Result: {result}")

    if result is True:
        print("This Padawan is READY for Jedi training.")
    elif result is False:
        print("This Padawan is NOT ready. Further guidance required.")
    else:
        print(f"Evaluation Error: {result}")