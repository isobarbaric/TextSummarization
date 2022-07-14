import numpy as np
g = [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [1, 0.5, 0, 0],
     [0, 0.5, 0, 0]]
g = np.array(g)
pr = np.array([1, 1, 1, 1]) # initialization for a, b, e, f is 1
d = 0.85

# pr = 0.15 + 0.85 * np.dot(g, pr)
# print(np.dot(g, pr))

print(pr)
print(np.dot(g, pr))
print(0.85 * np.dot(g, pr))
print(0.15 + 0.85 * np.dot(g, pr))