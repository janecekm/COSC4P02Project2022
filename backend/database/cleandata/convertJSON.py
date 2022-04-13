import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

filename = "exams.txt"
f = open(filename, 'r')
temp = json.loads(f.readlines())
print(json.dumps(temp.decode("utf-8","ignore")))

# for line in f.readlines():
#     temp = json.load(line)
#     print(json.dumps(temp))