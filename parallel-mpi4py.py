'''

'''
from PIL import Image
from createRGBDataset import createDataset
import time
from mpi4py import MPI


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


def calculateBestColorFit(eachPix, datasetPics):
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
    return [x,y,pic]

def createFinalPic(colorFitList, img, widthOfEach, heightOfEach):
    width, height = img.size
    finalImg = Image.new("RGB", (width * round(widthOfEach), height * round(heightOfEach)), color = "black")
    for i in range(0, len(colorFitList)):
        finalImg.paste(colorFitList[i][2],
                       (colorFitList[i][0] * round(widthOfEach), colorFitList[i][1] * round(heightOfEach)))

    finalImg.save("finalImg.png")
    return finalImg

def checkFinalImg(finalImg, correctResult):
    result = getPixelsOfPic(rescaleToPixels(finalImg))
    for i in range(len(result)):
        if result[i] != correctResult[i]:
            return False
    return True


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    id = comm.Get_rank()            #number of the process running the code
    numProcesses = comm.Get_size()  #total number of processes running

    print("\n ----- PARALLEL -----" + str(id))
    if(id==0):
        processedData = createDataset()
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

    else:
        dataset = []
        pixelsList = []


    pixelsList = comm.bcast(pixelsList, root = 0)
    colorFitList = []
    dataset = comm.bcast(dataset, root = 0)
    s3 = time.perf_counter()
    REPS = len(pixelsList)
    if ((REPS % numProcesses) == 0 and numProcesses <= REPS):
        # How much of the loop should a process work on?
        chunkSize = int(REPS / numProcesses)
        start = id * chunkSize
        stop = start + chunkSize
        # do the work within the range set aside for this process
        for i in range(start, stop):
            colorFitList.append(calculateBestColorFit(pixelsList[i], dataset))

    sum = comm.reduce(colorFitList, op=MPI.SUM)

    f3 = time.perf_counter()
    print(f'CalculateBestColorFit finished in {round(f3-s3, 2)} second(s)')

    if(id==0):

        from photomosaicsSEQ import correctResult
        print("\n ----- PARALLEL -----" + str(id))

        s4 = time.perf_counter()
        finalImg = createFinalPic(sum, rescaledInputImg, widthOfEach, heightOfEach)
        f4 = time.perf_counter()
        print(f'CreateFinalPic finished in {round(f4-s4, 2)} second(s)')

        test = checkFinalImg(finalImg, correctResult)
        print(test)
