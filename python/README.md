# Web Spider Pyton

## Tools
- Selenium: easy_install selenium 
- PhantomJs: [http://phantomjs.org/download.html](http://phantomjs.org/download.html)
- Requests
- Beautiful Soup

## Logging Level
|Level		|	value	|
|CRITICAL	|	50		|
|ERROR		|	40		|
|WARNING	|	30		|
|INFO		|	20		|
|DEBUG		|	10		|
|NOTSET		|	0		|

# E-commerce overview

## Amazon


### Keywork Searching

#### Searching URL
1.From home page: https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=<keyword>
  e.g.:
    1.https://www.amazon.com/s/ref=nb_sb_noss_2/156-5197205-3842330?url=search-alias%3Daps&field-keywords=C%2B%2B+primer
    2.https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=iphone+7
2.From product page, same as from home page.

#### Html Elements
1.Searching results container is <ul> and id is 's-results-list-atf'.
2.Product item container is <li> and class is 's-item-container'.(But get this container as a 'WebElement' is not working, unsolved)
3.Product name and link's xpath: "./div/div/div/div/div/a"

### Product Details 

#### Sales
#### Comments


### Price Adjustment

