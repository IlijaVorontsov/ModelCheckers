from sat_logic.Solvers import Cadical, SAT
from sat_logic.AigerCircuit import AigerCircuit


class BoundedModelChecker:
    def __init__(self, aigerfile: str):
        self.circuit = AigerCircuit(aigerfile)
        self.aigerfile = aigerfile
        self.solver = Cadical()
        self.solver.add_clause([1])

    def add_check(self, k: int):
        self.solver.add_formula(self.circuit.clauses_system(k))
        if self.solver.solve(constraint=self.circuit.clause_output(k)) == SAT:
            return False
        return True

    def check(self, k: int):
        for i in range(0, k+1):
            if not self.add_check(i):
                print(f"{self.aigerfile},FAIL,{i},")
                return
        print(f"{self.aigerfile},OK,{k},")


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description='Run a bounded model checker on the given AIGER file')
    parser.add_argument('filename', type=str,
                        help='Filename of the AIGER file')
    parser.add_argument(
        'k', type=int, help='Number of steps to check for the safety property')

    args = parser.parse_args()
    BoundedModelChecker(args.filename).check(args.k)
