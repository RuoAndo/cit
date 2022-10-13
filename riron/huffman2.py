from collections import Counter

def MIN_PRIORITY_QUEUE(S):
    return sorted(S.items(), key=lambda x: x[1], reverse=True)

def EXTRACT_MIN(Q):
    return Q.pop()

def INSERT(Q, z):
    return Q.append(z)

def HUFFMAN(S, a):
    n = len(S)
    Q = MIN_PRIORITY_QUEUE(S)
    for i in range(n - 1):
        left = EXTRACT_MIN(Q)
        right = EXTRACT_MIN(Q)
        freq = left[1] + right[1]
        z = (left[0] + right[0], freq)
        INSERT(Q, z)
        a.append([left, "0", left[0] + right[0]])
        a.append([right, "1", left[0] + right[0]])
        Q = dict(zip([i[0] for i in Q], [i[1] for i in Q]))
        Q = MIN_PRIORITY_QUEUE(Q)
    a.append([EXTRACT_MIN(Q), "", "top"])
    return a

def PrintReslut(b):
    for i in range(len(a)):
        now = a[i][0][0]
        num = a[i][1]
        j = 0
        while a[j][2] != 'top':
            if a[i][2] == a[j][0][0]:
                num = a[j][1] + num
                i = j
                flag = 0
                for k in range(len(a)):
                    if a[k][0][0] == 'top' or a[j][2] == a[k][0][0]:
                        flag = 1
                        break
            else:
                j += 1
        if now in s:
            b.append([now, num])
    return b

def DivideS(S):
    S = list(S)
    S = Counter(S)
    S = dict(S)
    return S

str="ABBCACCEACBCCFABCDAFEABFFADBBC"

s = DivideS(str)
a = HUFFMAN(s, [])
for b in sorted(PrintReslut([])):
    print(b[0] + ": " + b[1])
