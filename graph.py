class graph:
    def __init__(self):
        self.mapping = {}
        self.num = 0

    def add_courses(self, arr):
        for a in arr:
            self.mapping[a] = []

    def connect_courses_w_fn_priv(self, current, visited,fun):
        visited.append(current)
        temp = []

        for unvisited in [uv for uv in list(self.mapping.keys()) if uv not in visited]:
            if for_all(lambda x : fun(x,unvisited), visited) and (unvisited not in self.mapping[current]):
                temp.append(unvisited)
                self.mapping[current].append(unvisited)
                self.mapping[unvisited].append(current)

            for nxt in temp:
                self.connect_courses_w_fn_priv(nxt,visited,fun)


    def connect_courses_w_fn(self, fun):
        for x in list(self.mapping.keys()):
            self.connect_courses_w_fn_priv(x,[], fun)

    def get_prog_priv(self, current, visited):
        res = []

        print(f"\tcostructing program {self.num}")

        self.num += 1

        visited.append(current)

        for unvisited in [uv for uv in self.mapping[current] if uv not in visited]:
            rec_res = self.get_prog_priv(unvisited, visited)
            for r in rec_res:
                res.append(r)

        if len(res) == 0:
            res.append([current])
        else:
            for prog in res:
                prog.insert(0,current)

        return res

    def get_progs(self):
        first = list(self.mapping.keys())[0]
        return self.get_prog_priv(first, [])



    def score_program(program, fn_list):
        res = 0

        for fn in fn_list:
            if fn(program):
                res += 1

        return res

def for_all(fn, arr):
    for x in arr:
        if not fn(x):
            return False
    return True
