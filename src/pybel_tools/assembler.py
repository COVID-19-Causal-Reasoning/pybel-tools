"""Assembles a BEL graph into simple graphs."""

from typing import Callable, Iterable, List, Tuple

from pybel import BELGraph
from pybel.dsl import BaseEntity, Pathology, Protein
from pybel.struct.filters import invert_edge_predicate
from .filters.typing import EdgePredicate

Rows = Iterable[Tuple[str, str, str]]
EdgeHandler = Callable[[BELGraph, BaseEntity, BaseEntity, str], Rows]


class Assembler:
    #: A list of all of the possibilities
    wrapped_shit: List[Tuple[EdgePredicate, EdgeHandler]] = []

    @classmethod
    def decorate_my_shit(cls, edge_predicate: EdgePredicate):
        """"""

        def wrapper(edge_handler: EdgeHandler) -> EdgeHandler:
            """"""
            cls.wrapped_shit.append((edge_predicate, edge_handler))
            return edge_handler

        return wrapper

    @classmethod
    def get_it_done(cls, graph) -> Rows:
        for u, v, key in graph.edges(keys=True):
            for edge_predicate, edge_handler in cls.wrapped_shit:
                if edge_predicate(graph, u, v, key):
                    yield from edge_handler(graph, u, v, key)

