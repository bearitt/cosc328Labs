try:
    with open('./client/test.txt','r') as f:
        read_data = f.read()
        print(read_data)
except IOError:
    print('File not found!')
