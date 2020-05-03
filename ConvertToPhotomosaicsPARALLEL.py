from PIL import Image
from MakeRGBDataset import cropEach, createDataset, processDataset
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from threading import current_thread # SOLUTION


def rescaleToPixels(inputImg):
    numPixelsWidth = 100      # WHERE THE SAMPLE SIZE WILL CHANGE
    pixelRatio = (numPixelsWidth / float(inputImg.size[0]))
    numPixelsHeight = int((float(inputImg.size[1]) * float(pixelRatio)))
    newImg = inputImg.resize((numPixelsWidth, numPixelsHeight), Image.ANTIALIAS)
    return newImg


def getPixelsOfPic(img):
    width, height = img.size
    pixels = []
    for j in range(0, height):
        for i in range(0, width):
            pixels.append(img.getpixel((i, j)))
    return pixels


def calculateBestColorFit(rgb, datasetPics):
        result = []

    # for rgb in imgPixels:
        if rgb[3] <= 150:   #To remove the color edges
            rgb = (255,255,255,255)

        minDifference = 9999
        x = 0
        y = 0
        for i in range(len(datasetPics)):
            diff = 0
            diff += abs(rgb[0] - int(datasetPics[i][2]))
            diff += abs(rgb[1] - int(datasetPics[i][3]))
            diff += abs(rgb[2] - int(datasetPics[i][4]))

            if diff < minDifference :
                x = int(datasetPics[i][0])
                y = int(datasetPics[i][1])
                minDifference = diff

        result.append([x,y])

        return result


def createFinalPic(colorFitList, img, widthOfEach, heightOfEach):
    width, height = img.size
    finalImg = Image.new("RGB", (width * round(widthOfEach), height * round(heightOfEach)), color = "black")

    rangeX = 0
    rangeY = 0
    for i in range(0, len(colorFitList)):
        if rangeX >= width:
            rangeY += 1
            rangeX = 0
        finalImg.paste(cropEach(colorFitList[i][1], colorFitList[i][0], datasetImg, widthOfEach, heightOfEach),
                       (rangeX * round(widthOfEach), rangeY * round(heightOfEach)),
                       cropEach(colorFitList[i][1], colorFitList[i][0], datasetImg, widthOfEach, heightOfEach))
        rangeX += 1
    finalImg.save("finalImg.png")
    # finalImg.show()


if __name__ == "__main__":
    datasetName, datasetImg = createDataset()
    processedData = processDataset(datasetName)
    dataset = processedData[0]
    widthOfEach = processedData[1]
    heightOfEach = processedData[2]

    # inputImg = input("Name of picture to convert into Photomosaics:  ")
    inputImg = 'lorsan.png'
    inputImage = Image.open(inputImg).convert("RGBA")

    s1 = time.perf_counter()
    rescaledInputImg = rescaleToPixels(inputImage)
    f1 = time.perf_counter()
    print(f'RescaleToPixels finished in {round(f1-s1, 2)} second(s)')

    s2 = time.perf_counter()
    pixelsList = getPixelsOfPic(rescaledInputImg)
    f2 = time.perf_counter()
    print(f'getPixelsOfPic finished in {round(f2-s2, 2)} second(s)')

    s3 = time.perf_counter()
    # colorFitList = calculateBestColorFit(pixelsList, dataset)
    colorFitList = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = [executor.submit(calculateBestColorFit, rgb, dataset)
                           for rgb in pixelsList]
        print(current_thread().name)
        for i in as_completed(results):
            colorFitList.append(i.result()[0])
    # print(colorFitList)
    f3 = time.perf_counter()
    print(f'CalculateBestColorFit finished in {round(f3-s3, 2)} second(s)')

    s4 = time.perf_counter()
    createFinalPic(colorFitList, rescaledInputImg, widthOfEach, heightOfEach)
    f4 = time.perf_counter()
    print(f'CreateFinalPic finished in {round(f4-s4, 2)} second(s)')


#calculateBestColorFit and createFinalPic were the two out of 4 functions in ConvertToPhotomosaicsSEQ
# that are the mose expensive:
# ~8s for calculate and ~8.7s for createFinalPic (widthpixels = 100)
# 32.7s for calculate and