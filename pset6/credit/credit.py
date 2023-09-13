from cs50 import get_string
import sys


card_og = get_string("Number: ")


# reverse string, since we need to count from last digit
card = card_og[::-1]
length = len(card)

mul_sum1 = int_sum1 = int_sum2 = summ = 0
str_sum1 = ""


for num in range(length):
    # calculate even numbers
    if (num % 2) == 0:
        int_sum2 += int(card[num])
    # calculate odd numbers
    else:
        mul_sum1 = int(card[num]) * 2
        str_sum1 += str(mul_sum1)

# add digits of odd numbers
for num in range(len(str_sum1)):
    int_sum1 += int(str_sum1[num])

# get a sum of odd and even numbers and convert to string for checking
summ = int_sum1 + int_sum2
summ = str(summ)

# if last difit of a sum is not equal to 0, card is invalid
if summ[len(summ) - 1] != "0":
    print("INVALID")
    sys.exit(0)
# VISA length 13 or 16, starts with 4
elif length == 13 or length == 16 and card_og[0] == "4":
    print("VISA")
    sys.exit(0)
# MASTERCARD length 16, starts 51-55
elif length == 16 and card_og[0] == "5" and card_og[1] >= "1" or card_og[1] <= "5":
    print("MASTERCARD")
    sys.exit(0)
# AMEX lenght 15, starts 34 or 37
elif length == 15 and card_og[0] == "3" or card_og[1] == 7:
    print("AMEX")
    sys.exit(0)
# else if non of the above, card is invalid
else:
    print("INVALID")
    sys.exit(0)
