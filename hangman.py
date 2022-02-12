from string import whitespace
import requests, random, re
from bs4 import BeautifulSoup

def create_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
    
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def scrape_words():
    url = "https://www.ef.com/wwen/english-resources/english-vocabulary/top-1000-words/"
    soup = create_soup(url)

    global lists_of_words
    lists_of_words = []
    vocabs = soup.find("div", attrs={"class":"field-item even"}).select_one("div p:nth-of-type(2)").get_text().strip().replace("\n", " ").replace("\r", "").replace("\t", "")
    # print(vocabs.split())

    lists_of_words = vocabs.split()
    # print(lists_of_words)

def intro():
    print('\nWelcome to Hangman Game!')
    name = input("Enter your name: ")
    print("Hello {}! Let's play Hangman!".format(name))

    main()

# define the main function:
def main():
    global count
    global already_guessed
    global length
    global word
    global display
    global play_game

    scrape_words()

    word = random.choice(lists_of_words)
    
    length = len(word)
    count = 0

    display = '_' * length
    already_guessed = []

    play_loop()

# loop until word is fully guessed | time runs out
def play_loop():
    global play_game # continue | end ?
    play_game = input('Do you want to continue playing? Y/N \n')
    while play_game.lower() not in ['y', 'n']:
        play_game = input('Do you want to continue playing? Y/N \n')
    if play_game.lower() == 'n':
        print('Thanks for playing! Goodbye')
        exit()
    elif play_game.lower() == 'y':
        hangman()

def hangman():
    global count
    global word
    global already_guessed
    global length
    global display
    global play_game

    guess = input('\nThe Hangman word: '+display+' Enter your guess: ')
    while guess in already_guessed:
        guess = input("You have already guessed this letter. Select a different letter: ")

    guess = guess.strip()
    limit = 7

    if len(guess) < 1 | len(guess) > 1:
        print('Invalid input. Please enter one letter')
        hangman()
    elif guess in word:
        already_guessed.append(guess)
        print("You guessed the correct letter!")

        # check if there are more than 1 guessed alphabet
        for each in word:
            if word.count(each) > 1 and each == guess:
                how_many_same = word.count(each) - 1

                # find all indices of same alphabets
                index = word.find(guess)
                part = []
                part.append(word[:index] + guess)

                while how_many_same != 0:
                    display = display[:index] + guess + display[index + 1:]

                    word = word[index+1:]

                    index = word.find(guess)
                    part.append(word[:index] + guess)

                    how_many_same -= 1

                    if how_many_same == 0:
                        part.append(word[index+1:])
                        word = "".join(part) # this returns back to original word

            elif word.count(each) == 1 and each == guess:
                # find index of the guessed word and replace _ with guessed alphabet
                index = word.find(guess)
                display = display[:index] + guess + display[index + 1:]

        for each in word:
            txt = word.replace("", " ")[1: -1]

        keep = already_guessed
        display = re.sub(r'\b\w+\b', lambda w: w.group() if w.group() in keep else '_', txt)
        display = display.replace(" ", "")

        if '_' not in display:
            print("Congratulations! You have guessed the word correctly!")
            main()
        elif '_' in display:
            hangman()
        

    elif guess in already_guessed:
        print("Try another letter \n")
        hangman()
    elif guess not in word:
        count += 1
        print("Wrong guess. Remainig Guess: {} - Try again".format(limit-count))

        if count == 1:
            print("   _____ \n"
                  "  |     | \n"
                  "  |       \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "__|__\n")
        if count == 2:
            print("   _____ \n"
                  "  |     | \n"
                  "  |     O \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "__|__\n")
        elif count == 3:
            print("   _____ \n"
                  "  |     | \n"
                  "  |     O \n"
                  "  |     | \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "__|__\n")
        elif count == 4:
            print("   _____ \n"
                 "  |     | \n"
                 "  |     O \n"
                 "  |    /| \n"
                 "  |      \n"
                 "  |      \n"
                 "  |      \n"
                 "__|__\n")
        elif count == 5:
            print("   _____ \n"
                  "  |     | \n"
                  "  |     O \n"
                  "  |    /|\ \n"
                  "  |       \n"
                  "  |      \n"
                  "__|__\n")
        elif count == 6:
            print("   _____ \n"
                  "  |     | \n"
                  "  |     O \n"
                  "  |    /|\ \n"
                  "  |    /   \n"
                  "__|__\n")
        elif count == 7:
            print("   _____ \n"
                  "  |     | \n"
                  "  |     O \n"
                  "  |    /|\ \n"
                  "  |    / \ \n"
                  "__|__\n")
            print("The man was hanged :( The word was:\n{}".format(word))
            main()
        hangman()

if __name__ == "__main__":
    intro()