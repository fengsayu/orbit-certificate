"""Print the 28 orbits of the root-fixing S_5 action on X_5."""

from itertools import permutations, product


def format_vertex(vertex):
    """Format a vertex as (epsilon;z1z2z3z4)."""
    return "({};{})".format(vertex[0], "".join(map(str, vertex[1:])))


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


def main():
    # Each line contains the orbit index, size, and sorted vertex list.
    for index, orbit in enumerate(build_orbits()):
        vertices = [format_vertex(vertex) for vertex in orbit]
        print("{}\t{}\t{}".format(index, len(orbit), vertices))


if __name__ == "__main__":
    main()
