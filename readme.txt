Application is used to extract phone numbers and path to logo from webpage represented by provided url.

Before running the script install all necessary modules which are listed in requirements.txt. You can do it by running command:
$ pip install -r requirements.txt 


extract.py is a entrance point of the application. Script expects url to the website to be passed as the first program argument.
Example of running the script:
$ python3 extract.py https://contact.pepsico.com/pepsi

Program has two lines of output. First one contains phone numbers found on the webpage and the second one contains
url to the logo used in the webpage. If program found no phone numbers on the webpage, output of the first line is None.
If program found no logo url on the webpage, output of the second line is None.
Example output:
(800) 433 2652, 1 800 433 2652, 1 833 548 0119
https://contact.pepsico.com/pepsi/files/pepsi/brands/1692797414/Pepsi_New_Logo@2x.png


Phone number extraction is done by collecting all possible phone numbers from the page. This phone numbers 
are then processed in two phases:
	1) While collecting numbers we collect numbers prefixes as well. If prefix contains some of the key words like
	   "Phone", "Tel" or "Fax" number is accepted as the phone number.
	2) All numbers that are not accepted in the first stage continue to the second stage.
	   Here we apply number of filters on numbers trying to filter out phone numbers from other types of numbers.
	   For example we filter out dates, decimal numbers, numbers to short to be a phone number and so on.

Logo path extraction works by collecting all <img> tags as well as their parent tags from the html document. In this
tags we are searching for mention of some key words like "logo" or "icon". If we find multiple tags containing key
words we pick one that is most probable. 
