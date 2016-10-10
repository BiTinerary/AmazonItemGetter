import bottlenose
import bs4 as bs
import Tkinter as tk
from tkFileDialog import *

def center(toplevel): # Function for centerint root tKinter Window
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth() 
    h = toplevel.winfo_screenheight() 
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2 
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

try:
	r = open('AmazonAPICredz.txt') # Get Amazon API credentials
	accessKey = r.readline().rstrip('\n')
	secretAccess = r.readline().rstrip('\n')
	associatesID = r.readline().rstrip('\n')
	amazon = bottlenose.Amazon(accessKey, secretAccess, associatesID, MaxQPS=0.9) # Amazon allows 1 call/second. QPS Throttles each subsequent call to .9sec (since the request and response time > 1/10 second)
finally:
	r.close()

descriptionArray = [] # Store description of items
imgURlArray = [] #Store items iamge url
actualAveragePrice = [] # Mean average of every listings prices
_findAveragePrice = [] # Scratch pad array thats used for averaging items asking prices

def createHTMLOutputFile(): # This is the last thing to run. Gather up everything in static arrays and write/save/display to an html file. 
    i = 0 # Counter for starting static arrays at zero
    with open('index.html', 'w') as html: # Create file if not present, overwrite if is present.
        for everyItemFound in imgURlArray: # For every result found do the following.
            html.write("<p style='float: left; font-size: 20pt; text-align: center; width: 20%%; margin-right: 1%%; margin-bottom: 0.5em;'><img src='%s' style='width: 100%%'><b>Item:</b> %s<br><b>Price:</b> %s</img></p><br>" % (imgURlArray[i], descriptionArray[i][0:30], actualAveragePrice[i]))
            i += 1 # # 1 up the counter, so that the above for loop can enumerate through the static array index's being written to html file.
            print 'writing...'
        html.close() # Make sure to properly close index.html

def getAllInfo(keyWordSearch):
    description = amazon.ItemSearch(Keywords=keyWordSearch, SearchIndex="All") # Same, but for general description, etc...
    prices = amazon.ItemSearch(Keywords=keyWordSearch, SearchIndex="All", ResponseGroup="Offers") # Amazon API call for getting many listing prices of each items
    picture = amazon.ItemSearch(Keywords=keyWordSearch, SearchIndex="All", ResponseGroup="Images") # Amazon API calls for getting image URL of keyword variable

    apiCallArray = [description, prices, picture] # create Array of API call functions.
    for each in apiCallArray:  # Every keyword variable passed through this function will be put into 3 Amazon API calls to get their corresponding image, price, desc.
        soup = bs.BeautifulSoup(each, 'lxml') # Amazon API calls respond with XML source code. The 'each' is each XML source for images, price, desc.

        try: 
            if each == description:
                descriptionString = soup.title.string # Find <title> tag after being parsed by BeautifulSoup, then return only the string inside said tag.
                descriptionArray.append(str(descriptionString)) # Store this string into 'description' array.
                print descriptionString # Debugging
            else:
                pass
        except:
            descriptionArray.append('')
            print descriptionArray

        try:
            if each == prices:
                pricing = soup.find_all('formattedprice') # Find all occurances of 'formattedprice' tags and store in memory as a list.
                _findAveragePrice = [] # Create scratch array of many, many listings different asking prices (New, Used, Old...)
                for everyThing in pricing: # For every 'formattedprice' tag found
                    slurp = bs.BeautifulSoup(str(everyThing), 'lxml') # Parse each occurance of an asking price
                    for everyOne in slurp: #We are going to add up each asking price, to find the average cost.
                        _findAveragePrice.append(float(everyOne.formattedprice.string.lstrip('$'))) # strip '$' from asking price, so we can convert into a float $(21.99)
                if len(_findAveragePrice) > 10: # If there are more than 10 listings, the average might be skewed by low ballers or outliers.
                    while len(_findAveragePrice) > 10: # Since there are more than 10 asking prices, we are going to trim the fat.
                        _findAveragePrice.pop() # pop() removes the -1th (last) index until While loop is True
                    averageMeanPrice = sum(_findAveragePrice)/len(_findAveragePrice) # Find the mean average of every index (asking price) for a keyword
                else:
                    averageMeanPrice = sum(_findAveragePrice)/len(_findAveragePrice) # Otherwise, if there aren't more than 10 asking prices found, just find the average of all.
                actualAveragePrice.append(str(averageMeanPrice)) # Append the resulting, single averaged, asking price to a static array that will be used later.
                print str(averageMeanPrice) # Debuggin
            else:
                pass
        except:
            actualAveragePrice.append('')
            print actualAveragePrice

        try:
            if each == picture:
                imageString = soup.largeimage.url.string # Simply parse the string contents of <mediumimage> tag found in Amazon API .XML response.
                imgURlArray.append(str(imageString)) # append url string to static array that will be used later.
                print imageString # Debugging
            else:
                pass
        except:
            imgURlArray.append('http://i63.tinypic.com/ws1d9t.png') # Asign url to picture of a 'broken image' so that html doesnt display large empty border with borken link icon, in the event that Amazon API doesn't return one. 
            print imgURlArray
        
        createHTMLOutputFile() # Run function that creates HTML file and writes each items qualities to it. Easy for viewing URL images.

