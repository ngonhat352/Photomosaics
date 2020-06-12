from PIL import Image


def calculateRGBofEach(img):
    newImg = img.resize((1, 1), Image.ANTIALIAS)
    colors = newImg.getpixel((0, 0))

    red = colors[0]
    green = colors[1]
    blue = colors[2]

    return red, green, blue


def cropEach(x, y, datasetImg, widthOfEach, heightOfEach):
    imgOfEach = datasetImg.crop((x * widthOfEach, y * heightOfEach, x * widthOfEach + widthOfEach, y * heightOfEach + heightOfEach))
    return imgOfEach


def createDataset():
    # dataset = input("Your dataset picture (for example: pokemon_dataset.png):   ")
    dataset = 'pokemon_dataset.png'
    datasetName = dataset[:-4] + "_RGBList.txt"

    # dimensions = input("Dimensions of the dataset picture (number of columns and number of rows):   ")
    dimensions = '28 18'
    dimensions = dimensions.split()
    numCols = int(dimensions[0])
    numRows = int(dimensions[1])

    datasetImg = Image.open(dataset).convert("RGBA")
    width, height = datasetImg.size

    widthOfEach = int(width / numCols)
    heightOfEach = int(height / numRows)

    result = []
    for j in range(0, numRows):
        for i in range(0, numCols):
            onePic = []
            onePic.append((i, j))
            eachPic = cropEach(i, j, datasetImg, widthOfEach, heightOfEach)
            onePic.append(calculateRGBofEach(eachPic))
            onePic.append(eachPic)
            result.append(onePic)

    return result, widthOfEach, heightOfEach