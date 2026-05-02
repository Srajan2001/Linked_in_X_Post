from agents.memory_agent import save_to_memory # Import the new function

def approve_post(post, topic): # Added topic parameter
    print("\n--- LINKEDIN POST ---\n")
    print(post)
    print("\n-------------------")

    choice = input("Approve post? (yes/no/edit): ").lower()

    if choice == "yes":
        with open("approved_post.txt", "a", encoding="utf-8") as f:
            f.write(post + "\n\n")
        
        # Save to our new RAG database!
        save_to_memory(post, topic) 
        
        print(" Post approved and saved!")
        return "approved", ""
        
    elif choice == "edit":
        feedback = input("What should I change? ")
        return "edit", feedback
        
    else:
        print("Post rejected")
        return "rejected", ""