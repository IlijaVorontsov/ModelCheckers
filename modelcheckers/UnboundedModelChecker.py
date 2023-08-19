from Interpolant import Interpolant
from Solvers import ProofSolver, SAT
from BoundedModelChecker import BoundedModelChecker


class UnboundedModelChecker(BoundedModelChecker):
    def check(self):
        tick = 0
        while True:
            print(f"Checking tick {tick}")
            if not self.add_check(tick):
                return False

            if tick != 0 and self.invariantConverges(tick):
                return True
            tick += 1

    def invariantConverges(self, tick: int):
        solver = ProofSolver()
        solver.add_formula(self.circuit.clauses_gates(0))
        solver.add_formula(self.circuit.clauses_system(1))
        solver.add_formula(self.circuit.b)
        solver.add_clause(self.circuit.clause_output(tick))
        b = self.circuit.b & self.circuit.clause_output(tick)

        reachable = self.circuit.clauses_latches(0)

        round = 0

        while True:
            print(f"Checking round {round}")
            solver.add_formula(self.circuit.applySwitch(reachable, round))
            if solver.solve(assumptions=self.circuit.assumptions(round)) == SAT:
                return False

            # switches not in b, so dropped during interpolation
            interpolant = Interpolant("proof.trace", b).CNF
            interpolant = self.circuit.cnfAtTick(interpolant, 0)

            if ProofSolver.implies(interpolant, reachable):
                return True

            reachable = reachable | interpolant
            round += 1


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description='Run a bounded model checker on the given AIGER file')
    parser.add_argument('filename', type=str,
                        help='Filename of the AIGER file')

    args = parser.parse_args()

    if UnboundedModelChecker(args.filename).check():
        print("OK")
    else:
        print("FAIL")
