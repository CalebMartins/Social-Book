import random
num = 4
list = [1]
while True:
    try:
        li = random.sample(list, num)
        if li:
            num = 4
            break
    except:
        num -= 1
        continue

print(li)
