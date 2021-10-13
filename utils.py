import re
from validate_email import validate_email

pass_reguex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\W_]{8,}$"


def isEmailValid(email):
    is_valid = validate_email(email)
    return is_valid


def isPasswordValid(password):
    if re.search(pass_reguex, password):
        return True
    else:
        return False

def sumarCamisas(camisas):
    retorno=[]
    esta=False
    for i in camisas:
        for j in retorno:
            if i[2]==j[2]:
                insert=[j[0]+i[0],j[1],j[2]]
                print(insert)
                retorno.remove(j)
                retorno.append(insert)
                esta=True
                break
        if not esta:
            retorno.append(i)
        esta=False
    return retorno


