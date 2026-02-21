from myNumpy import mynumpy

# 1. 1차원 배열 내적 테스트
v1 = mynumpy([1, 2, 3])
v2 = mynumpy([4, 5, 6])
print("1차원 내적 결과:", v1.dot(v2)) # 32.0 출력 (1*4 + 2*5 + 3*6)

# 2. 2차원 행렬 내적 테스트
A = mynumpy([[1, 2], [3, 4]])
B = mynumpy([[5, 6], [7, 8]])
print("2차원 내적 결과:")
print(A.dot(B)) 
# array([[19.0, 22.0], [43.0, 50.0]]) 출력

# 3. 신경망(X * W) 형태 테스트 (입력 * 가중치)
X = mynumpy([[1, 2]])       # 1x2 행렬
W = mynumpy([[1, 3, 5], 
             [2, 4, 6]])    # 2x3 행렬
B = mynumpy([1])
Y = X.dot(W) + B
print("신경망 연산 결과:\n", Y)
# array([[6.0, 12.0, 18.0]]) 출력 (1x3 행렬)