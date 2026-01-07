import random
import time
import json
import os
from colorama import init, Fore, Style

# Renkli çıktılar için başlatıcı
init(autoreset=True)

def high_score_oku():
    """Skorları dosyadan yükler."""
    if os.path.exists("scores.json"):
        with open("scores.json", "r") as f:
            return json.load(f)
    return {}

def high_score_kaydet(seviye, deneme):
    """Yeni skor rekor ise dosyaya kaydeder."""
    skorlar = high_score_oku()
    if seviye not in skorlar or deneme < skorlar[seviye]:
        skorlar[seviye] = deneme
        with open("scores.json", "w") as f:
            json.dump(skorlar, f)
        return True
    return False

def start_game():
    print(Fore.CYAN + Style.BRIGHT + "\n=== Welcome to the Advanced Number Guessing Game! ===")
    
    while True:
        # Mevcut rekorları göster
        skorlar = high_score_oku()
        if skorlar:
            print(Fore.YELLOW + "\n--- Current Records ---")
            for s, d in skorlar.items():
                print(f"{s}: {d} attempts")

        print(Fore.WHITE + "\nPlease Select difficulty: ")
        print("1. Easy (10 attempts)")
        print("2. Medium (5 attempts)")
        print("3. Hard (3 attempts)")

        choice = input(Fore.YELLOW + "Enter 1, 2, or 3: ")
        
        # Zorluk ayarları
        config = {'1': (10, "Easy"), '2': (5, "Medium"), '3': (3, "Hard")}
        if choice in config:
            attempts, level = config[choice]
        else:
            print(Fore.RED + "Invalid choice. Please try again.")
            continue

        print(Fore.GREEN + f"\nSelected {level} level. You have {attempts} attempts. Good luck!")

        number_to_guess = random.randint(1, 100)
        test_number = 0
        start_time = time.time()
        winner = False

        while test_number < attempts:
            try:
                guess = int(input(Fore.WHITE + "\nEnter your guess: "))
                test_number += 1
                
                # Mesafe kontrolü (Sıcak/Soğuk)
                fark = abs(number_to_guess - guess)

                if guess == number_to_guess:
                    end_time = time.time()
                    time_taken = round(end_time - start_time, 2)
                    print(Fore.GREEN + Style.BRIGHT + f"Congratulations! You guessed it in {test_number} attempts.")
                    print(Fore.CYAN + f"Time taken: {time_taken} seconds.")

                    if high_score_kaydet(level, test_number):
                        print(Fore.MAGENTA + Style.BRIGHT + "NEW ALL-TIME HIGH SCORE FOR THIS LEVEL!")
                    
                    winner = True
                    break
                
                # İpucu Sistemi
                if fark <= 5:
                    print(Fore.RED + "BURNING HOT! You are extremely close.")
                elif fark <= 15:
                    print(Fore.YELLOW + "Warm! You are getting there.")
                else:
                    print(Fore.BLUE + "Cold... You are far away.")

                if guess < number_to_guess:
                    print(Fore.WHITE + "Hint: Try a HIGHER number.")
                else:
                    print(Fore.WHITE + "Hint: Try a LOWER number.")
                
                print(Fore.LIGHTBLACK_EX + f"Attempts left: {attempts - test_number}")

            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a number between 1 and 100.")
        
        if not winner:
            print(Fore.RED + f"\nGame Over! The correct number was {number_to_guess}.")
        
        play_again = input(Fore.YELLOW + "\nDo you want to play again? (y/n): ").lower()
        if play_again != 'y' and play_again != 'yes':
            print(Fore.CYAN + "Thank you for playing! Goodbye!")
            break

if __name__ == "__main__":
    start_game()