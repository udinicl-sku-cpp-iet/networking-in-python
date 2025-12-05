with open("myoutput.txt","r") as a:
    with open("example1_output.txt","r") as b:
        if a.read() == b.read():
            print("weom")
        else:
            print("youlose")
