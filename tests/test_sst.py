# -*- coding: utf-8 -*-


import logging
from pybel.constants import *
from pybel_tools.analysis.sst import run_cna
from tests.constants import ExampleNetworkMixin, ManagerMixin

HGNC = 'HGNC'

log = logging.getLogger(__name__)
log.setLevel(10)


class SstTest(ExampleNetworkMixin):
    def test_cna(self):
        test_network = self.network3  # Defined in test.constants.TestNetworks

        a_as_root = run_cna(graph=test_network, root=(PROTEIN, HGNC, 'a'), targets=[(GENE, HGNC, 'c')])

        self.assertEqual(-1, a_as_root[0][2].value)  # A -| C

        d_as_root = run_cna(graph=test_network, root=(RNA, HGNC, 'd'), targets=[(GENE, HGNC, 'c'), (GENE, HGNC, 'f')])

        self.assertEqual(-1, d_as_root[0][2].value)  # D -| C
        self.assertEqual(-1, d_as_root[1][2].value)  # A -| F

        e_as_root = run_cna(graph=test_network, root=(PROTEIN, HGNC, 'e'),
                            targets=[(GENE, HGNC, 'c'), (GENE, HGNC, 'f')])

        self.assertEqual(1, e_as_root[0][2].value)  # E -> C
        self.assertEqual(1, e_as_root[1][2].value)  # E -> F

        failed_results = run_cna(graph=test_network, root=(PROTEIN, HGNC, 'e'), targets=[(PROTEIN, HGNC, 'g')])

        self.assertEqual(0, failed_results[0][2].value)  # E -> G