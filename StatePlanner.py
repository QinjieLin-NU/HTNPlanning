class Operator:
    def __init__(self, name, preconditions, effects):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects

class State:
    def __init__(self, predicates):
        self.predicates = predicates

class Task:
    def __init__(self, name, operator):
        self.name = name
        self.operator = operator

class Planner:
    def __init__(self, initial_state, tasks, goal):
        self.state = initial_state
        self.tasks = tasks
        self.goal = goal

    def is_goal_reached(self):
        return self.goal.issubset(self.state.predicates)

    def get_applicable_tasks(self):
        applicable_tasks = []
        for task in self.tasks:
            if task.operator.preconditions.issubset(self.state.predicates):
                applicable_tasks.append(task)
        return applicable_tasks

    def apply_task(self, task):
        print(self.state.predicates,task.name)
        self.state.predicates.difference_update(task.operator.preconditions)
        self.state.predicates.update(task.operator.effects)
        print(self.state.predicates)

    def plan(self):
        if self.is_goal_reached():
            return []

        for task in self.get_applicable_tasks():
            self.apply_task(task)
            result = self.plan()
            if result is not None:
                return [task.name] + result

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
tasks = [Task(name, operator) for name, operator in zip(['PlaceOrder', 'TravelToStore', 'PickupPizza'], operators)]

# Define the initial state
initial_state = State({'IsAtHome', '!IsOrderPlaced', '!IsAtStore', '!IsPizzaPicked'})

# Define the goal
goal = {'IsPizzaPicked'}

# Initialize the planner
planner = Planner(initial_state, tasks, goal)

# Get the plan
plan = planner.plan()

print("Plan:", plan)
