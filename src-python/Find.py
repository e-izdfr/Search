import math
import copy
from Board import Board
from Cell import Cell

class Find:
    def __init__(self, board: Board):
        self.board = board
        self.source = self.__find_source()
        self.goal = self.__find_goal()
        self.explored = []

    def __find_source(self):
        for row in range(self.board.m):
            for col in range(self.board.n):
                if self.__get_opt(row, col).lower() == 's':
                    return [row, col]

    def __find_goal(self):
        for row in range(self.board.m):
            for col in range(self.board.n):
                if self.__get_opt(row, col).lower() == 'g':
                    return [row, col]

    def __get_opt(self, row: int, col: int) -> str:
        return self.board.cells[row][col][0].lower()

    def __get_number(self, row: int, col: int) -> int:
        return int(self.board.cells[row][col][1:])

    def __successor(self, cell: Cell) -> list:
        cells = []
        if cell.row > 0:
            if self.__get_opt(cell.row - 1, cell.col) != 'w':
                c = Cell(cell.row - 1, cell.col, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if not self.explored.__contains__(c.__hash__()):
                    cells.append(c)

        if cell.col > 0:
            if self.__get_opt(cell.row, cell.col - 1) != 'w':
                c = Cell(cell.row, cell.col - 1, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if not self.explored.__contains__(c.__hash__()):
                    cells.append(c)

        if cell.row < self.board.m - 1:
            if self.__get_opt(cell.row + 1, cell.col) != 'w':
                c = Cell(cell.row + 1, cell.col, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if not self.explored.__contains__(c.__hash__()):
                    cells.append(c)

        if cell.col < self.board.n - 1:
            if self.__get_opt(cell.row, cell.col + 1) != 'w':
                c = Cell(cell.row, cell.col + 1, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if not self.explored.__contains__(c.__hash__()):
                    cells.append(c)

        return cells

    def __cal_opt(self, path_sum, goal_value, row, col, g=0):
        opt = self.__get_opt(row, col)

        if opt == '+':
            path_sum += self.__get_number(row, col)
            g_value = 2 + g
            f_value = g_value + Find.h(self, row, col)
            
        elif opt == '-':
            path_sum -= self.__get_number(row, col)
            g_value = 1 + g
            f_value = g_value + Find.h(self, row, col)
            
        elif opt == '*':
            path_sum *= self.__get_number(row, col)
            g_value = 5 + g
            f_value = g_value + Find.h(self, row, col)
            
        elif opt == '^':
            path_sum **= self.__get_number(row, col)
            g_value = 11 + g
            f_value = g_value + Find.h(self, row, col)
            
        elif opt == 'a':
            goal_value += self.__get_number(row, col)
            g_value = 1 + g
            f_value = g_value + Find.h(self,row, col)
            
        elif opt == 'b':
            goal_value -= self.__get_number(row, col)
            g_value = 2 + g
            f_value = g_value + Find.h(self, row, col)
            
        else:
            g_value = 1 + g
            f_value = g_value + Find.h(self, row, col)

        return path_sum, goal_value, g_value, f_value

    def __check_goal(self, cell: Cell) -> bool:
        if cell.path_value > cell.goal_value:
            self.__print_solution(cell)
            return True
        return False

    def bfs_search(self):
        queue = []

        queue.append(
            Cell(self.source[0], self.source[1], [[False for x in range(self.board.n)] for y in range(self.board.m)],
                 self.__get_number(self.source[0], self.source[1]),
                 self.__get_number(self.goal[0], self.goal[1]), []))

        queue[0].path.append(queue[0])

        while len(queue) > 0:
            cell = queue.pop(0)
            self.explored.append(cell.__hash__())
            neighbors = self.__successor(cell)

            for c in neighbors:
                if c.row == self.goal[0] and c.col == self.goal[1]:
                    if self.__check_goal(cell):
                        return
                else:
                    if not cell.table[c.row][c.col]:
                        queue.append(c)

        print('no solution!!!')
            
    def __print_solution(self, cell: Cell):
        print(len(cell.path))

        cell.path.pop(0)

        for p in cell.path:
            print(str(p.row + 1) + ' ' + str(p.col + 1))

        print(str(self.goal[0] + 1) + ' ' + str(self.goal[1] + 1))
    
    frontier1 = []
    frontier2 = []   
    rest_of_frontier1 = []
    rest_of_frontier2 = []
    frontier = []
    m = math.inf
        
    def __successor1(self, cell: Cell) -> list:
            cells = []
            if cell.row > 0:
                if self.__get_opt(cell.row - 1, cell.col) != 'w':
                    c = Cell(cell.row - 1, cell.col, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                    c.path.append(c)
                    c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                    if not c in cell.path:
                        cells.append(c)

            if cell.col > 0:
                if self.__get_opt(cell.row, cell.col - 1) != 'w':
                    c = Cell(cell.row, cell.col - 1, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                    c.path.append(c)
                    c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                    if not c in cell.path:
                        cells.append(c)

            if cell.row < self.board.m - 1:
                if self.__get_opt(cell.row + 1, cell.col) != 'w':
                    c = Cell(cell.row + 1, cell.col, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                    c.path.append(c)
                    c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                    if not c in cell.path:
                        cells.append(c)

            if cell.col < self.board.n - 1:
                if self.__get_opt(cell.row, cell.col + 1) != 'w':
                    c = Cell(cell.row, cell.col + 1, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                    c.path.append(c)
                    c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                    if not c in cell.path:
                        cells.append(c)

            return cells
            
    def __successor2(self, cell: Cell) -> list:
        cells = []
        if cell.row > 0:
            if self.__get_opt(cell.row - 1, cell.col) != 'w':
                c = Cell(cell.row - 1, cell.col, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if not c in cell.path:
                    cells.append(c)

        if cell.col > 0:
            if self.__get_opt(cell.row, cell.col - 1) != 'w':
                c = Cell(cell.row, cell.col - 1, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if not c in cell.path:
                    cells.append(c)

        if cell.row < self.board.m - 1:
            if self.__get_opt(cell.row + 1, cell.col) != 'w':
                c = Cell(cell.row + 1, cell.col, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if not c in cell.path:
                    cells.append(c)

        if cell.col < self.board.n - 1:
            if self.__get_opt(cell.row, cell.col + 1) != 'w':
                c = Cell(cell.row, cell.col + 1, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if not c in cell.path:
                    cells.append(c)

        return cells
        
    def bidi_search(self):
        key = 0
        key2 = 0
        
        Find.frontier1 = []
        rest_of_frontier1 = []
        Find.frontier1.append(Cell(self.source[0], self.source[1], [[False for x in range(self.board.n)] for y in range(self.board.m)],
             self.__get_number(self.source[0], self.source[1]), self.__get_number(self.goal[0], self.goal[1]), []))
        Find.frontier1[0].path.append(Find.frontier1[0])
        
        Find.frontier2 = []
        rest_of_frontier2 = []
        Find.frontier2.append(Cell(self.goal[0], self.goal[1], [[False for x in range(self.board.n)] for y in range(self.board.m)], 0, 0
                                   ,[]))
        Find.frontier2[0].path.append(Find.frontier2[0])

        while(len(Find.frontier1) > 0 or len(Find.frontier2) > 0):
            cell1 = Find.frontier1.pop(0)
            rest_of_frontier1.append(cell1)
            neighbors = self.__successor1(cell1)
            
            for c in neighbors:
                Find.frontier1.append(c)
                for common1 in Find.frontier1:
                    for common2 in Find.frontier2 + rest_of_frontier2:
                        if common1.__eq__(common2):    
                            C = common1.path_value
                            l = common2.path[::-1]
                            del l[0]
                            for node in l:
                                if self.__get_opt(node.row, node.col) != 'a' and self.__get_opt(node.row, node.col) != 'b' \
                                and self.__get_opt(node.row, node.col) != 'g':
                                    if self.__get_opt(node.row, node.col) == '+':
                                        C += self.__get_number(node.row, node.col)
                                        
                                    elif self.__get_opt(node.row, node.col) == '-': 
                                        C -= self.__get_number(node.row, node.col)
                                        
                                    elif self.__get_opt(node.row, node.col) == '*':
                                        C *= self.__get_number(node.row, node.col)
                                        
                                    elif self.__get_opt(node.row, node.col) == '^':
                                        C = C**self.__get_number(node.row, node.col)
                                        
                            if self.__get_opt(common1.row, common1.col) == 'a':
                                if C > common1.goal_value + common2.goal_value \
                                - self.__get_number(common1.row, common1.col):
                                    key2 = 1
                                    for i in common1.path:
                                        for j in common2.path[:-1]:
                                            if i == j:
                                                key2 = 0
                                                break
                                            
                                        if key2 == 0:
                                            break
                                        
                                    if key2 == 1:
                                        print('The path_value(score) of the found solution is', C, 'which is greater than',
                                              common1.goal_value + common2.goal_value - self.__get_number(common1.row, common1.col))
                                        
                            elif self.__get_opt(common1.row, common1.col) == 'b':
                                if C > common1.goal_value + common2.goal_value \
                                + self.__get_number(common1.row, common1.col):
                                    key2 = 1
                                    for i in common1.path:
                                        for j in common2.path[:-1]:
                                            if i == j:
                                                key2 = 0
                                                break
                                            
                                        if key2 == 0:
                                            break
                                        
                                    if key2 == 1:
                                         print('The path_value(score) of the found solution is', C, 'which is greater than',
                                              common1.goal_value + common2.goal_value + self.__get_number(common1.row, common1.col))
                                         
                            else:
                                if C > common1.goal_value \
                                + common2.goal_value:
                                    key2 = 1
                                    for i in common1.path:
                                        for j in common2.path[:-1]:
                                            if i == j:
                                                key2 = 0
                                                break
                                            
                                        if key2 == 0:
                                            break
                                        
                                    if key2 == 1:
                                        print('The path_value(score) of the found solution is', C, 'which is greater than',
                                              common1.goal_value + common2.goal_value)
                            
                            if key2 == 1:
                                print('The length of the found solution is', len(common1.path) + len(common2.path) - 2)
                                print('(Note that the initial node is not displayed)')
                                common1.path.pop(0)
                                for p in common1.path:
                                    print(str(p.row + 1) + ' ' + str(p.col + 1))
                                common2.path.reverse()
                                common2.path.pop(0)
                                for p in common2.path:
                                    print(str(p.row + 1) + ' ' + str(p.col + 1))
                                key = 1
                                break
                            
                    if key == 1:
                        break
                    
                if key == 1:
                    break
                        
            if key == 1:
                break   

            cell2 = Find.frontier2.pop(0)
            rest_of_frontier2.append(cell2)
            neighbors = self.__successor2(cell2)
            
            for c in neighbors:
                Find.frontier2.append(c)
                for common2 in Find.frontier2:
                    for common1 in Find.frontier1 + rest_of_frontier1:
                        if common2.__eq__(common1):
                            C = common1.path_value
                            l = common2.path[::-1]
                            del l[0]
                            for node in l:
                                if self.__get_opt(node.row, node.col) != 'a' and self.__get_opt(node.row, node.col) != 'b' \
                                    and self.__get_opt(node.row, node.col) != 'g':
                                    if self.__get_opt(node.row, node.col) == '+':
                                        C += self.__get_number(node.row, node.col)
                                        
                                    elif self.__get_opt(node.row, node.col) == '-': 
                                        C -= self.__get_number(node.row, node.col)
                                        
                                    elif self.__get_opt(node.row, node.col) == '*':
                                        C *= self.__get_number(node.row, node.col)
                                        
                                    elif self.__get_opt(node.row, node.col) == '^':
                                        C = C**self.__get_number(node.row, node.col)
                                        
                            if self.__get_opt(common1.row, common1.col) == 'a':
                                if C > common1.goal_value + common2.goal_value \
                                - self.__get_number(common1.row, common1.col):
                                    key2 = 1
                                    for i in common1.path:
                                        for j in common2.path[:-1]:
                                            if i == j:
                                                key2 = 0
                                                break
                                            
                                        if key2 == 0:
                                            break
                                        
                                    if key2 == 1:
                                        print('The path_value(score) of the found solution is', C, 'which is greater than',
                                              common1.goal_value + common2.goal_value - self.__get_number(common1.row, common1.col))
                                        
                            elif self.__get_opt(common1.row, common1.col) == 'b':
                                if C > common1.goal_value + common2.goal_value \
                                + self.__get_number(common1.row, common1.col):
                                    key2 = 1
                                    for i in common1.path:
                                        for j in common2.path[:-1]:
                                            if i == j:
                                                key2 = 0
                                                break
                                            
                                        if key2 == 0:
                                            break
                                        
                                    if key2 == 1:
                                        print('The path_value(score) of the found solution is', C, 'which is greater than',
                                              common1.goal_value + common2.goal_value + self.__get_number(common1.row, common1.col))
                                        
                            else:
                                if C > common1.goal_value \
                                    + common2.goal_value:
                                        key2 = 1
                                        for i in common1.path:
                                            for j in common2.path[:-1]:
                                                if i == j:
                                                    key2 = 0
                                                    break
                                                
                                        if key2 == 0:
                                            break
                                        
                                        if key2 == 1:
                                            print('The path_value(score) of the found solution is', C, 'which is greater than',
                                              common1.goal_value + common2.goal_value)
                            
                            if key2 == 1:
                                print('The length of the found solution is', len(common1.path) + len(common2.path) - 2)
                                print('(Note that the initial node is not displayed)')
                                common1.path.pop(0)
                                for p in common1.path:
                                    print(str(p.row + 1) + ' ' + str(p.col + 1))
                                common2.path.reverse()
                                common2.path.pop(0)
                                for p in common2.path:
                                    print(str(p.row + 1) + ' ' + str(p.col + 1))
                                key = 1
                                break
                            
                    if key == 1:
                        break
                        
                if key == 1:
                    break
                
            if key == 1:
                break
    
    def __successor3(self, cell: Cell) -> list:
        cells = []
        if cell.row > 0:
            if self.__get_opt(cell.row - 1, cell.col) != 'w':
                c = Cell(cell.row - 1, cell.col, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if c not in cell.path:
                    cells.append(c)

        if cell.col > 0:
            if self.__get_opt(cell.row, cell.col - 1) != 'w':
                c = Cell(cell.row, cell.col - 1, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if c not in cell.path:
                    cells.append(c)

        if cell.row < self.board.m - 1:
            if self.__get_opt(cell.row + 1, cell.col) != 'w':
                c = Cell(cell.row + 1, cell.col, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if c not in cell.path:
                    cells.append(c)

        if cell.col < self.board.n - 1:
            if self.__get_opt(cell.row, cell.col + 1) != 'w':
                c = Cell(cell.row, cell.col + 1, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if c not in cell.path:
                    cells.append(c)

        return cells
    
    def __goal_test(self, cell: Cell) -> bool:
        if cell.row == self.goal[0] and cell.col == self.goal[1]:
            if cell.path_value > cell.goal_value:
                return True
        return False
    
    def recursive_DLS(self, cell, limit):
        if Find.__goal_test(self, cell):
            return cell
        
        elif limit == 0:
            return 'cutoff'
        
        else:
            cutoff_ocurred_or_not = False
            successors = Find.__successor3(self, cell)
            for i in range(0, len(successors)):
                result = Find.recursive_DLS(self, successors[-1], limit - 1)
                del(successors[-1])
                if result == 'cutoff':
                    cutoff_ocurred_or_not = True
                    
                elif result != 'failure':
                    return result
                
            if cutoff_ocurred_or_not:
                return 'cutoff'
            
            else:
                return 'failure'
            
    
    def DLS(self, limit):
        node = Cell(self.source[0], self.source[1],
                                        [[False for x in range(self.board.n)] for y in range(self.board.m)],
                                        self.__get_number(self.source[0], self.source[1]),
                                        self.__get_number(self.goal[0], self.goal[1]), [])
        node.path.append(node)
        return Find.recursive_DLS(self, node, limit)
    
    def __print_solution2(self, cell: Cell):
        print('The path_value(score) of the found solution is', cell.path_value, 'which is greater than', cell.goal_value)
        print('The length of the found solution is', len(cell.path) - 1)
        print('(Note that the initial node is not displayed)')

        cell.path.pop(0)
        
        print(cell.path_value)
        for p in cell.path:
            print(str(p.row + 1) + ' ' + str(p.col + 1))
    
    def IDDFS(self):
        depth = 0
        while True:
            result = Find.DLS(self, depth)
            if result != 'cutoff':
                break
            depth += 1
        if result == 'failure':
            print('No solution.')
            
        else:
            Find.__print_solution2(self, result)
        
    def __print_solution3(self, cell: Cell):
        print('The path_value(score) of the found solution is:', cell.path_value, 'which is greater than', cell.goal_value)
        print('The length of the found solution is', len(cell.path))
        print('(Note that the initial node is not displayed)')
        
        for p in cell.path:
            print(str(p.row + 1) + ' ' + str(p.col + 1))
    
    def __successor4(self, cell: Cell):
        if cell.row > 0:
            if self.__get_opt(cell.row - 1, cell.col) != 'w':
                c = Cell(cell.row - 1, cell.col, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col, cell.g)
                if c not in cell.path:
                    Find.frontier.append(c)
            
        if cell.col > 0:
            if self.__get_opt(cell.row, cell.col - 1) != 'w':
                c = Cell(cell.row, cell.col - 1, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col, cell.g)
                if c not in cell.path:
                    Find.frontier.append(c)

        if cell.row < self.board.m - 1:
            if self.__get_opt(cell.row + 1, cell.col) != 'w':
                c = Cell(cell.row + 1, cell.col, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col, cell.g)
                if c not in cell.path:
                    Find.frontier.append(c)

        if cell.col < self.board.n - 1:
            if self.__get_opt(cell.row, cell.col + 1) != 'w':
                c = Cell(cell.row, cell.col + 1, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value, c.g, c.f = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col, cell.g)
                if c not in cell.path:
                    Find.frontier.append(c)
    
    def h(self, row, col):
        return abs(row - self.goal[0]) + abs(col - self.goal[1])
    
    def A_star(self):
        key = 1
        Find.frontier = []
        initial_state = Cell(self.source[0], self.source[1], [[False for x in range(self.board.n)] for y in range(self.board.m)],
             self.__get_number(self.source[0], self.source[1]), self.__get_number(self.goal[0], self.goal[1]), [], 0)
        initial_state.f = Find.h(self, initial_state.row, initial_state.col)
        Find.frontier.append(initial_state)
        while True:
            if len(Find.frontier) == 0:
                key = 0
                break
            list_of_fs = [node.f for node in Find.frontier]
            index = list_of_fs.index(min(list_of_fs))
            cell = Find.frontier[index]
            del Find.frontier[index]
            if Find.__goal_test(self, cell):
                Find.__print_solution3(self, cell)
                break
            Find.__successor4(self, cell)
                      
        if key == 0:
            print('No solution.')
            
    def recursive_DLS2(self, cell, cutoff):
        if Find.__goal_test(self, cell):
            return cell
        
        elif cell.f > cutoff:
            Find.m = min([Find.m, cell.f])
            return 'cutoff'
        
        else:
            cutoff_ocurred_or_not = False
            successors = Find.__successor3(self, cell)
            for i in range(0, len(successors)):
                result = Find.recursive_DLS2(self, successors[-1], cutoff)
                del(successors[-1])
                if result == 'cutoff':
                    cutoff_ocurred_or_not = True
                    
                elif result != 'failure':
                    return result
                
            if cutoff_ocurred_or_not:
                return 'cutoff'
            
            else:
                return 'failure'
    
    def DLS2(self, cutoff):
        node = Cell(self.source[0], self.source[1],
                                        [[False for x in range(self.board.n)] for y in range(self.board.m)],
                                        self.__get_number(self.source[0], self.source[1]),
                                        self.__get_number(self.goal[0], self.goal[1]), [], 0,
                                        Find.h(self, self.source[0], self.source[1]))
        node.path.append(node)
        return Find.recursive_DLS2(self, node, cutoff)
    
    def IDA_star(self):
        cutoff = Find.h(self, self.source[0], self.source[1])
        while True:
            result = Find.DLS2(self, cutoff)
            if result != 'cutoff':
                break
            cutoff = Find.m
        if result == 'failure':
            print('No solution.')
            
        else:
            Find.__print_solution2(self, result)
            
                 