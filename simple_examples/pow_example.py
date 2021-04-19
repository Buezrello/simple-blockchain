from hashlib import sha256


"""
example of Proof of Work

PROBLEM:
x = 1
find such 'y' that sha256 hash of x*y has '123' at the end
"""

x = 1
y = 0

while sha256(f'{x*y}'.encode()).hexdigest()[-3:] != '123':
    y += 1

print(f'Solution is {y}')
print('Hash is {}'.format(sha256(f'{x*y}'.encode()).hexdigest()))

