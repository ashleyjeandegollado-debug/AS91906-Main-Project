def count(max, num):
    print(num)
    if num < max:
        count(max, num + 1 )

max = int(input("max?: "))
count(max, 0)

