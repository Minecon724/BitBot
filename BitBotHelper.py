class Konfiguracje:
    
    def ZablokujRadio(serwer):
        plik = open("/home/pi/bitbotdata/konfiguracje/radio/" + serwer, "w")
        plik.write("zablokowane")
        plik.close()

    def OdblokujRadio(serwer):
        plik = open("/home/pi/bitbotdata/konfiguracje/radio/" + serwer, "w")
        plik.write("odblokowane")
        plik.close()

    def RadioCzyZablokowane(serwer):
        try:
            plik = open("/home/pi/bitbotdata/konfiguracje/radio/" + serwer, "r")
            if plik.read() == "zablokowane":
                return True
            else:
                return False
        except:
            return False
        plik.close()

    def JoinDM(serwer):
        try:
            plik = open("/home/pi/bitbotdata/konfiguracje/joindm/" + serwer, "r")
            return plik.read()
        except:
            return "null"
        plik.close()

    def RemoveDM(serwer):
        try:
            plik = open("/home/pi/bitbotdata/konfiguracje/removedm/" + serwer, "r")
            return plik.read()
        except:
            return "null"
        plik.close()

    def UstawRemoveDM(serwer, wartosc):
        plik = open("/home/pi/bitbotdata/konfiguracje/removedm/" + serwer, "w")
        plik.write(wartosc)
        plik.close()

    def UstawJoinDM(serwer, wartosc):
        plik = open("/home/pi/bitbotdata/konfiguracje/joindm/" + serwer, "w")
        plik.write(wartosc)
        plik.close()
