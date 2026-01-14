# Quick Reference Guide

## Using the Python Editor

### Input/Output Basics

**Reading Input:**
```python
# Single value
name = input()

# Multiple values on one line
a, b = input().split()

# Convert to integers
x, y = map(int, input().split())

# Read a list of numbers
numbers = list(map(int, input().split()))
```

**Printing Output:**
```python
# Simple print
print("Hello")

# Print variable
print(answer)

# Format with f-strings
print(f"The answer is {result}")

# Format decimals
print(f"{value:.2f}")  # 2 decimal places

# Print multiple lines
print("First line")
print("Second line")
```

### Common Patterns

**Sum of numbers:**
```python
numbers = list(map(int, input().split()))
print(sum(numbers))
```

**Average:**
```python
numbers = list(map(int, input().split()))
avg = sum(numbers) / len(numbers)
print(f"{avg:.2f}")
```

**Max/Min:**
```python
numbers = list(map(int, input().split()))
print(max(numbers))
print(min(numbers))
```

**Count items:**
```python
sentence = input()
word_count = len(sentence.split())
print(word_count)
```

**Filter/Transform:**
```python
numbers = list(map(int, input().split()))
evens = [x for x in numbers if x % 2 == 0]
print(evens)
```

### Useful Imports

```python
import math          # math.sqrt(), math.pi, etc.
import re            # Regular expressions
import itertools     # Combinations, permutations
import collections   # Counter, defaultdict
import statistics    # mean, median, mode
```

### Tips

1. **Test Cases Show Input**: Look at the test case input to understand the format
2. **Exact Match Required**: Your output must match exactly (no extra spaces/newlines)
3. **Multi-line OK**: You can use as many lines as you need
4. **Use Functions**: Define functions if it makes your code clearer
5. **Debug**: If tests fail, check the expected vs actual output carefully

### Example: Complete Challenge

**Challenge**: Read two numbers and print their sum  
**Input**: `5 3`  
**Expected Output**: `8`

**Solution**:
```python
a, b = map(int, input().split())
print(a + b)
```

**How it works**:
1. `input()` reads "5 3"
2. `.split()` splits into ["5", "3"]
3. `map(int, ...)` converts to [5, 3]
4. `a, b = ...` unpacks into variables
5. `print(a + b)` outputs "8"

Happy coding! 🚀
