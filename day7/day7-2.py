import bisect
import string
import day7


class Worker(object):
    def __init__(self, cur_time):
        self.time = cur_time
        self.available = True
        self._task = None
        self.time_complete = self.time
    
    @property
    def task_complete(self):
        return self.time >= self.time_complete

    @property
    def task(self):
        return self._task

    @task.setter
    def task(self, value):
        self._task = value.id
        self.time_complete = self.task_time + self.time

    @property
    def task_time(self):
        if self.task:
            letter = self.task
            letter_values = {
                letter: value + 1 for value, letter in enumerate(string.ascii_uppercase)
            }
            BASE_TIME = 60

            return BASE_TIME + letter_values[letter]
        return None

    def step(self):
        self.time += 1


def main(graph, debug=False):
    cur_time = 0
    break_point = cur_time
    complete = False

    indexes = [graph.nodes.index(origin) for origin in graph.origin]
    visible_nodes = sorted([graph.nodes[index] for index in indexes])

    tasks_available = list(visible_nodes)
    tasks_complete = set()

    NUM_WORKERS = 5
    workers = [Worker(cur_time) for i in range(NUM_WORKERS)]

    while not complete:
        # Check all workers for complete tasks and add new nodes to visible
        # nodes
        for worker in workers:
            if worker.task_complete and worker.task:
                tasks_complete.add(worker.task)

                index = graph.nodes.index(worker.task)
                next_nodes = graph.nodes[index].to
                for node in next_nodes:
                    if all(
                        [
                            node not in visible_nodes,
                            node not in tasks_available,
                            node not in [worker.task for worker in workers],
                            node not in tasks_complete
                        ]
                    ):
                        index = graph.nodes.index(node)
                        bisect.insort(visible_nodes, graph.nodes[index])

        # Check if any new tasks are available
        for node in visible_nodes:
            if all([(n in tasks_complete) for n in node.fr]):
                if all([
                    node not in tasks_available,
                    node not in [worker.task for worker in workers],
                    node not in tasks_complete
                ]
                ):
                    bisect.insort(tasks_available, node)

        # Assign tasks to workers
        for worker in workers:
            if worker.task_complete:
                if tasks_available:
                    worker.task = tasks_available.pop(0)
                    if worker.task in visible_nodes:
                        visible_nodes.remove(worker.task)

        # Check if complete
        if tasks_complete == graph.unique_nodes:
            complete = True

        # Debug statements:
        if debug:
            if break_point == cur_time:
                print("*" * 150)
                print("Debug // Current time is:", cur_time)
                print("Tasks complete are:", sorted(tasks_complete))
                print("Tasks available are:", tasks_available)
                print("Current visible nodes are:", visible_nodes)
                for i, worker in enumerate(workers):
                    print(f"Worker {i}: {str(worker.task).ljust(5)} || {str(worker.time_complete).ljust(7)} || {worker.task_complete}")
                print("*"*150)
                break_point = int(input("Enter new breakpoint (int): ")) + cur_time

        # Step time
        cur_time += 1
        for worker in workers:
            worker.step()

    # Print final answer (off by one due to how we step through time)
    print(cur_time - 1)


filepath = 'day7\\input.txt'
g1 = day7.Graph(day7.InstructionsReader(filepath))
main(g1, debug=True)
