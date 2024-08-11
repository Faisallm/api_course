from passlib.context import CryptContext

# we are telling passlib what hashing algorithm...
# we want to use.
pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    # compares the plain and hashed password
    # returns true or false
    return pwd_context.verify(plain_password, hashed_password)