numbers = input("Enter numbers (comma-separated): ")

num_list = numbers.split(",")

even_count = 0
odd_count = 0

for num in num_list:
    n = int(num.strip())
    if n % 2 == 0:
        even_count += 1
    else:
        odd_count += 1

print("Even numbers:", even_count)
print("Odd numbers:", odd_count)
