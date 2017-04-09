# graph_search
Implementation of graph search algorithms like BFS, DFS, UCS and A*.

A creative and detailed problem statement is provided in Problem-statement.pdf. The python implementation is in file homework.py in the folder 'Python Answer'.
I also manually created some test cases to verify my code and test some corner cases. They are in the same directory with the names as BFS_case_1.txt, BFS_case_2.txt, etc. The files starting with BFS are meant to test BFS algorithm, those starting with DFS are meant to test DFS algorithm implementation and likewise. The expected output of a test case file is stored in another file (in the same directory) by the name of output_<name_of_test_case_file>. For example, expected output of UCS_case11.txt is stored in output_UCS_case11.txt.

Instead to running these cases individually, you can just run pu_test.sh file, which internally executes runScript.sh once for each type of search algortihm (BFS, DFS, UCS, A*). You might have to make small path related changes in order to run it.
