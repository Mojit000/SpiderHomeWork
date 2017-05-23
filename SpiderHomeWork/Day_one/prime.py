def isPrime(n):
    # 用于计算n能被整除的个数
    count = 0
    # 1非素数
    if n==1:
        return False
    for i in range(1, n+1):
        # 如果n能被i整除,count计数加1
        if n%i==0:
            count+=1
    # 整除的个数大于2,说明n不是素数
    if count>2:
        return False
    else:
        return True


if __name__ == '__main__':
    for i in range(1, 101):
        if isPrime(i):
            print('素数:', i)

[i for i in range(1, 101) if isPrime(i)]