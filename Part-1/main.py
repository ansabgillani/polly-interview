import requests

"""
1. I get the string and store in a state and store the number of wrong steps
2. Eliminate all the words tha are not of the same length as the hangman string
3. Identify the highest probability of the next element in available words and use it as the next guess. 
4. Make the guess and verify its position, if present, in the hangman string and 
eliminate all the elements that does not have that guess in that particular position. 
5. If it's not present, eliminate all the words that dont have that letter, recreate frequency matrix and we will go to the next prob. guess
5. Update the state in case of a correct guess and see if the hangman has all non-underscore letters, if not then verify if you have number of tries left. 
"""


def read_all_text():
    file = open('dictionary.txt', 'r')
    li = []
    for line in file:
        li.append(line.strip().lower())
    return li


def eliminate_all_words_not_of_same_length(words: list, length):
    return [word for word in words if len(word) == length]


def eliminate_all_words_not_having_element_index(words: list, element, index, count):
    return [word for word in words if word[index] == element and word.count(element) == count]


def eliminate_all_words_not_having_element(words, element):
    return [word for word in words if word.find(element) == -1]


def generate_frequency_matrix(words: list):
    alphabets = dict()
    for word in words:
        for index in range(len(word)):
            alphabets[word[index].lower()] = alphabets.get(word[index].lower(), 0) + 1
    return alphabets


def get_highest_probability_element(alphabets: dict, taken_guess):
    max = -1
    element = ''
    for k, v in alphabets.items():
        if v > max and k not in taken_guess:
            element = k
            max = v
    return element


def build_word(alphabets: dict):
    answer = ''
    for i in sorted(alphabets.keys()):
        answer += alphabets[i]
    return answer


def solution():
    list_of_all_words = read_all_text()
    number_of_wrong_steps = 7
    base_url = 'https://hangman-api.herokuapp.com'
    taken_guess = []
    correct_word = dict()
    response = requests.post(f'{base_url}/hangman').json()
    state = response['hangman']
    token = response['token']
    list_of_all_words = eliminate_all_words_not_of_same_length(list_of_all_words, len(state))
    while number_of_wrong_steps:
        frequency_matrix = generate_frequency_matrix(list_of_all_words)
        next_guess = get_highest_probability_element(frequency_matrix, taken_guess)
        response = requests.put(f'{base_url}/hangman', data={'token': token, 'letter': next_guess}).json()
        print(response)
        taken_guess.append(next_guess)
        state = response['hangman']
        if response['correct'] == False:
            number_of_wrong_steps -= 1
            list_of_all_words = eliminate_all_words_not_having_element(list_of_all_words, next_guess)
        else:  # correct response
            for i in range(state.count(next_guess)):
                index = state.find(next_guess)
                correct_word[index] = next_guess
                list_of_all_words = eliminate_all_words_not_having_element_index(
                    list_of_all_words, next_guess, state.find(next_guess), state.count(next_guess)
                )
                state = state.replace(next_guess, '_', 1)
            if len(correct_word) == len(state):  # we won
                return build_word(correct_word)
        print(build_word(correct_word))
        print(number_of_wrong_steps)
    return -1


print(solution())
