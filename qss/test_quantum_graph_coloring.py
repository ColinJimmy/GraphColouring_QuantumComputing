import unittest
from unittest.mock import patch

from quantum_graph_coloring import QuantumGraphColoring


class TestQuantumGraphColoring(unittest.TestCase):
    def test_is_valid_coloring(self):
        edges = [(0, 1), (1, 2)]
        qgc = QuantumGraphColoring(edges, num_vertices=3, num_colors=3)
        self.assertTrue(qgc._is_valid_coloring([0, 1, 0]))
        self.assertFalse(qgc._is_valid_coloring([1, 1, 2]))

    def test_extract_coloring(self):
        qgc = QuantumGraphColoring(edges=[(0, 1)], num_vertices=2, num_colors=3)  # 2 bits per vertex
        self.assertEqual(qgc._extract_coloring("0001"), [0, 1])
        self.assertEqual(qgc._extract_coloring("1110"), [3 % 3, 2 % 3])  # modulo num_colors

    def test_execute_with_mocked_counts(self):
        # Prepare deterministic counts: one valid coloring (0,1) for edge (0,1)
        counts = {"01": 5, "00": 3}

        class DummyResult:
            def get_counts(self_inner):
                return counts

        class DummyJob:
            def result(self_inner):
                return DummyResult()

        class DummySimulator:
            def run(self_inner, qc, shots):
                return DummyJob()

        edges = [(0, 1)]
        qgc = QuantumGraphColoring(edges, num_vertices=2, num_colors=2)
        qgc.simulator = DummySimulator()

        with patch("qss.quantum_graph_coloring.transpile", lambda qc, backend: qc):
            result = qgc.execute(shots=8, num_iterations=1)

        self.assertEqual(result["total_shots"], 8)
        self.assertEqual(result["num_valid_solutions"], 1)
        self.assertEqual(result["valid_colorings"], {(0, 1): 5})
        self.assertEqual(result["best_coloring"], (0, 1))
        self.assertEqual(result["num_colors_used"], 2)


if __name__ == "__main__":
    unittest.main()
