K, N = (int(i) for i in input().split())
deck = [int(j) for j in input().split()]
Vasya = 0
Petya = 0
for i in range(N):
    number = deck[i]
    if number % 5 == 0 and number % 3 != 0:
        Vasya += 1
    elif number % 3 == 0 and number % 5 != 0:
        Petya += 1
    if Vasya == K:        
        print('Vasya')
        break
    if Petya == K:
        print('Petya')
        break
    if i == N - 1 and (Vasya < K and Petya < K):
        if Vasya > Petya:
            print('Vasya')
        elif Vasya < Petya:
            print('Petya')
        else:
            print('Draw')
