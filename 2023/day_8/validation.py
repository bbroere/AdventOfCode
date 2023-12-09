import time

from input.testresults import testdata_1_1_result, testdata_1_2_result, testdata_2_result
from solution import part_1, part_2

print("========================================")
print("================ PART 1 ================")
print("========================================")

start_test_1_1 = time.time()
test_solution_1_1 = part_1("input/testdata_1_1.txt")
start_test_1_2 = time.time()
test_solution_1_2 = part_1("input/testdata_1_2.txt")
end_test_1_2 = time.time()
if (test_solution_1_1 is not None and test_solution_1_2 is not None and test_solution_1_1 == testdata_1_1_result and
        test_solution_1_2 == testdata_1_2_result):
    print(f"Test of part 1 succeeded with values {test_solution_1_1} and {test_solution_1_2}" +
          f" ({'%.3f' % (start_test_1_2 - start_test_1_1)}s, {'%.3f' % (end_test_1_2 - start_test_1_2)}s)")
    start_part_1 = time.time()
    sol_1 = part_1('input/input.txt')
    end_part_1 = time.time()
    print(f"Own solution should be {sol_1} ({'%.3f' % (end_part_1 - start_part_1)}s)")  # 18113
elif test_solution_1_1 != testdata_1_1_result:
    print(f"Part 1_1 unsuccessful, expected {testdata_1_1_result}, got {test_solution_1_1}")
else:
    print(f"Part 1_2 unsuccessful, expected {testdata_1_2_result}, got {test_solution_1_2}")

print("")
print("========================================")
print("================ PART 2 ================")
print("========================================")

start_test_2 = time.time()
test_solution_2 = part_2("input/testdata_2.txt")
end_test_2 = time.time()
if test_solution_2 == testdata_2_result and test_solution_2 is not None:
    print(f"Test of part 2 succeeded with value {test_solution_2} ({'%.3f' % (end_test_2 - start_test_2)}s)")
    start_part_2 = time.time()
    sol_2 = part_2('input/input.txt')
    end_part_2 = time.time()
    print(f"Own solution should be {sol_2} ({'%.3f' % (end_part_2 - start_part_2)}s)")  # 12315788159977
else:
    print(f"Part 2 unsuccessful, expected {testdata_2_result}, got {test_solution_2}")
