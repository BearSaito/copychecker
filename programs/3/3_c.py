def main(a):
    for i, j in enumerate(a):
        print(f"{i}:{j}")

if __name__ == '__main__':
    a = [i for i in range(10)]
    main(a)