class mainApp(tk.Tk): # The core class for creating tkinter GUI
    def __init__(self):
        tk.Tk.__init__(self)
        def openFileButton(): # Create open file button and enumerate buttons depending on number of lines in file, and its description/price/image results.
            inputFile = askopenfile() 
            lines = inputFile.readlines() # read each line from select file
            
            i = 0 # Main loop for finding description, price, url for items.
            for each in lines:
                i += 1 # Counter for command line item number debugging
                getAllInfo(each) # Run function [that gets description/price/imageurl] for each keyword passed to it. (keyword is every line from selected file)
                # Place Try/Except here for trying keyword query (as seen above), if failed, then try passing a UPC?

            i = 1
            for description in descriptionArray: #Makes a button/label for each item found, then uses description as displayed text
                descriptionLabel = tk.Label(text=description, relief='ridge', width=50, anchor='w')
                descriptionLabel.grid(row=i, column=1, padx=5, pady=1) # Row number is enumerated for each index in array containing descriptions.
                i += 1

            i = 1
            for price in actualAveragePrice: # Makes a button/label for each item found, then uses pricing as displayed text.
                priceLabel = tk.Label(text='$'+price, relief='ridge', width=10, anchor='w')
                priceLabel.grid(row=i, column=2, padx=5, pady=1) # Row number is enumerated for each index in array containing prices.
                i += 1

        buttonBrowse = tk.Button(width=20, text='Browse', command=lambda: openFileButton()) #Button to manually and easily select any file from a directory.
        buttonBrowse.place(relx=.025, rely=.012, anchor="nw") #Gui positioning relative to x,y coordinates of whole frames dimensions.
        row0 = tk.Label(width=0, height=2)
        row0.grid(row=0)

        i = 20 # Arbitrary number of empty fields, which will later be filled with results
        while i > 0: # Another loop to create 12 labels with nothing as text to be displayed before selecting a file.
            initialLabel = tk.Label(text='', relief='ridge', width=50, anchor='w')
            initialLabel.grid(row=i, column=1, padx=5, pady=1) 
            formShape = tk.Label(width=10, relief= 'ridge', text='', anchor='w') # Same, but for smaller labels, intended for pricing.
            formShape.grid(row=i, column=2, padx=5, pady=1)
            i -= 1

if __name__ == "__main__":
    root = mainApp()
    root.resizable(0,0) # Not resizeable
    root.geometry("465x500") # Static width/height of tkinter GUI
    center(root) # call Center function on entire frame, so each run is displayed on same monitors coordinates
    root.title('Amazon Item Getter') # Name GUI Window
    root.mainloop() # Run it