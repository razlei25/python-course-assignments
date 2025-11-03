def name(answer):
    while True:
        
        if answer == "Bob":
            print("It is so nice to finally meet you Bob! I hate other people.")
            break
        else:
            print(f"Hello, {answer}, I was hoping that you are Bob.")
            retry = input("Would you like to try again? (yes/no): ").strip().lower()
            
            if retry in ['yes', 'y']:
                continue
            else:
                print("I hoped you'd say that... Bob would have never given up")
                break


# Example answer
answer = "Bob"

# Run function
name(answer)


