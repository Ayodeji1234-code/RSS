email = input('Enter your e-mail (firstname.secondname@gmail.com): ')

# Find the position of '.' and '@'
dot_index = email.find('.')
at_index = email.find('@')

# Slice from start up to the dot
first_name = email[:dot_index]

print("First name:", first_name)
