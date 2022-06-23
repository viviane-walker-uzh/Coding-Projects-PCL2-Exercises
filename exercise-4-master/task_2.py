# authors: Viviane Walker, Micha David Hess

# we figured the encoding like this in the terminal:
# Vivis-MacBook-Air:exercise-4 vivianewalker$ file -I encoding_1.txt
# encoding_1.txt: text/plain; charset=us-ascii
# Vivis-MacBook-Air:exercise-4 vivianewalker$ file -I encoding_2.txt
# encoding_2.txt: text/plain; charset=iso-8859-1
# Vivis-MacBook-Air:exercise-4 vivianewalker$ 

# therefore we know now that encoding_1 --> ascii
# encoding_2 --> iso

# also: encoding_2.txt contains characters that aren't in the ASCII charset, such as 'àêé'.

with open("encoding_utf-8.txt", "w", encoding="utf-8") as f3:
    with open("encoding_1.txt", "r", encoding="ISO 8859-1") as f1:
        lines_f1 = f1.readlines()
        lines_f1_utf8 = [f3.write(line) for line in lines_f1]

    with open("encoding_1.txt", "r", encoding="us-ascii") as f2:
        lines_f2 = f2.readlines()
        lines_f2_utf8 = [f3.write(line) for line in lines_f2]


