from bs4 import BeautifulSoup
import requests
import sys
import os.path
"""
Colin Lambe
A Webscraper to get the number of words, number of claps, and article text from articles on Medium.com
Uses BeatifulSoup4 and Requests
"""
class MediumScraper:

    def scrape(self, url, minWords, minClaps):

        #gets the article source code from the url
        source = requests.get(url).text
        page = BeautifulSoup(source, "lxml")

        #the article itself still with html context
        article = page.find('article')

        #the name of the article
        name = article.find('h1').text

        #if file already exists don't save again
        stripped_name = name.replace(" ", "")
        if os.path.isfile(f"./{stripped_name}.txt") :
            print("File has already been processed")

        else:
            #gather the html free text of the article from the paragraph tags
            text = []
            for par in article.find_all('p'):
                text = text + par.text.split(" ")
            #finds the claps button and determines the number of claps
            for button in page.find_all('button'):
                if "claps" in button.text:
                    num_claps = button.text
                    num_claps = num_claps.split(" ")[0]
                    if "K" in num_claps:
                        num_claps = int(float(num_claps.replace("K", "")) * 1000)
                    elif "M" in num_claps:
                        num_claps = int(float(num_claps.replace("M", "")) * 1000000)
                    else:
                        num_claps = int(num_claps)

            if text.__len__() > minWords:
                if num_claps > minClaps:
                    MediumScraper.save_contents(self, url, name, text.__len__(), num_claps, " ".join(text))
                else:
                    print("Not Enough Claps")
            else:
                print("Not Enough Words")


    """ Saves the article to a file
    file name is the name of the article with white space removed and .txt extension
    file format follows: 
    
    name
    url
    number of words
    number of claps
    
    article text
    """
    def save_contents(self,url, name, words, claps, text):
        stripped_name = name.replace(" ", '')
        file = open(f"{stripped_name}.txt", "w")
        file.write(f"""Article Name: {name}
Article Url: {url}
Number of Words: {words}
Number of Claps: {claps}
        
{text}""")


if __name__ == "__main__":

    MediumScraper.scrape(MediumScraper, sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
