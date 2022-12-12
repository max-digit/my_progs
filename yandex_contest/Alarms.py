import sys
# вводим данные
N, X, K = (int(i) for i in input().split())
while N < 1 or X < 1 or K < 1:
    N, X, K = (int(i) for i in input().split())
alarms = [int(i) for i in input().split()][:N]

# проверяем частные случаи
if K == 1:
    Time = min(alarms)
    print(Time)
    sys.exit()
elif N == 1:
    Time = min(alarms) + round((X / N) * (K - 1))
    print(Time)
    sys.exit()

# удаляем лишние будильники:
d = {}
def group(alarm):    
    r = alarm % X
    if r in d and alarm < d[r]:
        d[r] = alarm
    if r not in d:
        d[r] = alarm
list(map(group,alarms))

def reduce(y):
    y.clear()
    def f(key):
        y.append(d[key])
    list(map(f,d))
reduce(alarms)
alarms.sort()
N = len(alarms)

# Если период повтора больше максимального будильника (X >= tmax):
if X >= max(alarms):
    if K <= N:
        Time = alarms[K - 1]
    elif K > N:
        Time = alarms[(K - 1) % N] + X * ((K - 1) // N)
    print(Time)
    sys.exit()

# задаем функции по подсчету количества прозвеневших будильников:
def q(alarm):
    if T <= alarm:
        q = 0
    if T > alarm:
        q = (T - alarm) / X
        if q != int(q):
            q = int(q) + 1
    return q

def Q(T):
    Q = sum(map(q,alarms))
    return Q

# ищем время пробуждения:
Tmin = min(alarms)
Tmax = max(alarms) + round((X / N) * (K - 1))
T = round(Tmin / 2) + round(Tmax / 2)
while True:
    Qu = Q(T)
    if Qu < K - 1:
        Tmin = T
    elif Qu > K - 1:
        Tmax = T
    elif Qu == K - 1:
        R = T % X
        if d.get(R) in alarms:
            Time = int(T)
            print(Time)
            sys.exit()            
        else:
            Tmin = T
    T = round(Tmin / 2) + round(Tmax / 2)
