from cs50 import get_string


def main():
    s = get_string("Text: ")

    letters = 0
    word = 0
    sentences = 0
    n = len(s)

    if s[0].isalnum() == True:
        word += 1
# All 3 cases for letters,words and sentences
    for i in range(n):
        if s[i].isalpha() == True:
            letters = letters + 1
        if ((s[i].isspace() == True) and ((s[i+1].isalnum() == True) or s[i+1] == '"')):
            word += 1
        if (s[i] == '!' or s[i] == '?' or s[i] == '.') and (s[i-1].isalnum() == True):
            sentences += 1

# Coleman-lian index
    grade = 0.0588*(100.0*letters/word) - 0.296*(100.0*sentences/word) - 15.8

# round the result
    num = round(grade)

    if num <= 1:
        print("Before Grade 1\n")
    elif num > 16:
        print("Grade 16+\n")
    else:
        print("Grade", str(num))


if __name__ == "__main__":
    main()