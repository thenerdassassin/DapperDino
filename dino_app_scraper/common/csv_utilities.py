import os
import csv

def generateFileName(dinoNumber):
    return 'dino_stats_' + str(dinoNumber) + ".csv"

def generateFileNames(dinoNumberList):
    return list(map(generateFileName, dinoNumberList))
    
def writeDinoFile(filename, stats):
    with open(filename, 'w') as csvFile:
        print("Writing " + filename)
        writer = csv.writer(csvFile)
        writer.writerows(stats)
    
def mergeCsvFiles(files, header = None, shouldDelete = True):
    # Create File for to merge into
    with open(generateFileName('last_run'), 'a') as mergedFile:
        writer = csv.writer(mergedFile)
        # if header exists, write the header
        if header != None:
            writer.writerow(header)
        for file in sorted(files):
            # Read Each file
            with open(file, 'r') as currentFile:
                currentCsv = csv.reader(currentFile)
                # Copy all the lines from the file to the merged file
                for lines in currentCsv:
                    writer.writerow(lines)
            # Delete temp files
            if shouldDelete == True:
                os.remove(file)