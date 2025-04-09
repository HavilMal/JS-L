import time, sys, os


def tail(filename):
    # with open(filename, "r") as file:
    with sys.stdin as file:
        # znajdujemy początkową pozycję pliku
        # file.seek(0)
        while True:
            # zapisujemy aktualną pozycję pliku
            # current_position = file.tell()
            line = file.readline()
            if not line:
                # jeśli nie ma nowych linii, czekamy chwilę
                time.sleep(0.1)

                # weryfikujemy rozmiar pliku
                # current_size = os.stat(filename).st_size

                # jeśli obecna pozycja jest dalej,
                # niż rozmiar pliku, przesuwamy na początek
                # if current_position > current_size:
                #     file.seek(0)
            else:
                # jeśli mamy nową linię, wypisujemy ją na ekran
                sys.stdout.write(line)
                sys.stdout.flush()


if __name__ == "__main__":
    # try:
    #     tail(sys.argv[1])
    # except IndexError:
    #     print("Please provide first argument.")
    tail("")
