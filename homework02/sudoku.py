import pathlib
import typing as tp
from copy import deepcopy
import random

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    return [values[i*n:(i+1)*n] for i in range(n)]

def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    arr = []
    for i in range(len(grid)):
        arr.append(grid[i][pos[1]])
    return arr


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    ifirst = pos[0] // 3 * 3
    isecond = pos[1] // 3 * 3
    arr = []
    for i in range(ifirst, ifirst+3):
        for j in range(isecond, isecond+3):
            arr.append(grid[i][j])
    return arr


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    n = len(grid)
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '.':
                return (i, j)
    return -1

def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    row_vals = set(get_row(grid, pos))
    col_vals = set(get_col(grid, pos))
    blk_vals = set(get_block(grid, pos))
    all_vals = set(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
    all_vals -= row_vals
    all_vals -= col_vals
    all_vals -= blk_vals
    return all_vals


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    pos = find_empty_positions(grid)
    if pos == -1:
        return grid
    nums = find_possible_values(grid, pos)
    for num in nums:
        grid[pos[0]][pos[1]] = num
        if solve(grid):
            return solve(grid)
    grid[pos[0]][pos[1]] = '.'
def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    clist = set()
    rlist = set()
    blist = set()
    #print(solution)
    n = len(solution[0])
    for i in range(n):
        for j in get_col(solution, (0, i)):
            if j not in clist:
                clist.add(j)
        if len(clist) != 9:
            return False
        for j in get_row(solution, (i, 0)):
            if j not in rlist:
                rlist.add(j)
        if len(rlist) != 9:
            return False
    for i in range(0, n, 3):
        for j in range(0, n, 3):
            for k in get_block(solution, (i, j)):
                if k not in blist:
                    blist.add(k)
            if len(blist) != 9:
                return False
    if '.' in clist or '.' in rlist or '.' in blist:
        return False
    return True

def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    sudoku = [['.'] * 9 for i in range(9)]
    i = 0
    while i < 9:
        j = random.randint(0, 8)
        impossible = get_block(sudoku, (i, i))
        n = str(random.randint(1, 9))
        dots = impossible.count('.')
        for K in range(dots):
            impossible.remove('.')

        if n not in impossible:
            sudoku[i][i] = n
            i += 1

    sudoku = solve(sudoku)
    M = 81 - N
    while M > 0:
        i, j = random.randint(0, 8), random.randint(0, 8)
        if sudoku[i][j] == '.':
            continue
        else:
            sudoku[i][j] = '.'
            M -= 1
    return sudoku

if __name__ == "__main__":
   for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
       grid = read_sudoku(fname)
       display(grid)
       solution = solve(grid)
       if not solution:
           print(f"Puzzle {fname} can't be solved")
       else:
           display(solution)
