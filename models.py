class ComplexTask:
    def __init__(self, param_a: int, param_b: int):
        self.param_a = param_a
        self.param_b = param_b

    @staticmethod
    def from_json(json: dict):
        return ComplexTask(
            param_a=json['paramA'],
            param_b=json['paramB'],
        )


class ComplexTaskBatch:
    def __init__(self, tasks: list):
        self.tasks = tasks
