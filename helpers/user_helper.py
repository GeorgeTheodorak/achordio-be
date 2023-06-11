import random
import string

def generateRandomVerificationCode():
    characters = string.ascii_letters + string.digits
    code_length = 6  # You can adjust the code length as needed
    verification_code = ''.join(random.choices(characters, k=code_length))
    return verification_code


