sentence = input("Enter a sentence: ")
num_characters = len(sentence)
words = sentence.split()
num_words = len(words)
vowels = "aeiouAEIOU"
num_vowels = 0
for char in sentence:
    if char in vowels:
        num_vowels += 1
print("Number of characters:", num_characters)
print("Number of words:", num_words)
print("Number of vowels:", num_vowels)

sentence = input("Enter a sentence: ")
num_characters = len(sentence)
words = sentence.split()
num_words = len(words)
vowels = "aeiouAEIOU"
num_vowels = 0
for char in sentence:
    if char in vowels:
        num_vowels += 1
print("Number of characters:", num_characters)
print("Number of words:", num_words)
print("Number of vowels:", num_vowels)
