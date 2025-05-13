from typing import Set
import networkx as nx
import time

def simulate_broadcast_rounds(
    tree: nx.DiGraph,
    root: int,
    terminals: Set[int],
    timeout_seconds: float = 10.0  # Add timeout parameter with default 10 seconds
) -> int:
    """
    Simulate the telephone‐model broadcast on a directed multicast tree.

    Each round, every informed node may inform exactly one of its children.
    We continue until at least all `terminals` are informed, or no progress
    is possible.

    :param tree: a directed tree (DiGraph) rooted at `root`
    :param root: the root node index
    :param terminals: the set of terminals we care about (subset of tree nodes)
    :param timeout_seconds: maximum execution time in seconds
    :return: number of rounds taken to inform all terminals (or maximum reached)
    """
    # Start timer for timeout
    start_time = time.time()
    
    # Initialize informed set and filter out terminals not in the tree
    informed = {root}
    valid_terminals = set(n for n in terminals if n in tree)
    remaining = valid_terminals - informed
    
    # If all terminals are already informed or don't exist, return 0
    if not remaining:
        return 0
    
    # Special case: check if the tree is a bush tree with all terminals being leaves
    # Bush tree structure: all leaves are at the same depth from root
    is_bush_tree = True
    depths = {}
    
    # Iterative version of depth computation to avoid recursion errors
    stack = [(root, 0)]  # (node, depth) pairs
    iteration_count = 0
    max_iterations = 1000000  # Limit iterations to prevent infinite loops
    
    while stack and (time.time() - start_time < timeout_seconds) and iteration_count < max_iterations:
        iteration_count += 1
        node, depth = stack.pop()
        depths[node] = depth
        # Add successors to stack in reverse order to maintain original traversal order
        for child in reversed(list(tree.successors(node))):
            stack.append((child, depth + 1))
    
    # If we hit timeout or iteration limit during depth computation
    if time.time() - start_time >= timeout_seconds or iteration_count >= max_iterations:
        print(f"Depth computation timed out after {time.time() - start_time:.2f}s")
        return -1  # Indicate timeout
    
    # Check if all terminals are leaves and at the same depth
    if valid_terminals and all(tree.out_degree(t) == 0 for t in valid_terminals):
        # Verify all terminals have the same depth
        target_depth = None
        for t in valid_terminals:
            if t in depths:
                if target_depth is None:
                    target_depth = depths[t]
                elif depths[t] != target_depth:
                    is_bush_tree = False
                    break
            else:
                is_bush_tree = False
                break
        
        # If it's a bush tree, return the depth as the round count
        if is_bush_tree and target_depth is not None:
            return target_depth
        
    # Regular simulation for non-bush trees
    rounds = 0
    # Precompute children lists for fast access
    children = {u: list(tree.successors(u)) for u in tree.nodes()}
            
    # Continue until no terminals left or no one can inform
    max_rounds = 1000  # Limit rounds to prevent infinite loops
    while remaining and rounds < max_rounds and (time.time() - start_time < timeout_seconds):
        rounds += 1
        new_informed = set()

        # Each informed node picks one uninformed child (if any)
        for u in list(informed):
            for v in children.get(u, []):
                if v not in informed:
                    new_informed.add(v)
                    break

        # If no new nodes got informed, stop early
        if not new_informed:
            break

        informed |= new_informed
        remaining -= new_informed
    
    # If we hit timeout or round limit
    if time.time() - start_time >= timeout_seconds:
        print(f"Simulation timed out after {time.time() - start_time:.2f}s")
        return -2  # Indicate simulation timeout
    
    if rounds >= max_rounds:
        print(f"Simulation exceeded maximum rounds ({max_rounds})")
        return -3  # Indicate max rounds reached

    return rounds
