import ray

from islands_desync.geneticAlgorithm.run_hpc.run_algorithm_params import (
    RunAlgorithmParams,
)
from islands_desync.islands.core.Computation import Computation
from islands_desync.islands.core.SignalActor import SignalActor
from islands_desync.islands.selectAlgorithm import SelectAlgorithm


@ray.remote
class Island:
    def __init__(self, island_id: int, select_algorithm: SelectAlgorithm):
        self.island_id: int = island_id
        self.computation = None
        self.islands: [Island] = []
        self.immigrants = []
        self.select_algorithm: SelectAlgorithm = select_algorithm

    def start(
        self, island_handle, islands: ["Island"], algorithm_params: RunAlgorithmParams, signal_actor: SignalActor
    ):
        self.islands = islands
        self.computation = Computation.remote(
            island_handle,
            self.island_id,
            islands,
            self.select_algorithm,
            algorithm_params,
            signal_actor
        )

        print("Comp created")

        return self.computation

    def receive_immigrant(self, immigrant_iteration):
        # print(
        #     "Wyspa %s: dostaje imigranta: %s"
        #     % (self.island_id, str(immigrant_iteration)[:10])
        # )
        self.immigrants.append(immigrant_iteration)

    def get_immigrants(self):
        return [self.immigrants.pop(0) for _ in self.immigrants]

    def __repr__(self):
        return "Island %s" % self.island_id
