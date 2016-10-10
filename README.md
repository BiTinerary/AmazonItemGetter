# AmazonItemAPI
GUI for getting Bulk Amazon listing descriptions and prices via API.

## Over all
End user friendly tkinter GUI for conducting 1 Amazon search/second for each line in selected spreadsheet. Outputing results to `.html` file which can then be analyzed to see the average 'for sale' prices and double check accuracy of search results by displaying images and description.<br>
<br>
<img src='https://github.com/BiTinerary/AmazonItemGetter/blob/master/Untitled.png'></img>
<br>
##Note:
* GUI lists first 20 items (lines in selected `.csv` file) followed by average price (of <=10 listings) for each item.
* However, API calls are done for every line in selected `.csv/`, anything more will be appended to an `output.html`
<br>

###TODO
* <strike>Revise Log.txt write to sort/write 3 seperate array's instead of old 'master' 3d matrix nightmare.</strike><br>
 * <strike>(for now just open in any spreadsheet and sort by column)</strike>
* Add option to manually enter column number corresponding to manufacturer's arbitrary spreadsheet headers.
 * This will remove the copy/pasting of desired column to new file
 * <strike>open file as binary to remove any potential conflict with programatic syntax (ie: `'`,`"`, `,`, etc...)</strike> Not A prob so far...
 * <strike>or `var.strip(',')` to maintain keyword search accuracy?</strike>
* Add Multiple file selection
* Review Amazon API info for searching via <strike>UPC</strike>, MID, ASIN, etc... not just keywords. Can add UPC function call to main `try/except` loop later.

###HTML Output Example
<br>
<img src='https://github.com/BiTinerary/AmazonItemGetter/blob/master/Untitledhtml.png'></img>
<br>
