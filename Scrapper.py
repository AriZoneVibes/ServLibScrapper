#libraries
import requests
from fpdf import FPDF

pdf = FPDF()

#Settings
Url = "https://servlib.com/disk/panasonic/fax/kx-ft33la/html/km79804202c3-1.png"
#Url you got on the previous step, should look like: https://servlib.com/disk/panasonic/fax/kx-ft33la/html/km79804202c3-1.png

StartPage = 1 #First page to export
EndPage = 127 #Last page to export
MakePdf = True #If will export the final file as PDF

#Variables
CurrentPage = StartPage
imagelist = [] #Store downloaded images

#Trim page number from URL
n = Url.rfind("-") #Find and store location of last occurance of "-"
Url = Url[slice(n+1)] #Cut the Url at the location stored, leaving the left part
print("Downloading from: " + Url) #Show trimmed URL
print("")
#Download and save images
for CurrentPage in range(StartPage,EndPage+1): #Repeat the download process through the indicated pages,
    print("Downloading Page: " + str(CurrentPage))
    CurrentUrl = Url + str(CurrentPage) + ".png" #Build the link for the page to download

    r = requests.get(CurrentUrl, stream=True) #Ask the website for the image
    #Save the image
    file = open(str(CurrentPage) + ".png", "wb")
    file.write(r.content)
    file.close()
    
    imagelist.append(str(CurrentPage) + ".png") #Add the file to a list to build the PDF file later

    print("Downloaded")
    pass

#Take the images and convert them to PDF
if MakePdf == True: #See if the Settings state it should create a PDF file
    for image in imagelist: #Repeat for every entry on the images list
        pdf.add_page() #Create a blank page on the file
        pdf.image(image,0,0,210) #Place image on page
    pdf.output("manual.pdf", "F") #Save File
    print("Manual Saved!")
