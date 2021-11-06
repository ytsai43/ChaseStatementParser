import PyPDF2
import configparser
import os
import pandas as pd


def convertStatement(fileName, inputPath=".", outputPath=".\csv"):
    """
    Parseing row PDF table and combine all transactions in one table
    """
    print("INFO: Parseing row PDF table and combine all transactions in one table...")
    pdf_file = open(os.path.join(inputPath, fileName), 'rb')
    # pdf_file = open("%s\%s" %(inputPath,fileName),'rb')
    pdf_object = PyPDF2.PdfFileReader(pdf_file)
    if pdf_object.isEncrypted == True:
        pdf_object.decrypt("")

    numPages = pdf_object.getNumPages()
    allTextList = []
    for page in range(2, numPages):
        allTextList += pdf_object.getPage(page).extractText().split("\n")

    """
    Data cleaning for unnecessary rows
    """
    print("INFO: Data cleaning to remove unnecessary rows...")
    firstTranDateIdx = [idx for idx, s in enumerate(allTextList) if 'Payment Thank You-Mobile' in s][0]
    firstTranDate = allTextList[firstTranDateIdx][-6:]
    tailIndex = [idx for idx, s in enumerate(allTextList) if 'Total fees charged in' in s][0]
    tableList = allTextList[firstTranDateIdx + 1:tailIndex]
    tableList.insert(0, firstTranDate)

    """
    Extract information and put in final table
    """
    print("INFO: Extract information and put in final table...")
    rawData = pd.DataFrame(tableList, columns=["rawData"])
    idxTranNTD = rawData[rawData['rawData'].str.contains('EXCHG RATE')].index
    idxTranDate = idxTranNTD - 3
    idxTranName = idxTranNTD - 2
    idxTranUSD = idxTranNTD - 1

    NTD = rawData.iloc[idxTranNTD]["rawData"].str.split("X", 1).apply(lambda x: x[0])
    USD = rawData.iloc[idxTranUSD]["rawData"].str.split("/", 1).apply(lambda x: x[0][:-2])
    DATE = rawData.iloc[idxTranDate]["rawData"].apply(lambda x: x[-6:] if len(x) > 6 else x)#(lambda x: x[-5:] if len(x) > 5 else x)
    TranName = rawData.iloc[idxTranName]["rawData"]

    finalTable = pd.DataFrame(data={"日期": (DATE),
                                    "商家名稱": list(TranName),
                                    "NTD": list(NTD),
                                    "USD": list(USD)})

    """
    Export to CSV
    """
    finalTable.to_csv(os.path.join(outputPath, fileName[:-4]+'.csv'), header=True, index=False, encoding='utf_8_sig')
    pdf_file.close()
    print("INFO: Program is completed and CSV is generated.")


def main():
    parser = configparser.ConfigParser()
    parser.read("config.txt")

    inputDirectory = parser.get("config", "INPUT_DIRECTORY")
    outputDirectory = parser.get("config", "OUTPUT_DIRECTORY")
    pdfFileName = parser.get("config", "PDF_FILENAME")

    convertStatement(pdfFileName, inputDirectory, outputDirectory)


if __name__ == "__main__":
    main()
