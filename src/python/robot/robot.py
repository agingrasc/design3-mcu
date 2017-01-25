class Robot:
    def __init__(self):
        self.current_state = "WAITING"

    def get_state(self):
        return self.current_state

    def execute_task(self, task):
        self.current_state = "EXECUTING TASK"
        task.execute()
