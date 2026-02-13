import numpy as np
import heapq


def a_star(grid, start, goal, e):
    # grid: your 512x512 numpy array
    height, width = grid.shape

    # Priority Queue: (priority, current_node)
    # priority = cost_so_far + heuristic_dist_to_goal
    pq = [(0, start)]

    came_from = {}
    cost_so_far = {start: 0}

    while pq:
        current_priority, current = heapq.heappop(pq)

        if current == goal:
            break

        # Explore 8 neighbors (including diagonals)
        for dx, dy in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]:
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < height and 0 <= neighbor[1] < width:
                # Calculate Movement Cost:
                # Distance (1 or 1.41) + Steepness Penalty
                dist = 1.41 if dx != 0 and dy != 0 else 1

                # Height Penalty: Multiply the absolute difference in height
                # Making this value high forces the path to stay level.
                height_diff = abs(grid[neighbor] - grid[current])
                penalty = (height_diff * 1000) ** e

                new_cost = cost_so_far[current] + dist + penalty

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    # Heuristic: Euclidean distance to goal
                    priority = new_cost + np.linalg.norm(
                        np.array(neighbor) - np.array(goal)
                    )
                    heapq.heappush(pq, (priority, neighbor))
                    came_from[neighbor] = current

    # Reconstruct path
    path = []
    curr = goal
    while curr != start:
        path.append(curr)
        curr = came_from[curr]
    path.append(start)
    return path[::-1]


# Usage
data = np.load("sparse_hills_map0.npy")
path = a_star(data, (250, 250), (780, 1003), 8)

from PIL import Image, ImageDraw

# Load your colored map from the previous step
img = Image.open("sparse_hills0.png").convert("RGB")
draw = ImageDraw.Draw(img)

# Convert path coordinates to (x, y) for PIL
# path is [(y, x), ...] so we swap them
line_path = [(p[1], p[0]) for p in path]

# Draw a thick white line for the path
draw.line(line_path, fill=(255, 255, 255), width=3)
img.save("map_with_path0.png")
