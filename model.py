import re
import json
from bs4 import BeautifulSoup
import urllib2

# ------------------------------------------------------------------------------
# The main Class 
# ------------------------------------------------------------------------------
class Scrape:
    # --------------------------------------------------------------------------
    # SET "init(ial)" state to objects/instances, for self 
    # arguments that are to be used throughout the program.
    # Parameters: Self -> self.json_obj & self.product_attr
    # --------------------------------------------------------------------------
    def __init__(self):
        # To begin with, this creates an object and array to 
        # store final exported content. Object is the exported
        # list of products + total as json format. Array is the
        # product attributes fetched from the crawling.
        self.product_attr = []
        self.json_obj = {}

    # --------------------------------------------------------------------------
    # GET Request Object
    # --------------------------------------------------------------------------
    def getRequest(self, url):
        # Now a method to fetch webpage request 
        # and return the request as an object.
        # -------------------------
        # Parameters: @self, @url
        # -------------------------
        # Output: @response
        # -------------------------
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-Agent', 'Mozilla/ 5.0')]
            # Open url as either a string / Request Obj
            response = opener.open(url)

        except urllib2.HTTPError, e:
            print('''An error occurred: {}
			The response code was {}'''.format(e, e.getcode()))

        return response  # The Request object

    # --------------------------------------------------------------------------
    # Return list of found urls from Request object 
    # 'response'. Find links on the html single layer.
    # --------------------------------------------------------------------------
    def getProdUri(self, uri):
        # Take the response Object, initiate the response.
        # From response, if there is one, begin a simple 
        # parse of single layer html for the @uri parameter.
        # -------------------------
        # Parameters: @uri, [uris]
        # Input: @uri (string of urls)
        # Output: [uris]
        # -------------------------

        # Take uri which started off as 'seed'
        response = self.getRequest(uri)
        # Make sure we get a friendly welcoming response
        if response.getcode() == 200 or response.getcode() == 302:
            html = response.read()
            soup = BeautifulSoup(html, 'lxml')
            productLinks = soup.select('.productInfo a')
            productLinks = [x.get("href") for x in productLinks]
            print '-' * 50
            print 'Found', len(productLinks), 'Product Links'
            print '-' * 50

        return productLinks

    # --------------------------------------------------------------------------
    # Method to extract data from each product hyperlink 
    # found in @getProdUri and create the json_obj we 
    # defined within _init_.
    # --------------------------------------------------------------------------
    def getProdAttr(self, uri):
        # -------------------------
        # Parameters: @uri
        # Input: @uri(s)
        # Output: @json_obj
        # -------------------------

        # Create new response for @uri
        response = self.getRequest(uri)
        html = response.read()
        soup = BeautifulSoup(html, 'lxml')

        # Title
        title = soup.select('.productTitleDescriptionContainer > h1')[0].text.strip()
        print 'Found the following Product Title:', title

        # Unit Price
        up = soup.select('.pricePerUnit')[0].text
        unit_price = float(re.findall('\d+\.\d+', up)[0])
        print 'Found the following Product Unit Price:', unit_price

        # Description
        desc = soup.select('.productText')[0].text.strip()
        print 'Found the following Product Description:', desc

        # Size
        bytes = float(response.headers['content-length'])
        size = '{:.2f}kb'.format(bytes / 1024)
        print 'Found the following Product Uri Size in kb:', size

        # create json_obj from earlier
        self.product_attr.append({
            "title": str(title),
            "unit_price": unit_price,
            "size": size,
            "description": str(desc)
        })
        # print self.product_attr
        self.json_obj["result"] = self.product_attr
        self.json_obj["total"] = unit_price + self.json_obj.get("total", 0)

    # --------------------------------------------------------------------------
    # RETRIEVE data from object of matched urls [] and
    # then traverse through the links, directly calling 
    # the method to extract product information per product.
    # --------------------------------------------------------------------------
    def retrieveData(self, seed):
        # -------------------------
        # Parameters: @seed
        # Input: @seed
        # Output: @json_obj (with product details now intact)
        # -------------------------
        # Method used to crawl page incrementally
        # and return product attribute information per
        # product. For example, extract product links,
        # then for each product link, extract product
        # attribute data!
        productLinks = self.getProdUri(seed)
        if len(productLinks) < 1:
            print 'What?! Are you kidding? Why no Product Links have been found?'
        else:
            for uri in productLinks:
                self.getProdAttr(uri)  # go fetch product information per product
        # We just round the total float to 3 decimal  places...
        self.json_obj["total"] = round(self.json_obj.get("total", 0), 3)
        
        # Finally, return our newly appended json_obj 
        # with the fancy new total.
        print '-' * 50
        print 'Print Json Data:'
        print '-' * 50
        
        return self.json_obj
       
# ------------------------------------------------------------------------------
# Initiate Class and begin callback for Class 
# definitions. After callbacks have successfully 
# executed, return Json format and save to disk.
# ------------------------------------------------------------------------------
def main():
    # Root URL to parse html.
    seed = 'http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/5_products.html'
    # Begin some confirmation before crawling:
    print '-' * 50
    confirmation = str(raw_input("Confirm that you would like to crawl the following domain: " + seed + " (y/n): ")).lower().strip()

    if confirmation == 'y':

        # Begin to initiate the main program class.
        scrapeObj = Scrape()
        productJson = scrapeObj.retrieveData(seed)
        print json.dumps(productJson, indent=4, sort_keys=True)

    if confirmation == 'n':
        print 'Exiting Program!'
        exit()

if __name__ == '__main__':
    main()
