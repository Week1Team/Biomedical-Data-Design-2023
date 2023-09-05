import numpy as np


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