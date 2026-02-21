# -*- coding: utf-8 -*-

class mynumpy:
    def __init__(self, data=None):
        self.myArray = None
        self.myShape = None
        if data is not None:
            self.array(data)

    def __version__(self):
        return "myNumpy version : 0.0.2 (Py2.7 Support)"

    def __len__(self):
        return 0 if self.myShape is None else self.myShape[0]

    def __bool__(self):
        return self.myArray is not None
        
    # Python 2.7에서는 __nonzero__를 사용해야 객체의 bool 값을 평가할 수 있습니다.
    def __nonzero__(self): 
        return self.__bool__()

    # def __repr__(self):
    #     return "array(" + str(self.myArray) + ")"
    def __repr__(self):
        # 데이터가 없는 경우 예외 처리
        if self.myArray is None:
            return "array(None)"
        
        # 먼저 리스트를 기본 문자열로 변환 (예: "[[1.0, 2.0], [3.0, 4.0]]")
        str_arr = str(self.myArray)
        
        # 2차원 배열 이상일 때만 줄바꿈 적용
        if len(self.shape) >= 2:
            # "], [" 부분을 찾아서 줄바꿈(\n)과 공백 7칸을 넣어줌
            # 공백 7칸인 이유는 맨 앞의 "array([" 글자 수가 딱 7칸이기 때문이야!
            str_arr = str_arr.replace("], [", "],\n       [")
            
        return "array(" + str_arr + ")"

    # 속성(Property)으로 만들어 numpy의 x.shape 처럼 괄호 없이 쓸 수 있게 함
    @property
    def shape(self):
        return self.myShape

    def array(self, getArray):
        """파이썬 리스트를 입력받아 내부 배열과 모양을 설정합니다."""
        self.myArray = self._copy_and_check(getArray)
        self.myShape = self._get_shape(self.myArray)
        return self

    def _get_shape(self, data):
        """재귀적으로 배열의 모양(Shape)을 파악합니다."""
        if isinstance(data, list):
            if len(data) == 0:
                return (0,)
            # 리스트 안의 첫 번째 원소를 따라가며 차원을 계산 (정사각형 배열 가정)
            return (len(data),) + self._get_shape(data[0])
        else:
            return () # 숫자에 도달하면 빈 튜플 반환

    def _copy_and_check(self, data):
        """재귀적으로 데이터를 복사하며 숫자인지 확인하고 Float으로 통일합니다."""
        if isinstance(data, list):
            return [self._copy_and_check(item) for item in data]
        elif isinstance(data, (int, float)):    
            return float(data)
        else:
            raise ValueError("원소가 숫자가 아닙니다.")

    def _apply_op(self, a, b, op):
        """재귀적으로 두 배열(또는 스칼라) 간의 연산을 수행합니다."""
        # 1. 배열과 숫자(스칼라)의 연산 (브로드캐스팅)
        if isinstance(a, list) and not isinstance(b, list):
            return [self._apply_op(item, b, op) for item in a]
        if not isinstance(a, list) and isinstance(b, list):
            return [self._apply_op(a, item, op) for item in b]

        # 2. 두 배열의 연산
        if isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):
                raise ValueError("사이즈가 맞지 않습니다.")
            return [self._apply_op(x, y, op) for x, y in zip(a, b)]
            
        # 3. 두 숫자의 연산 (재귀의 끝)
        return op(a, b)

    # ================= 사칙 연산 =================
    
    def __add__(self, other):
        other_data = other.myArray if isinstance(other, mynumpy) else other
        res = mynumpy()
        res.myArray = self._apply_op(self.myArray, other_data, lambda x, y: x + y)
        res.myShape = res._get_shape(res.myArray)
        return res

    def __sub__(self, other):
        other_data = other.myArray if isinstance(other, mynumpy) else other
        res = mynumpy()
        res.myArray = self._apply_op(self.myArray, other_data, lambda x, y: x - y)
        res.myShape = res._get_shape(res.myArray)
        return res

    def __mul__(self, other):
        other_data = other.myArray if isinstance(other, mynumpy) else other
        res = mynumpy()
        res.myArray = self._apply_op(self.myArray, other_data, lambda x, y: x * y)
        res.myShape = res._get_shape(res.myArray)
        return res

    def __div__(self, other): # Python 2.7용 나눗셈
        other_data = other.myArray if isinstance(other, mynumpy) else other
        res = mynumpy()
        res.myArray = self._apply_op(self.myArray, other_data, lambda x, y: x / y)
        res.myShape = res._get_shape(res.myArray)
        return res

    def __truediv__(self, other): # 호환성 유지
        return self.__div__(other)

    # 오른쪽 항이 스칼라일 때를 위한 매직 메서드 (예: 3 + array)
    def __radd__(self, other): return self.__add__(other)
    def __rmul__(self, other): return self.__mul__(other)
    def __rsub__(self, other):
        res = mynumpy()
        res.myArray = self._apply_op(other, self.myArray, lambda x, y: x - y)
        res.myShape = res._get_shape(res.myArray)
        return res
    def __rdiv__(self, other):
        res = mynumpy()
        res.myArray = self._apply_op(other, self.myArray, lambda x, y: x / y)
        res.myShape = res._get_shape(res.myArray)
        return res


    # 내적
    def dot(self, other):
        """
        1차원 벡터 및 2차원 행렬의 내적을 수행합니다.
        """
        # other가 mynumpy 객체인지 일반 리스트인지 확인하여 데이터와 형태를 추출
        if isinstance(other, mynumpy):
            other_data = other.myArray
            other_shape = other.shape
        else:
            other_data = self._copy_and_check(other)
            other_shape = self._get_shape(other_data)
            
        my_shape = self.shape
        
        # 1. 1차원 벡터의 내적 (예: [1, 2] dot [3, 4])
        if len(my_shape) == 1 and len(other_shape) == 1:
            if my_shape[0] != other_shape[0]:
                raise ValueError("벡터 내적을 위한 사이즈가 맞지 않습니다.")
            return sum(x * y for x, y in zip(self.myArray, other_data))
            
        # 2. 2차원 행렬 간의 내적 (예: (2, 3) dot (3, 2))
        elif len(my_shape) == 2 and len(other_shape) == 2:
            if my_shape[1] != other_shape[0]:
                raise ValueError("행렬 곱셈 차원 불일치: 앞 행렬의 열과 뒤 행렬의 행 크기가 다릅니다.")
            
            result = []
            for i in range(my_shape[0]):
                row = []
                for j in range(other_shape[1]):
                    # 내적 계산
                    val = sum(self.myArray[i][k] * other_data[k][j] for k in range(my_shape[1]))
                    row.append(val)
                result.append(row)
            return mynumpy(result)
            
        # 3. 2차원 행렬과 1차원 벡터의 내적
        elif len(my_shape) == 2 and len(other_shape) == 1:
            if my_shape[1] != other_shape[0]:
                raise ValueError("행렬-벡터 곱셈 차원 불일치")
            result = []
            for i in range(my_shape[0]):
                val = sum(self.myArray[i][k] * other_data[k] for k in range(my_shape[1]))
                result.append(val)
            return mynumpy(result)
            
        # 4. 1차원 벡터와 2차원 행렬의 내적
        elif len(my_shape) == 1 and len(other_shape) == 2:
            if my_shape[0] != other_shape[0]:
                raise ValueError("벡터-행렬 곱셈 차원 불일치")
            result = []
            for j in range(other_shape[1]):
                val = sum(self.myArray[k] * other_data[k][j] for k in range(my_shape[0]))
                result.append(val)
            return mynumpy(result)
            
        else:
            raise NotImplementedError("현재 1차원과 2차원 배열의 내적만 지원합니다.")