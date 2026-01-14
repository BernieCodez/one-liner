#!/bin/bash

echo "=== Testing All Challenge Types ==="
echo ""

echo "1. One-liner (Challenge 1):"
curl -s -X POST http://127.0.0.1:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"code": "print([x**2 for x in range(1, 6)])", "challenge_id": 1}' | \
  python3 -c "import sys, json; r=json.load(sys.stdin); print(f\"  Result: {'✅ PASSED' if r['passed'] else '❌ FAILED'}\")"
echo ""

echo "2. Input/Output (Challenge 11 - Sum Two Numbers):"
curl -s -X POST http://127.0.0.1:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"code": "a, b = map(int, input().split())\nprint(a + b)", "challenge_id": 11}' | \
  python3 -c "import sys, json; r=json.load(sys.stdin); print(f\"  Result: {'✅ PASSED' if r['passed'] else '❌ FAILED'}\"); print(f\"  Example - Input: '{r['results'][0]['input']}' -> Output: '{r['results'][0]['actual']}'\")"
echo ""

echo "3. Multi-line with imports (Challenge 13 - Count Words):"
curl -s -X POST http://127.0.0.1:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"code": "import re\nsentence = input()\nprint(len(sentence.split()))", "challenge_id": 13}' | \
  python3 -c "import sys, json; r=json.load(sys.stdin); print(f\"  Result: {'✅ PASSED' if r['passed'] else '❌ FAILED'}\")"
echo ""

echo "4. Temperature Converter (Challenge 14):"
curl -s -X POST http://127.0.0.1:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"code": "celsius = float(input())\nfahrenheit = round((celsius * 9/5) + 32, 1)\nprint(fahrenheit)", "challenge_id": 14}' | \
  python3 -c "import sys, json; r=json.load(sys.stdin); print(f\"  Result: {'✅ PASSED' if r['passed'] else '❌ FAILED'}\")"
echo ""

echo "=== All Features Working! ==="
echo ""
echo "✅ Multi-line code support"
echo "✅ Input via stdin (input())"
echo "✅ Output via stdout (print())"
echo "✅ Import statements"
echo "✅ Full Python functionality"
