import unittest
import requests
from bs4 import BeautifulSoup
from model import Scrape


class TestScrape(unittest.TestCase):
	# ---------------------------------------------------------------------
	# Some basic configuration:
	# ---------------------------------------------------------------------
	def setUp(self):
		# ---------------------------------------------------------------------
		# Set up seed url:
		# ---------------------------------------------------------------------
		self.seedUrl = 'http://hiring-tests.s3-website-eu-west-1.amazonaws'\
		'.com/2015_Developer_Scrape/5_products.html'
		# ---------------------------------------------------------------------
		# Set up a product url
		# ---------------------------------------------------------------------
		self.productUrl = 'http://hiring-tests.s3-website-eu-west-1.amazonaws.com'\
		'/2015_Developer_Scrape/sainsburys-golden-kiwi--taste-the-difference-x4-685641-p-44.html'
		# ---------------------------------------------------------------------
		# Configure the main program object class:
		# ---------------------------------------------------------------------
		self.scrapeObj = Scrape()
		# ---------------------------------------------------------------------
		# set up some simple mock html scraped from the website:
		# ---------------------------------------------------------------------
		self.htmlProducts = BeautifulSoup('<div class='\
			'"productTitleDescriptionContainer"><h1>Sainsbury\'s Avocados Ripe'\
			' & Ready x4</h1></div><div class="pricing"><p class='\
			'"pricePerUnit">&pound;3.20</p></div><div class="productText">'\
			'<p>Avocados</p></div><div class="productTitleDescriptionContainer"><h1>'\
			'Sainsbury\'s Golden Kiwi x4</h1></div><div class="pricing"><p class='\
			'"pricePerUnit">&pound;1.80</p></div><div class ="productText">'\
			'<p>Gold Kiwi</p></div>', 'lxml')

		self.htmlMain = BeautifulSoup('<div class="productInfo"><a' \
			' href="http://hiring-tests.s3-website-eu-west-1.amazonaws.com/' \
			'2015_Developer_Scrape/sainsburys-apricot-ripe---ready-320g.html"' \
			'>Sainsbury\'s Apricot Ripe &amp; Ready x5</a>' \
			'<div class="productTitleDescriptionContainer"><h1>Sainsbury\'s' \
			' Apricot Ripe & Ready x5</h1></div><p class="pricePerUnit">' \
			'&pound;3.50<span class="pricePerUnitUnit">unit</span></p>' \
			'<div class="productText">Apricots</div></div>' \
			'<div class="productInfo"><a ' \
			'href="http://hiring-tests.s3-website-eu-west-1.amazonaws.com/' \
			'2015_Developer_Scrape/sainsburys-avocado-xl-pinkerton-loose-' \
			'300g.html">Sainsbury\'s Avocado Ripe &amp; Ready XL Loose 300g' \
			'</a><div class="productTitleDescriptionContainer"><h1>' \
			'Sainsbury\'s Avocado Ripe & Ready XL Loose 300g</h1></div>' \
			'<p class="pricePerUnit">&pound;1.50<span class="pricePerUnitUnit"'\
			'>unit</span></p><div class="productText">Avocados</div></div>'\
			'<div class="productInfo"><a ' \
			'href="http://hiring-tests.s3-website-eu-west-1.amazonaws.com/' \
			'2015_Developer_Scrape/sainsburys-conference-pears--ripe---ready-x4-'\
			'\28\minimum\%\29.html">'\
			'Sainsbury\'s Conference Pears, Ripe &amp; Ready x4 (minimum)'\
			'</a><div class="productTitleDescriptionContainer"><h1>'\
			'Sainsbury\'s Conference Pears, Ripe & Ready x4 (minimum)</h1></div>'\
			'<p class="pricePerUnit">&pound;1.50<span class="pricePerUnitUnit"'\
			'>unit</span></p><div class="productText">Conference</div></div>', 'lxml')
	# ---------------------------------------------------------------------
	# Test some Http requests to make sure objects 
	# are being successfully matched using regular
	# equivalence methods:
	# ---------------------------------------------------------------------
	def test_getRequest(self):
		# ----------------------------------------
		# Test a request for main seed url:
		# ----------------------------------------
		# Have to use requests over model internal
		# use of urllib2 as it "causes any 
		# response with a response code outside the 
		# 2xx range to be handled as an error. 
		# The 3xx status codes then are handled by 
		# the HTTPRedirectHandler object, and 
		# some of the 40x codes 
		# (related to authentication) are handled
		# by specialised authentication handlers, 
		# but most codes simply are left to be 
		# raised as an exception".
		# After some research, it's been noted
		# to use request module instead of urllib2
		# in unit testing environments for simple
		# use cases.
		response_seed = requests.get(self.seedUrl)

		#requests.get(url)
		assert response_seed is not None
		self.assertEqual(response_seed.status_code, 200)
		self.assertEqual(response_seed.url, self.seedUrl)

		# ----------------------------------------
		# Returns response object
		# ----------------------------------------

	def test_getProdUri(self):
		# ----------------------------------------
		# Test to see if we can at least find two 
		# or more product link uri(s) within the 
		# mock html. 
		# ----------------------------------------

		# Set up mock htmlProducts via bs4
		def beautifulSoup_html(argv1, argv2):
			return self.htmlMain # return html object

		# Import main program: 
		import model

		# Now return the html object method and 
		# check for any found products via bs4. 
		# Should find at least one or more products
		# and their <a> @Uri types.
		model.BeautifulSoup = beautifulSoup_html
		productUri = self.scrapeObj.getProdUri(self.seedUrl)
		self.assertEqual(len(productUri), 3) # at least  <= 3 product links


	def test_getProdAttr(self):
		# ---------------------------------------
		# Test to see if we can scrape some
		# products html attributes. For example,
		# there should be a product description,
		# title and unit price displayed via 
		# html elements within the single layer.
		# Bs4 then does its magic scrape.
		
		# Set up mock html for single product:
		def beautifulSoup_html(argv1, argv2):
			return self.htmlProducts # return html object

		# Import main program:
		import model
		# Now return the mock html object method.
		# Execute some simple regular equivilance
		# upon the data in our json. We hope to find
		# the elements we have listed below in the 
		# parsed bs4 mock html object.
		model.BeautifulSoup = beautifulSoup_html
		self.scrapeObj.getProdAttr(self.productUrl)
		json_obj = self.scrapeObj.json_obj
		self.assertEqual(len(json_obj), 2)
		self.assertEqual(json_obj.get('total'), 3.2)
		self.assertEqual(json_obj['result'][0].get('description'), 'Avocados')
		self.assertEqual(json_obj['result'][0].get('unit_price'), 3.2)
		self.assertEqual(json_obj['result'][0].get('title'), 'Sainsbury\'s' \
			' Avocados Ripe & Ready x4')
