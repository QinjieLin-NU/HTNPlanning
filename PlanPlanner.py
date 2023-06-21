class Operator:
    def __init__(self, name, preconditions, effects):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects

class Method:
    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks

class Task:
    def __init__(self, name):
        self.name = name

class Planner:
    def __init__(self, initial_state, methods, operators, tasks):
        self.state = initial_state
        self.methods = methods
        self.operators = operators
        self.tasks = tasks

    def get_applicable_methods(self, task):
        return [method for method in self.methods if method.name == task.name]

    def get_applicable_operators(self, task):
        return [operator for operator in self.operators if operator.name == task.name and operator.preconditions.issubset(self.state)]

    def apply_operator(self, operator):
        self.state.difference_update(operator.preconditions)
        self.state.update(operator.effects)

    def plan(self, tasks):
        if not tasks:
            return []
        task = tasks[0]
        rest_tasks = tasks[1:]

        # Try each operator
        for operator in self.get_applicable_operators(task):
            self.apply_operator(operator)
            result = self.plan(rest_tasks)
            if result is not None:
                return [operator.name] + result

        # Try each method
        for method in self.get_applicable_methods(task):
            result = self.plan(method.tasks + rest_tasks)
            if result is not None:
                return result

        return None

# Define the operators
operators = [
    Operator('PlaceOrder', {'IsAtHome','!IsOrderPlaced','!IsAtStore', '!IsPizzaPicked'}, 
             {'IsAtHome','IsOrderPlaced','!IsAtStore', '!IsPizzaPicked'}),
    Operator('TravelToStore', {'IsAtHome','IsOrderPlaced','!IsAtStore', '!IsPizzaPicked'}, 
             {'!IsAtHome','IsOrderPlaced','IsAtStore', '!IsPizzaPicked'}),
    Operator('PickupPizza', {'!IsAtHome','IsOrderPlaced','IsAtStore', '!IsPizzaPicked'}, 
             {'!IsAtHome','IsOrderPlaced','IsAtStore', 'IsPizzaPicked'}),
]

# Define the tasks
tasks = [Task(name) for name in ['GetPizza']]

# Define the methods
methods = [Method('GetPizza', [Task(name) for name in ['PlaceOrder', 'TravelToStore', 'PickupPizza']])]

# Define the initial state
initial_state = {'IsAtHome', '!IsOrderPlaced', '!IsAtStore', '!IsPizzaPicked'}

# Initialize the planner
planner = Planner(initial_state, methods, operators, tasks)

# Get the plan
plan = planner.plan(tasks)

print("Plan:", plan)
