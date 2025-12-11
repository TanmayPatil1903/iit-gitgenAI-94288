numbers = input("Enter numbers separated by commas: ")
num_list = [int(n.strip()) for n in numbers.split(',')]
even_count = 0
odd_count = 0
for num in num_list:
    if num % 2 == 0:
        even_count += 1
    else:
        odd_count += 1
print("Even numbers:", even_count)
print("Odd numbers:", odd_count)