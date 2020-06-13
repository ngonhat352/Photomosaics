'''
WILL WORK IF COMM.BARRIER() WORKS...
'''
from PIL import Image
from createRGBDataset import createDataset
import time
from photomosaicsSEQ import correctResult
from mpi4py import MPI


# print(photomosaicsSEQ.correctResult)

def rescaleToPixels(inputImg):
    numPixelsWidth = 100      # WHERE THE SAMPLE SIZE WILL CHANGE
    pixelRatio = (numPixelsWidth / float(inputImg.size[0]))
    numPixelsHeight = int((float(inputImg.size[1]) * float(pixelRatio)))
    newImg = inputImg.resize((numPixelsWidth, numPixelsHeight), Image.ANTIALIAS)
    return newImg


'''
GET RGB of each pixel
= [R,G,B,a]
'''
def getPixelsOfPic(img):
    width, height = img.size
    pixels = []
    for j in range(0, height):
        for i in range(0, width):
            pixels.append([i,j,img.getpixel((i, j))])
    return pixels


def calculateBestColorFit(imgPixels, datasetPics):
    result = []
    comm = MPI.COMM_WORLD
    id = comm.Get_rank()            #number of the process running the code
    numProcesses = comm.Get_size()  #total number of processes running
    myHostName = MPI.Get_processor_name()  #machine name running the code

    REPS = len(imgPixels)
    print(id)
    print('\n')
    if (numProcesses <= REPS):

        for i in range(id, REPS, numProcesses):

    # for eachPix in imgPixels:
            eachPix = imgPixels[i]
            x = eachPix[0]
            y = eachPix[1]
            rgb = eachPix[2]
            if rgb[3] <= 150:   #To remove the color edges
                rgb = (255,255,255,255)

            minDifference = 9999

            for i in range(len(datasetPics)):
                diff = 0
                diff += abs(rgb[0] - int(datasetPics[i][1][0]))
                diff += abs(rgb[1] - int(datasetPics[i][1][1]))
                diff += abs(rgb[2] - int(datasetPics[i][1][2]))

                if diff < minDifference:
                    pic = datasetPics[i][2]
                    minDifference = diff

        result.append([x,y,pic])

    max = comm.reduce(diff, op=MPI.MAX)
    comm.Barrier()
    comm.barrier()

    return result


def createFinalPic(colorFitList, img, widthOfEach, heightOfEach):
    width, height = img.size
    finalImg = Image.new("RGB", (width * round(widthOfEach), height * round(heightOfEach)), color = "black")
    for i in range(0, len(colorFitList)):
        finalImg.paste(colorFitList[i][2],
                       (colorFitList[i][0] * round(widthOfEach), colorFitList[i][1] * round(heightOfEach)))

    finalImg.save("finalImg.png")
    # comm = MPI.COMM_WORLD
    # id = comm.Get_rank()            #number of the process running the code
    # numProcesses = comm.Get_size()  #total number of processes running
    # myHostName = MPI.Get_processor_name()  #machine name running the code
    #
    #
    # # print(numProcesses)
    # if (numProcesses <= len(colorFitList)):
    #     for i in range(id, len(colorFitList), numProcesses):
    #
    # #     # if i%numProcesses!=id: continue
    #         finalImg.paste(colorFitList[i][2],
    #                    (colorFitList[i][0] * round(widthOfEach), colorFitList[i][1] * round(heightOfEach)))
    # comm.Barrier()
    # finalImg.save("finalImg.png")
    # finalImg.show()
    return finalImg

def checkFinalImg(finalImg, correctResult):
    result = getPixelsOfPic(rescaleToPixels(finalImg))
    for i in range(len(result)):
        if result[i] != correctResult[i]:
            return False
    return True

if __name__ == "__main__":
    processedData = createDataset()
    dataset = processedData[0]
    widthOfEach = processedData[1]
    heightOfEach = processedData[2]


    # inputImg = input("Name of picture to convert into Photomosaics:  ")
    inputImg = 'bulbasaur.png'
    inputImage = Image.open(inputImg).convert("RGBA")

    s1 = time.perf_counter()
    rescaledInputImg = rescaleToPixels(inputImage)
    f1 = time.perf_counter()
    print(f'RescaleToPixels finished in {round(f1-s1, 2)} second(s)')

    s2 = time.perf_counter()
    pixelsList = getPixelsOfPic(rescaledInputImg)
    f2 = time.perf_counter()
    print(f'getPixelsOfPic finished in {round(f2-s2, 2)} second(s)')

    # print(len(pixelsList))
    # smallerParts = comm.Scatter(pixelsList, root=0)
    # print(len(smallerParts))

    s3 = time.perf_counter()
    colorFitList = calculateBestColorFit(pixelsList, dataset)
    # print(colorFitList)
    f3 = time.perf_counter()
    print(f'CalculateBestColorFit finished in {round(f3-s3, 2)} second(s)')

    s4 = time.perf_counter()
    finalImg = createFinalPic(colorFitList, rescaledInputImg, widthOfEach, heightOfEach)
    f4 = time.perf_counter()
    print(f'CreateFinalPic finished in {round(f4-s4, 2)} second(s)')

    test = checkFinalImg(finalImg, correctResult)
    print(test)
#calculateBestColorFit and createFinalPic were the two out of 4 functions in ConvertToPhotomosaicsSEQ
# that are the mose expensive:
# ~8s for calculate and ~8.7s for createFinalPic (widthpixels = 100)
# 32.7s for calculate and
