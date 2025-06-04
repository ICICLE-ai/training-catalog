---
tags:
  - CI4AI
---

# Explanation

### Detailing csv columns
In the output file: ***ProgramFeatures.csv***, you will find several column names:

**Important note**
Cetus' static profiler handles data sizes and loop sizes in different ways. When it comes to profiling data sizes, loops, or inputs, they can be either numerical or symbolic, depending on the program and whether data sizes are available at compilation time.


1. **application_name**  
   The name of the application being analyzed. This is detected by the tool automatically (it will commonly use the .c source file).

2. **loop_id**  
   Identifier for the loop being measured within the application. Using the standard cetus notation **function#loop_id#loopnest_id#...#loopnest_n_id**

3. **data_size**  
   Size of the data being processed by the loop.

4. **no_iterations**  
   Number of iterations performed by the loop in one execution.

5. **total_iterations**  
   Total number of iterations the loop has executed over its lifetime.

6. **no_loads**  
   Number of memory load operations performed by the loop.

7. **no_stores**  
   Number of memory store operations performed by the loop.

8. **no_instructions**  
   Total number of instructions executed within the loop.

9. **no_statements**  
   Total number of statements inside the loop.

10. **loopness_level**  
    Depth or nesting level of the loop in the application.

11. **no_bits_per_iteration**  
    Number of bits processed during each iteration of the loop.

12. **no_times_data_type_changed**  
    Number of times the operating data type is changed during loop execution.

13. **no_integer_operations**  
    Number of integer operations performed by the loop.

14. **no_float_operations**  
    Number of floating-point operations performed by the loop.

15. **no_double_operations**  
    Number of double-precision floating-point operations executed in the loop.

16. **no_long_double_operations**  
    Number of long double precision operations executed in the loop.

17. **no_long_operations**  
    Number of long-type operations performed by the loop.

18. **no_short_operations**  
    Number of short-type operations performed by the loop.

19. **bigo_notation**  
    Time complexity of the loop expressed in Big O notation.

20. **no_multiplications**  
    Number of multiplication operations executed by the loop.

21. **no_substractions**  
    Number of subtraction operations executed by the loop.

22. **no_sums**  
    Number of addition operations executed by the loop.

23. **no_side_effect_free_function_calls**  
    Number of function calls in the loop that do not produce side effects.

24. **data_dependence_free**  
    Indicates whether the loop is free from data dependence.

25. **ratio_reduction_statements**  
    Ratio of statements in the loop related to reduction operations.

26. **ratio_remaining_flow_dependences**  
    Ratio of remaining flow dependences in the loop.





