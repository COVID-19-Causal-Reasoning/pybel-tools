# -*- coding: utf-8 -*-

import logging
import os
from typing import Iterable, Optional

from bel_resources import write_namespace
from pybel import BELGraph
from pybel.struct.summary.node_summary import get_names_by_namespace
from ..summary.error_summary import get_incorrect_names_by_namespace, get_undefined_namespace_names

log = logging.getLogger(__name__)

__all__ = [
    'export_namespace',
    'export_namespaces',
]


def export_namespace(
        graph: BELGraph,
        namespace: str,
        directory: Optional[str] = None,
        cacheable: bool = False,
) -> None:
    """Export all names and missing names from the given namespace to its own BELNS file in the given directory.

    Could be useful during quick and dirty curation, where planned namespace building is not a priority.

    :param pybel.BELGraph graph: A BEL graph
    :param namespace: The namespace to process
    :param directory: The path to the directory where to output the namespace. Defaults to the current working
     directory returned by :func:`os.getcwd`
    :param cacheable: Should the namespace be cacheable? Defaults to ``False`` because, in general, this operation
     will probably be used for evil, and users won't want to reload their entire cache after each iteration of curation.
    """
    directory = os.getcwd() if directory is None else directory
    path = os.path.join(directory, f'{namespace}.belns')

    log.info('Outputting to %s', path)
    right_names = get_names_by_namespace(graph, namespace)
    log.info('Graph has %d correct names in %s', len(right_names), namespace)
    wrong_names = get_incorrect_names_by_namespace(graph, namespace)
    log.info('Graph has %d incorrect names in %s', len(wrong_names), namespace)
    undefined_ns_names = get_undefined_namespace_names(graph, namespace)
    log.info('Graph has %d names in missing namespace %s', len(undefined_ns_names), namespace)

    names = (right_names | wrong_names | undefined_ns_names)

    if 0 == len(names):
        log.warning(f'{namespace} is empty')

    with open(path, 'w') as file:
        write_namespace(
            namespace_name=namespace,
            namespace_keyword=namespace,
            namespace_domain='Other',
            author_name=graph.authors,
            author_contact=graph.contact,
            citation_name=graph.name,
            values=names,
            cacheable=cacheable,
            file=file,
        )


def export_namespaces(
        graph: BELGraph,
        namespaces: Iterable[str],
        directory: Optional[str] = None,
        cacheable: bool = False,
) -> None:
    """Wrap :func:`export_namespace` for an iterable of namespaces (thinly).

    :param graph: A BEL graph
    :param namespaces: An iterable of strings for the namespaces to process
    :param directory: The path to the directory where to output the namespaces. Defaults to the current working
     directory returned by :func:`os.getcwd`
    :param cacheable: Should the namespaces be cacheable? Defaults to ``False`` because, in general, this operation
     will probably be used for evil, and users won't want to reload their entire cache after each iteration of curation.
    """
    directory = os.getcwd() if directory is None else directory  # avoid making multiple calls to os.getcwd later
    for namespace in namespaces:
        export_namespace(graph, namespace, directory=directory, cacheable=cacheable)
