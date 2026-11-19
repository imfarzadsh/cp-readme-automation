def is_palindrome(x: int) -> bool:
    return x >= 0 and str(x) == str(x)[::-1]
