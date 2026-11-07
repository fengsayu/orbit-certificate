"""Compute and print the 28-by-28 orbit neighbor-count matrix Q."""

from itertools import permutations, product


def permute_vertex(vertex, permutation):
    """Move coordinate i to position permutation[i] in the encoding Psi."""
    epsilon = vertex[0]
    z = vertex[1:]
    encoded = ((epsilon - sum(z)) % 4,) + z
    permuted = [0] * 5
    for source, target in enumerate(permutation):
        permuted[target] = encoded[source]
    return (epsilon,) + tuple(permuted[1:])


def build_orbits():
    """Order the orbits by their lexicographically smallest vertices."""
    group = tuple(permutations(range(5)))
    remaining = {
        (epsilon,) + z
        for epsilon in range(2)
        for z in product(range(4), repeat=4)
    }
    orbits = []
    while remaining:
        representative = min(remaining)
        orbit = sorted({permute_vertex(representative, p) for p in group})
        if not set(orbit).issubset(remaining):
            raise ValueError("The generated orbits are not disjoint.")
        orbits.append(orbit)
        remaining.difference_update(orbit)

    if len(orbits) != 28 or sum(map(len, orbits)) != 512:
        raise ValueError("Unexpected orbit count or total vertex count.")
    return orbits


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


def build_matrix(orbits):
    """Count neighbors per vertex and verify every vertex in every orbit."""
    orbit_index = {
        vertex: index
        for index, orbit in enumerate(orbits)
        for vertex in orbit
    }

    def neighbor_counts(vertex):
        counts = [0] * len(orbits)
        for other in neighbors(vertex):
            counts[orbit_index[other]] += 1
        return counts

    matrix = []
    for orbit in orbits:
        row = neighbor_counts(orbit[0])
        if sum(row) != 5:
            raise ValueError("A row of Q does not sum to five.")
        if any(neighbor_counts(vertex) != row for vertex in orbit):
            raise ValueError("Neighbor counts are not constant on an orbit.")
        matrix.append(row)

    # Count the edges between two orbits in both directions.
    for i, orbit_i in enumerate(orbits):
        for j, orbit_j in enumerate(orbits):
            if len(orbit_i) * matrix[i][j] != len(orbit_j) * matrix[j][i]:
                raise ValueError("The orbit edge-balance identity fails.")
    return matrix


def main():
    # Row and column indices both start at zero.
    matrix = build_matrix(build_orbits())
    print("[")
    for row in matrix:
        print("    {!r},".format(row))
    print("]")


if __name__ == "__main__":
    main()
