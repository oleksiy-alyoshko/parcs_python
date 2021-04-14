from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

        matrix, vector = self.read_input()
        n_row, n_col = len(matrix), len(matrix[0])
        step = int(n_row / len(self.workers))

        # map
        mapped = []
        for i in xrange(0, len(self.workers)):
            print("map %d" % i)
            if i == len(self.workers) - 1:
                mapped.append(self.workers[i].mymap(matrix[i * step:], vector[i * step:], n_row - step * i))
            else:
                mapped.append(self.workers[i].mymap(matrix[i * step:(i + 1) * step], vector[i * step:(i + 1) * step], step))

        # reduce
        result = self.reduce_files(mapped)

        # output
        self.write_output(result)


        print("Job Finished")


    @staticmethod
    @expose
    def mymap(matrix, vector, length):
        chunk = []
        for i in range(length):
            curr_row = matrix[i]
            s = 0
            for j in range(length):
                s += curr_row[j] * vector[j]
            chunk.append(s)
        return chunk

    @staticmethod
    @expose
    def reduce_files(mapped):
        print("reduce")
        output = []

        for val in mapped:
            print("reduce loop")
            output = output + val.value
        print("reduce done")
        return output

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            a, b = [int(x) for x in f.readline().split()]
            matrix = [[int(x) for x in f.readline().split()] for _ in range(a)]
            vector = [int(f.readline()) for _ in range(b)]
        return matrix, vector

    def write_output(self, output):
        with open(self.output_file_name, 'w') as f:
            for j in range(len(output)):
                f.write(str(output[j]))
                f.write('\n')
        print("output done")