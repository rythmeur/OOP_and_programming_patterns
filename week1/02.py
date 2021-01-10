
fine_sum = 0  # money
v, num = 70, "B555AA"  # speed and number of car
v = int(v)
print(num[0] != "A", num[1] != "5", num[2] != "5" , num[3] != "5" , num[4] != "A" , num[5] != "A", v > 60)
print((num[0] != "A" and num[1] != "5" and num[2] != "5" and num[3] != "5" and num[4] != "A" and num[5] != "A"))
if (num[0] != "A" and num[1] != "5" and num[2] != "5" and num[3] != "5" and num[4] != "A" and num[5] != "A"):
    print("it's not boss")

while (num[0] != "A" and num[1] != "5" and num[2] != "5" and num[3] != "5" and num[4] != "A" and num[5] != "A"):

    if v > 60:
        if num[1] == num[2] or num[2] == num[3] or \
                num[1] == num[3]:
            if num[1] == num[2] == num[3]:
                fine_sum += 1000
            else:
                fine_sum += 500
        else:
            fine_sum += 100
    v, num = 160, "A555AA"
    v = int(v)
print(fine_sum)