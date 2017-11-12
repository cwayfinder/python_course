def validator(s: str):
    opening = '({{'
    closing = ')]}'

    for i in range(len(opening)):
        b1 = s.find(opening[i])
        b2 = s.find(closing[i], b1)

        if b1 == -1 and b2 == -1:
            continue  # The pair of brackets has not been found in the string. Try another pair

        if b2 == -1:
            return False  # Only opening bracket has been found; the closing one is absent

        s1 = s[:b1]
        s2 = s[b1 + 1:b2]
        s3 = s[b2 + 1:]

        if closing[i] in s1:
            return False  # A closing bracket has been found in front of the opening one

        if not (validator(s2) and validator(s3)):
            return False

    return True


print(validator('ah_(some_[text])_bla_bla'))
print(validator('ah  )(some [text]) bla bla'))
print(validator('ah  ((some [text]) bla bla'))
