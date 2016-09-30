# py-json-converter

## Installation

The following modules are required for the program to be succesfully executed:

- `re` (For regular expressions)
- `urllib2` (For url / request parsing)
- `json` (For pretty printing objects as json)
- `BeautifulSoup` (For html parsing)
- 'request' (For Unit Testing)
- ``unittest` (For Unit Testing)

Simply returning the following at the command line should install these for you:

```
> python setup.py

```

## Run Program

The following command should run the program:

```

> python model.py

```

## Program Architecture

The program follows a simple OOP architecture and the fundamental operations are called using a class mechanisim that adopts multiple methods through inheritence. 

The Base Class: `Scrape()` 

Class Methods: 

	- `retrieveData(self)`
	- `getProdAttr(self)`
	- `getProdUri(self)`
	- `getRequest(self)`

Global Objects: `json_obj`, `product_attr`

Each method communicates with eachother and recursively returns objects for each method to communicate and interact with.

## Testing

Some Unit Testing has been implemented and can be found within the `test_module.py` file.

### Installation

The following modules need to be installed on your system: 

- `unittest`
- `request`

## Run Tests

After installing both `unittest` and `request`, the testing program can be executed by returning the following command:

```
> python -m unittest test_model

```



# py-json-print
