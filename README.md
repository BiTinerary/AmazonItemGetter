# AmazonItemAPI
GUI for getting Bulk Amazon listing descriptions and prices via API.

## Over all
End user friendly tkinter GUI for conducting hundreds of amazon searches/minute by selecting a spreadsheet. Outputing results to `.csv/.xlsx` which can then be analyzed to see the best 'for sale' prices.<br>
<br>
<img src='https://github.com/BiTinerary/AmazonItemAPI/blob/master/work%20in%20progress2.png'></img>
<br>
##Note:
* GUI lists only first 4 items (lines in selected `.csv` file) followed by 3 different listings for each item.
* However, API calls are done for every line in selected `.csv`, anything more will be appended to an `output.csv`
<br>

###TODO
* Revise Log.txt write to sort/write 3 seperate array's instead of old 'master' 3d matrix nightmare.<br>
 * (for now just open in any spreadsheet and sort by column)
* Add option to manually enter column number corresponding to manufacturer's arbitrary spreadsheet headers.
 * This will remove the copy/pasting of desired column to new file
 * open file as binary to remove any potential conflict with programatic syntax (ie: `'`,`"`, `,`, etc...)
 * or `var.strip(',')` to maintain keyword search accuracy?
* Add Multiple file selection
* Review Amazon API info for searching via UPC, MID, ASIN, etc... not just keywords.