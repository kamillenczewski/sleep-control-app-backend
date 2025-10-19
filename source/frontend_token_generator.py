from uuid import uuid4

def generatePart():
    return uuid4().__str__().replace('-', '')

def generate():
    return generatePart() + generatePart()

if __name__ == '__main__':
    print(generate())