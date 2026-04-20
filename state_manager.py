steps = {}

def register_next_step(user_id, func):
    steps[user_id] = func