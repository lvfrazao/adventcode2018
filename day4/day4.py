import re
from datetime import datetime as dt


class Guard(object):
    def __init__(self, guard_id, asleep=None, awake=None):
        self.id = guard_id
        self.asleep = [list(range(asleep, awake))] if asleep else [[]]
        self.time_asleep = awake - asleep if asleep else 0
    
    def add_entry(self, asleep, awake):
        asleep_range = list(range(asleep, awake)) if asleep else []
        self.asleep.append(asleep_range)
        asleep_time = awake - asleep if asleep else 0
        self.time_asleep += asleep_time

    def get_sleep_freq(self):
        freq = {}
        for sleep in self.asleep:
            for minute in sleep:
                freq[minute] = freq.get(minute, 0) + 1
        return freq
    
    def most_asleep_time(self):
        freq = self.get_sleep_freq()
        most_asleep_min = sorted(list(freq.items()), key=lambda x: x[1], reverse=True)[0][0]
        return most_asleep_min

    def __eq__(self, other):
        return self.id == other
    
    def __repr__(self):
        return f"Guard({self.id}, {self.asleep}, {self.time_asleep})"


def read_logs(logs):
    pattern = re.compile(r'\[(\d+)-(\d+)-(\d+) (\d\d):(\d\d)\] (.*)')

    results = []
    for log in logs:
        year, month, day, hour, minute, text = pattern.search(log).groups()
        results.append((dt(int(year), int(month), int(day), int(hour), int(minute)), text))
    
    results = sorted(results, key=lambda x: x[0])
    return results


def organize_logs(logs):
    data = []
    res = {
        "id": None,
        "awake": [],
        "asleep": [],
    }
    for log in logs:
        text = log[1]
        if "begins shift" in text:
            if res:
                if len(res["asleep"]) == 0:
                    res["asleep"] = [None]
                    res["awake"] = [None]
                data.append(dict(res))
                res = {
                    "id": None,
                    "awake": [],
                    "asleep": [],
                }
            id_pattern = re.compile(r'Guard #(\d+) begins shift')
            res["id"] = id_pattern.search(text).group(1)
        elif "wakes up" in text:
            res["awake"].append(log[0].minute)
        elif "falls asleep" in text:
            res["asleep"].append(log[0].minute)
    data.append(dict(res))

    return data


def build_guard_objects(logs):
    guard_pool = []
    for night in logs:
        if night["id"] in guard_pool:
            index = guard_pool.index(night["id"])
            for asleep, awake in zip(night["asleep"], night["awake"]):
                guard_pool[index].add_entry(asleep, awake)
        else:
            guard = Guard(
                night["id"],
                night["asleep"].pop(0),
                night["awake"].pop(0),
            )
            for asleep, awake in zip(night["asleep"], night["awake"]):
                guard.add_entry(asleep, awake)
            guard_pool.append(guard)
    return guard_pool


def main():
    logs = [s for s in open("input.txt").read().split("\n") if s]
    data = read_logs(logs)
    organized_logs = organize_logs(data)
    guard_pool = build_guard_objects(organized_logs)
    most_asleep_guard = sorted(guard_pool, key=lambda x: x.time_asleep, reverse=True)[0]
    most_common_sleep_time = most_asleep_guard.most_asleep_time()
    gid = most_asleep_guard.id
    asleep_time = most_asleep_guard.time_asleep
    print(
        f"Most asleep guard is {gid} with {asleep_time} minutes asleep - most",
        f"commonly at minute {most_common_sleep_time}"
    )


main()
