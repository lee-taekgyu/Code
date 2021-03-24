sequence  = input("write your sequence : ")

def serch_palindromic(sequence):
    seq_dic = {'A':'T','T':'A','G':'C','C':'G'}
    Temp = []
    if len(sequence) % 2 == 0:
        for base in sequence:
            Temp += seq_dic[base]
            Temp = ''.join(Temp)
        if Temp[::-1] == sequence:
            return "This is palindromic"
        else:
            return "This is not palindromic"
    elif len(sequence) % 2 == 1:
        sequence = sequence.replace(sequence[int((len(sequence)-1)/2)],"")
        for base in sequence:
            Temp += seq_dic[base]
            Temp = ''.join(Temp)
        if Temp[::-1] == sequence:
            return "This is palindromic"
        else:
            return "This is not palindromic"

print(serch_palindromic(sequence))
