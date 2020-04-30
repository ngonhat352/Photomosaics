﻿from PIL import Image
from MakeRGBDataset import cropEach, createDataset, processDataset


def rescaleToPixels(inputImg):
    numPixelsWidth = 100      # WHERE THE SAMPLE SIZE WILL CHANGE
    pixelRatio = (numPixelsWidth / float(inputImg.size[0]))
    numPixelsHeight = int((float(inputImg.size[1]) * float(pixelRatio)))
    newImg = inputImg.resize((numPixelsWidth, numPixelsHeight), Image.ANTIALIAS)
    return newImg


def getPixelsOfPic(img):
    width,height = img.size
    pixels = []
    for j in range(0, height):
        for i in range(0, width):
            pixels.append(img.getpixel((i, j)))
    return pixels


def calculateBestColorFit(imgPixels, datasetPics):
    result = []

    for rgb in imgPixels:
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
    finalImg.show()


if __name__ == "__main__":
    datasetName, datasetImg = createDataset()
    processedData = processDataset(datasetName)
    dataset = processedData[0]
    widthOfEach = processedData[1]
    heightOfEach = processedData[2]

    inputImg = input("Name of picture to convert into Photomosaics:  ")
    inputImage = Image.open(inputImg).convert("RGBA")

    rescaledInputImg = rescaleToPixels(inputImage)
    pixelsList = getPixelsOfPic(rescaledInputImg)
    colorFitList = calculateBestColorFit(pixelsList, dataset)

    createFinalPic(colorFitList, rescaledInputImg, widthOfEach, heightOfEach)
