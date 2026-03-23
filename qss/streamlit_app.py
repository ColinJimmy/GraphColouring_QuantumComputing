import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))

from execute import (  # noqa: E402
    MAX_SIMULATOR_QUBITS,
    default_stress_graph,
    max_vertices_for_colors,
    run_graph_coloring,
)


def parse_edges(raw_text, num_vertices):
    """Parse edges from text input: one edge per line as 'u v' or 'u,v'."""
    edges = []
    for line_number, raw_line in enumerate(raw_text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue

        line = line.replace("(", "").replace(")", "")
        if "," in line:
            parts = [p.strip() for p in line.split(",") if p.strip()]
        else:
            parts = [p.strip() for p in line.split() if p.strip()]

        if len(parts) != 2:
            raise ValueError(
                f"Invalid edge format at line {line_number}: '{raw_line}'. "
                "Use 'u v' or 'u,v'."
            )

        u = int(parts[0])
        v = int(parts[1])
        if u < 0 or v < 0 or u >= num_vertices or v >= num_vertices:
            raise ValueError(
                f"Edge ({u}, {v}) is out of range for vertices 0..{num_vertices - 1}."
            )
        edges.append((u, v))

    return edges


def format_edges_for_textarea(edges):
    return "\n".join(f"{u},{v}" for u, v in edges)


def build_complete_graph_edges(num_vertices):
    edges = []
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            edges.append((i, j))
    return edges


def main():
    st.set_page_config(page_title="Quantum Graph Coloring", page_icon="Q", layout="wide")
    st.title("Quantum Graph Coloring - Streamlit UI")
    st.caption(
        "Interactive UI for setting vertices, colors, and edges, then running the "
        "Qiskit-based graph coloring solver."
    )

    default_edges, default_vertices, default_colors = default_stress_graph()

    with st.sidebar:
        st.header("Solver Settings")

        num_colors = st.number_input(
            "Number of colors",
            min_value=2,
            max_value=8,
            value=default_colors,
            step=1,
        )
        max_vertices_allowed = max_vertices_for_colors(num_colors)

        st.info(
            "Max vertices for current color count: "
            f"{max_vertices_allowed} (qubit budget: {MAX_SIMULATOR_QUBITS})"
        )

        default_vertex_value = min(default_vertices, max_vertices_allowed)
        num_vertices = st.number_input(
            "Number of vertices",
            min_value=2,
            max_value=max_vertices_allowed,
            value=default_vertex_value,
            step=1,
        )

        shots = st.number_input("Shots", min_value=1, max_value=20000, value=1024, step=128)
        num_iterations = st.number_input(
            "Amplitude amplification iterations",
            min_value=1,
            max_value=6,
            value=2,
            step=1,
        )

    st.subheader("Graph Edges")
    st.write(
        "Enter one edge per line as `u,v` or `u v`. "
        f"Vertex ids must be in range `0..{num_vertices - 1}`."
    )

    if "edges_text" not in st.session_state:
        st.session_state["edges_text"] = format_edges_for_textarea(default_edges)

    col1, col2 = st.columns([2, 1])

    with col1:
        edges_text = st.text_area(
            "Edges",
            value=st.session_state["edges_text"],
            height=320,
            help="Example:\n0,1\n1,2\n2,0",
        )

    with col2:
        st.markdown("**Quick graph generators**")
        if st.button("Load stress graph", use_container_width=True):
            stress_edges, stress_vertices, _ = default_stress_graph()
            if stress_vertices > max_vertices_allowed:
                st.warning(
                    "Stress graph needs more vertices than allowed for current colors. "
                    "Increase colors or lower vertices."
                )
            else:
                st.session_state["edges_text"] = format_edges_for_textarea(stress_edges)
                st.success("Loaded stress graph edges in editor.")
                st.rerun()

        if st.button("Load complete graph K_n", use_container_width=True):
            complete_edges = build_complete_graph_edges(num_vertices)
            st.session_state["edges_text"] = format_edges_for_textarea(complete_edges)
            st.success(f"Loaded complete graph with {len(complete_edges)} edges.")
            st.rerun()

        if st.button("Clear edges", use_container_width=True):
            st.session_state["edges_text"] = ""
            st.rerun()

    run_clicked = st.button("Run quantum graph coloring", type="primary", use_container_width=True)

    if run_clicked:
        try:
            parsed_edges = parse_edges(edges_text, num_vertices)
            result = run_graph_coloring(
                edges=parsed_edges,
                num_vertices=num_vertices,
                num_colors=num_colors,
                shots=shots,
                num_iterations=num_iterations,
            )
        except Exception as exc:
            st.error(f"Execution failed: {exc}")
            return

        st.success("Execution completed.")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Vertices", result["num_vertices"])
        m2.metric("Edges", result["num_edges"])
        m3.metric("Valid colorings", result["num_valid_solutions"])
        m4.metric("Qubits used", f"{result['qubits_used']} / {result['max_qubits']}")

        st.subheader("Result Summary")
        st.write(f"Colors attempted: **{result['num_colors']}**")
        st.write(f"Total shots: **{result['total_shots']}**")

        if result["best_coloring"] is not None:
            st.write(f"Best coloring: `{result['best_coloring']}`")
            st.write(f"Colors used in best coloring: **{result['num_colors_used']}**")
        else:
            st.warning("No valid coloring found in this run.")

        st.subheader("All valid colorings")
        if result["valid_colorings"]:
            rows = [
                {"coloring": str(coloring), "count": count}
                for coloring, count in sorted(result["valid_colorings"].items())
            ]
            st.dataframe(rows, use_container_width=True)
        else:
            st.info("No valid colorings to display.")
if __name__ == "__main__":
    main()
