def is_valid_change(word1, word2):
   """Check if word2 differs from word1 by only one letter."""
   if len(word1) != len(word2):
       return False
   return sum(1 for a, b in zip(word1, word2) if a != b) == 1

while True:
    try:
        word_length = int(input("Welcome to the Word Ladder Game! How many letters will your words have? ").strip())
        if word_length <= 0:
            print("Please enter an integer greater than 0.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter an integer greater than 0.")

while True:
    start_word = input(f"Enter the starting word (must be {word_length} letters): ").lower().strip()
    if not isinstance(start_word, str) or not start_word:
        print("Words must be strings. Try again.")
        continue
    if not start_word.isalpha():
        print("Words must contain only letters. Try again.")
        continue
    if len(start_word) != word_length:
        print(f"Start word must be exactly {word_length} letters. Try again.")
        continue
    break

while True:
    goal_word = input(f"Enter the goal word (must be {word_length} letters): ").lower().strip()
    if not isinstance(goal_word, str) or not goal_word:
        print("Words must be strings. Try again.")
        continue
    if not goal_word.isalpha():
        print("Words must contain only letters. Try again.")
        continue
    if goal_word == start_word:
        print("Goal word must be different from the start word. Try again.")
        continue
    if len(goal_word) != word_length:
        print(f"Goal word must be exactly {word_length} letters. Try again.")
        continue
    break
current_word = start_word

print(f"Word Ladder Game! Transform '{start_word}' to '{goal_word}' one letter at a time.")

while current_word != goal_word:
   new_word = input(f"Enter a word that changes one letter in '{current_word}': ").lower()

   if not is_valid_change(current_word, new_word):
       print("Invalid move! Your word must change exactly one letter.")
   else:
       current_word = new_word

print(f"Congratulations! You turned '{start_word}' into '{goal_word}'!")