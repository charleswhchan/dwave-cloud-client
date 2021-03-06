from __future__ import absolute_import, print_function

import unittest
import itertools

from dwave.cloud.coders import encode_bqm_as_qp
from dwave.cloud.qpu import Solver


def get_solver():
    data = {
        "properties": {
            "supported_problem_types": ["qubo", "ising"],
            "qubits": [0, 1, 2, 3],
            "couplers": [(0, 1), (1, 2), (2, 3), (3, 0)],
            "num_qubits": 4,
            "parameters": {"num_reads": "Number of samples to return."}
        },
        "id": "test-solver",
        "description": "A test solver"
    }
    return Solver(client=None, data=data)


class TestCoders(unittest.TestCase):

    def test_qpu_request_encoding(self):
        solver = get_solver()
        linear = {index: 1 for index in solver.nodes}
        quadratic = {key: -1 for key in solver.undirected_edges}
        request = encode_bqm_as_qp(solver, linear, quadratic)
        self.assertEqual(request['format'], 'qp')
        self.assertEqual(request['lin'],  'AAAAAAAA8D8AAAAAAADwPwAAAAAAAPA/AAAAAAAA8D8=')
        self.assertEqual(request['quad'], 'AAAAAAAA8L8AAAAAAADwvwAAAAAAAPC/AAAAAAAA8L8=')
