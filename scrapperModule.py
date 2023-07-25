from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(level=logging.DEBUG,filename="scrapper.log",format="%(levelname)s : %(filename)s : %(message)s : %(asctime)s")

class Website_scrapper():
    
    def search_result_scrapper(self,searchstring):
        try:
            searchstring=searchstring.replace(" ","")
            flipkart_url="https://www.flipkart.com/search?q="+ searchstring
            uclient=uReq(flipkart_url)
            flipkart_page=uclient.read()
            uclient.close()
            self.flipkart_html=bs(flipkart_page,"html.parser")
            logging.info("Generating url for product successfully")
            return self.flipkart_html
        except Exception as e:
            logging.error("Error generating url for product ",e)

class Product_Scrapper(Website_scrapper):
    def __init__(self,searchstring):
        self.searchstring=searchstring
    
    def individual_products(self):
        try:
            a=super().search_result_scrapper(self.searchstring)
            bigboxes = a.findAll("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            print(prod_html)
            self.commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})
            return self.commentboxes
        except Exception as e:
            logging.error("Error parsing",e)
            return "Error occurred during parsing"
    
    def savingComments(self):
        try:
            comm=self.individual_products()
            self.reviews = []
            for commentbox in comm:
                try:
                    
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text

                except:
                    name = 'No Name'

                try:
                    
                    rating = commentbox.div.div.div.div.text
                except:
                    rating = 'No Rating'

                try:
                    
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    
                    custComment = comtag[0].div.text
                except Exception as e:
                    logging.error("Exception while creating dictionary: ",e)

                self.mydict = {"Product": self.searchstring, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                self.reviews.append(self.mydict)
            return self.reviews
        except Exception as e:
            logging.error("Exception while creating dictionary: ",e)
            return "Some error occurred"
            