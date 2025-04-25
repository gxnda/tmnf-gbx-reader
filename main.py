from headers import read_header

def read_gbx(file):
    with open(file, "rb") as f:
        headers, user_data = read_header(f)
        print(headers)

if __name__ == "__main__":
    read_gbx("Circles of hell.Challenge.Gbx")