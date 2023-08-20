
from sat_logic.Interpolant import Interpolant, SATException
try:
    from modelcheckers.BoundedModelChecker import BoundedModelChecker
except ModuleNotFoundError:
    from BoundedModelChecker import BoundedModelChecker

from sat_logic.ColoredLogic import ColorfulCNF
from sat_logic.Logic import CNF


class UnboundedModelChecker(BoundedModelChecker):
    def check(self):
        tick = 0
        while True:
            if not self.add_check(tick):
                print(f"Tick: {tick} @ 0")
                return False

            if tick != 0 and self.invariantConverges(tick):
                return True
            tick += 1

    def invariantConverges(self, tick: int):
        reachable = self.circuit.clauses_latches(0)
        transition1 = self.circuit.clauses_gates(
            0) & self.circuit.clauses_system(1)
        rest = self.circuit.b & CNF(self.circuit.clause_output(tick))

        round = 0
        while True:
            print(f"Tick: {tick} @{round}", end="\r")
            try:
                interpolant = Interpolant(ColorfulCNF(
                    [reachable & transition1, rest]))
                interpolant = interpolant.cnf
            except SATException:
                return False

            interpolant = self.circuit.cnfAtTick(interpolant, 0)

            if interpolant.implies(reachable):
                print(f"Tick: {tick} @{round}")
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
