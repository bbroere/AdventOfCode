import time

from input.testresults import testdata_1_result
from solution import part_1, part_2

print("========================================")
print("================ PART 1 ================")
print("========================================")

start_test_1 = time.time()
test_solution_1 = part_1("input/testdata.txt")
end_test_1 = time.time()
if test_solution_1 == testdata_1_result and test_solution_1 is not None:
    print(f"Test of part 1 succeeded with value {test_solution_1} ({'%.3f' % (end_test_1 - start_test_1)}s)")
    start_part_1 = time.time()
    sol_1 = part_1('input/input.txt')
    end_part_1 = time.time()
    print(f"Own solution should be {sol_1} ({'%.3f' % (end_part_1 - start_part_1)}s)")  # 3699
else:
    print(f"Part 1 unsuccessful, expected {testdata_1_result}, got {test_solution_1}")

print("")
print("========================================")
print("================ PART 2 ================")
print("========================================")

start_part_2 = time.time()
sol_2 = part_2('input/input.txt')
end_part_2 = time.time()
print(f"Own solution should be {sol_2} ({'%.3f' % (end_part_2 - start_part_2)}s)")  # 613391294577878
