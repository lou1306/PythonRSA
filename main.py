"""
Luca Di Stefano --- 235068
Ing. Informatica e Automatica
"""

from RSA import RSAKey, RSAMessage
def main():
    k = RSAKey.generate(1024)
    print("--- Chiave RSA ---")
    print(k)
    print("------------------")
    m = input("Inserisci il messaggio da crittografare: ")
    
    msg = RSAMessage(m)
    c = msg.encrypt(k.publicKey())
    print("--- Messaggio crittografato ---")
    print(c)
    print("-------------------------------")

    del m # Il messaggio originale non è più in memoria
    m1 = RSAMessage.decrypt(c, k)
    print("--- Recupero il testo in chiaro ---")
    print(m1)
    print("-----------------------------------")
    
    input("Premere invio per continuare.")
    
    print("--- Attacco di Wiener: dimostrazione ---")
    print("Genero una chiave vulnerabile...")
    k1 = RSAKey.weakGenerate(1024)
    print(k1)
    
    input("Premere invio per continuare.")
    
    e = k1.e
    n = k1.n
    del k1
    print("Eseguo l'attacco...")
    k2 = RSAKey.WienersAttack(e, n)
    if k2 != False:
        print("Attacco riuscito:")
        print(k2)
    
if __name__ == '__main__':
    main()