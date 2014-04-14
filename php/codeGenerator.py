import random
import string

length = 10
chars = string.ascii_lowercase + string.digits
codice = ''.join(random.choice(chars) for i in range(length))
print codice