class ExceptionHunter(Exception):
    # print('Exception Hunter has been called for', Exception)
    pass

words = ['this', 'is', 'an', 'exception']

for word in words:
    if word == "an":
        raise ExceptionHunter(word)