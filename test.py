import bcrypt
import base64
class Password:
# Hashing a password
    def hash_password(self,plain_text_password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)

        # Encode the binary hash to Base64 and return as a string
        return base64.b64encode(hashed_password).decode('utf-8')

# Checking a password
    def check_password(self, plain_text_password, hhashed_password):
        # Decode the Base64-encoded hashed password to get the original binary hash
        hashed_password = base64.b64decode(hhashed_password)

        # Verify the password against the decoded binary hash
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)


