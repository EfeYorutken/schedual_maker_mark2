class course:
    #Mo 13 - 16 Th 10 - 13
    def __init__(self, code, times, section, extra_fileds={}):
        self.code = code
        self.times = {}
        self.section = section
        self.extra_fileds = extra_fileds
        arr = times.split(" ")
        for i in range(0,len(arr), 4):
            self.times[arr[i]] = [int(arr[i+1]), int(arr[i+3])]


    def to_str(self):
        return f"{self.code}-{self.section}"

    def intersect(first, other):
        common_days = [x for x in list(first.times.keys()) if x in list(other.times.keys())]

        for day in common_days:
            tf = first.times[day]
            to = other.times[day]

            rf = set(range(tf[0], tf[1]))
            ro = set(range(to[0], to[1]))

            if rf.intersection(ro):
                return True

        return False
