from box import Box


def main():
        weigth = 122
        width = 2257
        height = 944
        bx = Box(weigth,width,height)
        bx.genTrackNo()
        box = bx.getBox()
        print(box['trackNo'])
        bx.addBox()

if __name__ =="__main__":
    main()