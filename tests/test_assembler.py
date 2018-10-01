"""Assembles a BEL graph into simple graphs."""

import unittest

from pybel import BELGraph
from pybel.dsl import BaseEntity, Pathology, Protein
from pybel.struct.filters import invert_edge_predicate
from pybel_tools.assembler import Assembler, Rows


def is_ppi(graph: BELGraph, u: BaseEntity, v: BaseEntity, key: str) -> bool:
    return isinstance(u, Protein) and isinstance(v, Protein)


class ExamplePPIAssembler(Assembler):
    """"""

    @decorate_my_shit(is_ppi)
    @staticmethod
    def ppi_handler(graph: BELGraph, u: BaseEntity, v: BaseEntity, key: str) -> Rows:
        yield str(u), 'ppi', str(v)

    @decorate_my_shit(invert_edge_predicate(is_ppi))
    @staticmethod
    def not_ppi_handler(graph: BELGraph, u: BaseEntity, v: BaseEntity, key: str) -> Rows:
        pass


class TestAssembler(unittest.TestCase):

    def test_it(self):
        graph = BELGraph()
        graph.add_increases(Protein('HGNC', 'A'), Protein('HGNC', 'B'), '', '')
        graph.add_increases(Protein('HGNC', 'A'), Pathology('HGNC', 'B'), '', '')

        for row in ExamplePPIAssembler.get_it_done(graph):
            print(*row)
