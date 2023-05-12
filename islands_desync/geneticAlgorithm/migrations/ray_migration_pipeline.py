from typing import Dict, List

import ray

from islands_desync.geneticAlgorithm.migrations.ray_migration import RayMigration
from islands_desync.islands.core.Emigration import Emigration


class RayMigrationPipeline(RayMigration):
    def __init__(self, islandActor, emigration: Emigration):
        super().__init__(islandActor, emigration)
        self.new_individuals_refs = self.islandActor.get_immigrants.remote()

    def receive_individuals(
        self, step_num: int, evaluations: int
    ) -> (List, Dict | None):
        new_individuals = ray.get(self.new_individuals_refs)
        self.new_individuals_refs = self.islandActor.get_immigrants.remote()

        new_individuals, migrant_iteration_numbers = zip(*new_individuals)

        migration_at_step_num = {
            "step": step_num,
            "ev": evaluations,
            "iteration_numbers": migrant_iteration_numbers,
        }

        return list(new_individuals), migration_at_step_num