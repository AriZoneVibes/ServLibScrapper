#libraries
import re
import time
from fpdf import FPDF
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pdf = FPDF()

#Settings
cdexe = r"C:\Portable\Chromedriver\chromedriver.exe"
Url = "https://servlib.com/lg/washing-machine/f1695rdh.html?start=0"
#Url of one of the pages

StartPage = 1 #First page to export
EndPage = 69 #Last page to export
MakePdf = True #If will export the final file as PDF

#Variables
CurrentPage = StartPage
imagelist = [] #Store downloaded images

#Start Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service(executable_path=cdexe)
driver = Chrome(service=service, options=chrome_options)

#Trim page number from URL
n = Url.rfind("=") #Find and store location of last occurance of "="
Url = Url[slice(n+1)] #Cut the Url at the location stored, leaving the left part
print("Downloading from: " + Url) #Show trimmed URL
print("")
#Download and save images
for CurrentPage in range(StartPage-1, EndPage): #Repeat the download process through the indicated pages,
    print("Downloading Page: " + str(CurrentPage))
    CurrentUrl = Url + str(CurrentPage) #Build the link for the page to download

    driver.get(CurrentUrl) #Open website with image, then locate it
    div = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//div[@class='pdfbg'][contains(@style,'-{CurrentPage+1}.png')]")))

    #Extract a possible scaling from CSS style tag, then resize browser window
    Scale = float(
        re.match(r".*scale\((.*)\).*", div.get_attribute("style")).groups()[0])
    NeededHeight = div.location["y"] + div.size["height"] * Scale
    print(f"Setting window size to make image fully visible ({NeededHeight})")
    driver.set_window_size(1920, NeededHeight)
    time.sleep(2)

    #Save the image
    imageFilename = f"P{CurrentPage:02.0f}.png"
    div.screenshot(imageFilename)
    imagelist.append(imageFilename) #Add the file to a list to build the PDF file later

    print("Downloaded")

#Take the images and convert them to PDF
if MakePdf == True: #See if the Settings state it should create a PDF file
    for image in imagelist: #Repeat for every entry on the images list
        pdf.add_page() #Create a blank page on the file
        pdf.image(image) #Place image on page
    pdf.output("manual.pdf", "F") #Save File
    print("Manual Saved!")
