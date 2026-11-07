"""Print the sorted adjacency list of X_5 as a nested Python list."""

from itertools import product


def format_vertex(vertex):
    """Format a vertex as (epsilon;z1z2z3z4)."""
    return "({};{})".format(vertex[0], "".join(map(str, vertex[1:])))


def neighbors(vertex):
    """Use +e_i on side 0 and -e_i on side 1, modulo 4."""
    epsilon = vertex[0]
    z = vertex[1:]
    result = [(1 - epsilon,) + z]
    step = 1 if epsilon == 0 else -1
    for coordinate in range(4):
        shifted = list(z)
        shifted[coordinate] = (shifted[coordinate] + step) % 4
        result.append((1 - epsilon,) + tuple(shifted))
    return sorted(result)


def build_adjacency_list():
    """Sort both the vertices and the five neighbors of each vertex."""
    vertices = [
        (epsilon,) + z
        for epsilon in range(2)
        for z in product(range(4), repeat=4)
    ]
    adjacency = {vertex: neighbors(vertex) for vertex in vertices}
    for vertex, adjacent in adjacency.items():
        if len(set(adjacent)) != 5 or vertex in adjacent:
            raise ValueError("Unexpected degree or self-loop.")
        if any(vertex not in adjacency[other] for other in adjacent):
            raise ValueError("The adjacency relation is not symmetric.")
    return [
        [format_vertex(vertex), [format_vertex(other) for other in adjacency[vertex]]]
        for vertex in vertices
    ]


def main():
    # The complete output is a valid Python list with one vertex per row.
    print("[")
    for row in build_adjacency_list():
        print("    {!r},".format(row))
    print("]")


if __name__ == "__main__":
    main()
