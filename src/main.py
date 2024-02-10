import matplotlib.pyplot as plt
import seaborn as sns
import random
import click

# Set the Seaborn theme for styling
sns.set_theme()
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})


class Node:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def next_power_of_two(n):
    if n == 0:
        return 1
    n -= 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    return n + 1


def build_tournament_tree(teams):
    if len(teams) == 1:
        return Node(value=teams[0])
    elif not teams:
        return None
    mid = len(teams) // 2
    left_subtree = build_tournament_tree(teams[:mid])
    right_subtree = build_tournament_tree(teams[mid:])
    return Node(left=left_subtree, right=right_subtree)


def plot_tournament_tree(node, ax, x, y, dx, is_root=True):
    if node is not None:
        label = node.value if node.value else ""
        if is_root:
            label += "(Winner)"

        if label:
            ax.text(
                x,
                y,
                label,
                ha="center",
                va="center",
                fontsize=12,
                bbox=dict(
                    facecolor="lightblue", edgecolor="gray", boxstyle="round,pad=0.5"
                ),
            )

        if node.left or node.right:
            if node.left:
                next_x, next_y = x - dx, y - 0.1
                ax.plot([x, next_x], [y - 0.02, next_y + 0.02], "k-", lw=2)
                plot_tournament_tree(
                    node.left, ax, next_x, next_y, dx / 2, is_root=False
                )
            if node.right:
                next_x, next_y = x + dx, y - 0.1
                ax.plot([x, next_x], [y - 0.02, next_y + 0.02], "k-", lw=2)
                plot_tournament_tree(
                    node.right, ax, next_x, next_y, dx / 2, is_root=False
                )


if __name__ == "__main__":
    # List of team names for the example
    teams = click.prompt("Enter the team names separated by a space").split(",")
    random.shuffle(teams)
    complete_teams = teams + [None] * (next_power_of_two(len(teams)) - len(teams))
    tournament_root = build_tournament_tree(complete_teams)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis("off")
    plot_tournament_tree(tournament_root, ax, x=0.5, y=1, dx=0.25)

    plt.savefig("tournament_tree.png")
    plt.show()
