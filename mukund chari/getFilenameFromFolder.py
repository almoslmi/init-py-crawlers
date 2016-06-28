import glob
import os

inpFileList = glob.glob("E:\\UT\\new consolidation 19dec\\*.html")

for inpFile in inpFileList:
    # print inpFile
    # break
    findDelimit1 = inpFile.find('final_dump')
    # findDelimit2 = inpFile.find('.html')
    link = inpFile[len("E:\\UT\\new consolidation 19dec\\"):]
    print link.replace('.html','').strip()
    # print link
    # break