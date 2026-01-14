# Python Editor Examples

This document shows examples of what you can do with the updated Python editor.

## Features

✅ **Multi-line code** - No longer restricted to one-liners!  
✅ **Input handling** - Use `input()` to read from stdin  
✅ **Print output** - Use `print()` to write to stdout  
✅ **Imports** - Import any Python standard library module  
✅ **Full Python support** - Functions, classes, loops, everything!

## Example 1: Simple Input/Output

**Challenge:** Read two numbers and print their sum

**Input:** `5 3`  
**Output:** `8`

**Solution:**
```python
a, b = map(int, input().split())
print(a + b)
```

## Example 2: Multiple Inputs

**Challenge:** Read a name and print a greeting

**Input:** `Alice`  
**Output:** `Hello, Alice!`

**Solution:**
```python
name = input()
print(f'Hello, {name}!')
```

## Example 3: Using Imports

**Challenge:** Count words in a sentence

**Input:** `The quick brown fox`  
**Output:** `4`

**Solution:**
```python
import sys
sentence = input()
words = sentence.split()
print(len(words))
```

## Example 4: Multi-line Output

**Challenge:** Calculate statistics for a list of numbers (sum, average, max)

**Input:** `10 20 30 40 50`  
**Output:**
```
150
30.00
50
```

**Solution:**
```python
numbers = list(map(int, input().split()))
print(sum(numbers))
print(f'{sum(numbers)/len(numbers):.2f}')
print(max(numbers))
```

## Example 5: Functions and Loops

You can even define functions and use loops!

**Challenge:** Print all even numbers from 1 to N

**Input:** `10`  
**Output:** `2 4 6 8 10`

**Solution:**
```python
def get_evens(n):
    return [x for x in range(1, n+1) if x % 2 == 0]

n = int(input())
evens = get_evens(n)
print(' '.join(map(str, evens)))
```

## Example 6: Still Support One-Liners!

The editor still supports elegant one-liners for simple tasks:

**Challenge:** Square numbers 1-5

**Output:** `[1, 4, 9, 16, 25]`

**Solution:**
```python
print([x**2 for x in range(1, 6)])
```

## Tips

1. **Input Parsing:** The test cases provide input via stdin. Use `input()` to read it.
2. **Exact Output:** Your output must match exactly - watch for trailing spaces and newlines!
3. **Multiple Lines:** To output multiple lines, use multiple `print()` statements.
4. **Debugging:** If your code doesn't pass, check the "Input" field in the test results to see what was provided.
5. **Imports:** Feel free to import modules like `math`, `itertools`, `collections`, etc.

## Common Patterns

### Reading a single integer
```python
n = int(input())
```

### Reading multiple integers on one line
```python
a, b, c = map(int, input().split())
```

### Reading a list of integers
```python
numbers = list(map(int, input().split()))
```

### Reading multiple lines
```python
line1 = input()
line2 = input()
```

### Formatting output with specific decimal places
```python
print(f'{value:.2f}')  # 2 decimal places
```

Happy coding! 🐍
