import numpy as np
# -This module provides a drawlines function.
# -Given an array with max matched-zero number, the drawlines function try to use the fewest lines to cover all zeros.

# -The algorithm need this function to draw lines for the preparation of generating more zeros in next loop,
#       when the max matched-zero number is fewer than the docters.

# -The algorithm firstly marks the rows without matched-zero,
#       then marks the columns of the unmatched-zeros in newly-marked rows,  (function draw_col),
#       then marks the rows of the matched-zeros in newly-marked cols, (function draw_row),
#       Finally, when no more columns or rows can be marked, draw all marked columns and unmarked rows.


def draw_col(array, i, rows, cols, p):
    row = array[i]
    new_cols = list(set(np.where(row == 0)[0]) - set(np.where(p == i)[0]) - set(cols))
    if len(new_cols) != 0:
        cols += new_cols
        for j in new_cols:
            draw_row(array, j, rows, cols, p)


def draw_row(array, j, rows, cols, p):
    new_row = p[j]
    if new_row != -1 and sum(rows == new_row) == 0:
        rows.append(p[j])
        draw_col(array, p[j], rows, cols, p)


def drawLines(ranking, p):
    X = ranking.copy()
    marked_rows = []
    marked_cols = []
    new_rows = list(set(range(len(X))) - set(p))
    marked_rows += new_rows
    for i in new_rows:
        draw_col(ranking, i, marked_rows, marked_cols, p)
    row_lines = np.asarray(list(set(range(len(X))) - set(marked_rows)))
    col_lines = np.asarray(marked_cols)
    return row_lines, col_lines