from bad_words import BAD_WORDS


m = 'это Обычный текст на замену, Буквы на звездочки'

# проверка и замена
n = m.split()
for i in n:
    if i.lower() in BAD_WORDS:
       m = m.replace(i, (i[0] + '*' * (len(i) - 1)))