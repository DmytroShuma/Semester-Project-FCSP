import time
import copy
import random
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
        return f"{self.name} (Age: {self.age}) | Discipline: {self.discipline_score} | Force: {self.force_sensitivity} | Logic: {self.expression}"
    
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
        
def insertion_sort_by_discipline(padawans):   #Insertion sorting function
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

def merge_sort_by_force(padawans):     #Merge sorting function
    if len(padawans) <= 1:
        return padawans

    mid = len(padawans) // 2
    left = merge_sort_by_force(padawans[:mid])
    right = merge_sort_by_force(padawans[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        # Compare by force_sensitivity first, then logic_result (True > False)
        if (left[i].force_sensitivity > right[j].force_sensitivity or
            (left[i].force_sensitivity == right[j].force_sensitivity and left[i].logic_result and not right[j].logic_result)):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

#Linear Search function
def search_ready_padawans(padawans, min_force=0):
    ready_list = []
    for padawan in padawans:
        if padawan.logic_result is True and padawan.force_sensitivity >= min_force:
            ready_list.append(padawan)
    return ready_list


#Descriptions for our variables
meanings = {
    "loyal": "Is loyal to the Jedi Code",
    "impulsive": "Acts without thinking or control",
    "patient": "Able to remain calm, composed and wait for great results"}

def get_bool(prompt):
    answer = input(prompt).strip().lower()
    return answer.startswith("t")  # Accepts 't', 'true', etc.

def print_bar(label, value, max_value, width=40):
    bar_length = int((value / max_value) * width)
    bar = "▇" * bar_length
    print(f"{label:<15}: {bar} {value:.2f} ms")

def generate_padawans(n, expression_type="simple"):
    padawans = []
    for i in range(n):
        name = f"Auto_{i}"
        age = random.randint(10, 18)
        discipline = random.randint(0, 100)
        force = round(random.uniform(0, 100), 2)

        # Random True/False values
        loyal = random.choice([True, False])
        impulsive = random.choice([True, False])
        patient = random.choice([True, False])

        truth_values = {
            "loyal": loyal,
            "impulsive": impulsive,
            "patient": patient
        }

        if expression_type == "simple":
            expression = "loyal ∧ patient"
        else:
            expression = "¬loyal ∨ (patient ∧ ¬impulsive)"

        padawan = Padawan(name, age, discipline, force, expression, truth_values)
        padawans.append(padawan)
    
    return padawans

#Testing random list creation and its logic analysis perfomance
simple_list = generate_padawans(200, "simple")
complex_list = generate_padawans(200, "complex")

# Simple logic analysis perfomance
start = time.time()
for p in simple_list:
    logic = LogicalExpression(p.expression, p.truth_values)
    p.logic_result = logic.evaluate()
insertion_sort_by_discipline(simple_list)
simple_time = (time.time() - start) * 1000

# Complex logic analysis perfomance
start = time.time()
for p in complex_list:
    logic = LogicalExpression(p.expression, p.truth_values)
    p.logic_result = logic.evaluate()
insertion_sort_by_discipline(complex_list)
complex_time = (time.time() - start) * 1000

max_time = max(simple_time, complex_time)

# Show results
for padawan in simple_list:
    print (padawan)

for padawan in complex_list:
    print (padawan)

print("\nLogic Analysis Timing for 200 Padawans in each list)")
print_bar("Simple Logic List", simple_time, max_time)
print_bar("Complex Logic List", complex_time, max_time)

#
#
#
#Interactive interface for the Jedi to input their data about Padawans into a list and get results
padawan_list = []

print("\n\nWelcome to the Jedi Padawan Sorting Tool (JPST)")
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

print("\nDate Sorting Options:")
print("1 - Sort by Discipline (Insertion Sort)")
print("2 - Sort by Force Sensitivity (Merge Sort)")

sort_choice = input("Choose sorting method (1 or 2): ").strip()

for padawan in padawan_list:
    logic = LogicalExpression(padawan.expression, padawan.truth_values)
    padawan.logic_result = logic.evaluate()

if sort_choice == "1":
    insertion_sort_by_discipline(padawan_list)
elif sort_choice == "2":
    padawan_list = merge_sort_by_force(padawan_list)
else:
    print("Invalid choice. Defaulting to Insertion Sort.")
    padawan_list = merge_sort_by_force(padawan_list) #If input is invalid - system will default to using Merge sorting function. 

# Before printing results, the system will evaluate how fast was the sorting process
insertion_list = copy.deepcopy(padawan_list)
merge_list = copy.deepcopy(padawan_list)

# Timing of insertion sort
start_time = time.time()
insertion_sort_by_discipline(insertion_list)
insertion_duration = (time.time() - start_time) * 1000  # in milliseconds

# Timing of merge sort
start_time = time.time()
merge_list = merge_sort_by_force(merge_list)
merge_duration = (time.time() - start_time) * 1000  # in milliseconds

# Perfomace results
print("\nSorting Performance Result")
print(f"Insertion Sort Time: {insertion_duration:.2f} ms")
print(f"Merge Sort Time:     {merge_duration:.2f} ms")


print("\n\nJedi Council Evaluation Report:\n")

for padawan in padawan_list:
 print("--------------------------------------------------")
 print(padawan)
 print(f"Expression: {padawan.expression}")
 print("With values:")
 for var, val in padawan.truth_values.items():
        meaning = meanings.get(var, "Unknown")
        print(f"  {var} = {val}  -->  {meaning}")
 print(f"\nFinal Result: {padawan.logic_result}")

if padawan.logic_result is True:
        print("This Padawan is READY for Jedi training.")
elif padawan.logic_result is False:
        print("This Padawan is NOT ready. Further guidance required.")
else:
        print(f"Evaluation Error: {padawan.logic_result}")

# Testing search functions: finding all logic-approved and ready Padawans with force sensitivity >= 50
matching = search_ready_padawans(padawan_list, min_force=50)

print("\n\n Search Results: Ready for training Padawans with Force sensitivity ≥ 50\n")
if matching:
    for p in matching:
        print(f"- {p.name} | Force: {p.force_sensitivity} | Discipline: {p.discipline_score}")
else:
    print("No matching Padawans found.")
