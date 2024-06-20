import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from lxml import etree
isbn_url = 'https://drive.google.com/uc?export=download&id=1u4f-SSnZsgleZCK0533EC5VJauoFHjuM'
isbn_list = pd.read_csv(isbn_url, header=None)[0].tolist()
# Function to scrape book details from Booktopia
def scrape_book_details(isbn):
    # url = f'https://www.booktopia.com.au/search.ep?keywords={isbn}&productType=917504'
    url = f'https://www.booktopia.com.au/the-screwtape-letters-letters-from-a-senior-to-a-junior-devil-c-s-lewis/book/{isbn}.html'

    books_data1=[]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize book details dictionary
    book_details = {
        'ISBN': isbn,
        'Title': 'book not found',
        'Author': None,
        'Book type': None,
        'Original Price (RRP)': None,
        'Discounted price': None,
        'ISBN-10': None,
        'Published Date': None,
        'Publisher': None,
        'No. of Pages': None
    }

    try:

        if "Sorry, no search results found" in soup.text:
            return book_details

        dic_date = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8,
                    'September': 9, 'October': 10, 'November': 11, 'December': 12}

        # Scrape required details
        book_info = soup.find('div', {'class': 'MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-md-7 mui-style-1ak9ift'})
        book_info1 = soup.find('div', {'class': 'MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation0 mui-style-cier7i'})
        details_list = soup.find('div', {'class': 'MuiBox-root mui-style-h3npb'})
        try:
            book_details['Title'] = book_info.find('h1').text.strip()
        except:
            pass
        try:
            book_details['Author'] = book_info.find('span').text.strip()
        except:
            pass
        # data_type=book_info.find_all('p', {'class': 'MuiTypography-root MuiTypography-body1 mui-style-tgrox'})
        # book_details['Book type']=data_type[3].text.strip().split('|')[0]
        try:
            book_details['Book type'] = book_info1.find('h3', {'class': 'MuiTypography-root MuiTypography-h3 mui-style-lijwn'}).get_text(strip=True)
        except:
            pass
        try:
            book_details['Original Price (RRP)'] =book_info1.find('span', {'class': 'strike'}).get_text(strip=True)
        except:
            pass
        try:
            book_details['Discounted price'] =book_info1.find('p', {'class': 'MuiTypography-root MuiTypography-body1 BuyBox_sale-price__PWbkg mui-style-tgrox'}).get_text(strip=True)
        except:
            pass

        try:
            lst_details = details_list.find_all('p', {'MuiTypography-root MuiTypography-body1 mui-style-tgrox'})
            book_details['ISBN-10'] = lst_details[0].text.strip().split(':')[1]
            pub_date= lst_details[3].text.strip().split(':')[1]
        except:
            pass
        # try:
        #     # book_details['Publisher'] = lst_details[10].text.strip().split(':')[1]
        #     data_publisher_val = lst_details[10].text.strip().split(':')[1]
        # except:
        #     data_publisher_val=''
        # if data_publisher_val.strip()=='Digital original':
        #     try:
        #         data_publisher_val=lst_details[8].text.strip().split(':')[1]
        #     except:
        #         pass
        # if data_publisher_val.strip()=='':
        #     try:
        #         data_publisher_val=lst_details[7].text.strip().split(':')[1]
        #     except:
        #         pass
        #
        # try:
        #     book_details['Publisher']=data_publisher_val
        # except:
        #     pass
        data1=''
        try:
            # book_details['No. of Pages'] = lst_details[6].text.strip().split(':')[1]
            data1 = lst_details[6].text.strip().split(':')[1].strip()
        except:
            pass
        if not data1.isdigit():
            try:
                data1 = lst_details[6].text.strip().split(':')[1]
            except:
                pass
            if not data1.isdigit():
                data1=''

        try:
            book_details['No. of Pages']=data1
        except:
            pass
        try:

            publisher = pub_date.strip().split(' ')
            month = dic_date[publisher[1]]
            year = publisher[2]
            date = publisher[0].replace('st', '').replace('nd', '').replace('rd','').replace('th','')
            book_details['Published Date'] = year + '-' + str(month) + '-' + date
        except:
            book_details['Published Date'] = ''

        dom = etree.HTML(str(soup))

        # Step 4: Use XPath to extract data
        # For example, to extract the text from a specific <span> tag in a nested <div>
        # Title_xpath='//*[@id="ProductDetails_d-product-info__rehyy"]/div[3]/h1/text()'
        # title=dom.xpath(Title_xpath)
        # book_details['Title']=str(title)[1:-1]
        # author_xpath='//*[@id="ProductDetails_d-product-info__rehyy"]/div[3]/p[1]/a/span/text()'
        # author=dom.xpath(author_xpath)
        # book_details['Author']=str(author)[1:-1]
        # book_xpath='//*[@id="BuyBox_product-version__uw1et"]/h3/text()'
        # book_type=dom.xpath(book_xpath)
        # book_details['Book type']=str(book_type)[1:-1]
        # rrp_xpath='//*[@id="BuyBox_product-version__uw1et"]/div[1]/div/div/div/p/span/text()'
        # rrp=dom.xpath(rrp_xpath)
        # book_details['Original Price (RRP)']=str(rrp)[1:-1]
        # price_xpath='//*[@id="BuyBox_product-version__uw1et"]/div[1]/div/div/p/text()'
        # price_value=dom.xpath(price_xpath)
        # book_details['Discounted price']=str(price_value)[1:-1]
        #
        # isbn_xpath='//*[@id="pdp-tabpanel-details"]/div/p[2]/text()'
        # isbn_value=dom.xpath(isbn_xpath)
        #
        # book_details['ISBN-10']=str(isbn_value)[1:-1]
        # published_date_xpath='//*[@id="pdp-tabpanel-details"]/div/p[3]/text()'
        # published_date=dom.xpath(published_date_xpath)
        # book_details['Published Date']=str(published_date)[1:-1]
        # number_xpath='//*[@id="pdp-tabpanel-details"]/div/p[7]/text()'
        #
        # number_page = dom.xpath(number_xpath)
        #
        # book_details['No. of Pages'] = str(number_page)[1:-1]


        xpath_expression = '//*[@id="pdp-tabpanel-details"]/div/p[11]/text()|//*[@id="pdp-tabpanel-details"]/div/p[9]/text()'
        # xpath_expression = '//*[@id="pdp-tabpanel-details"]/div/p[9]/text()'
        extracted_text = dom.xpath(xpath_expression)
        if len(extracted_text)==0:
            xpath_publisher='//*[@id="pdp-tabpanel-details"]/div/p[8]/text()'
            extracted_text = dom.xpath(xpath_publisher)
        if len(extracted_text) == 0:
            extracted_text=''

        book_details['Publisher']=str(extracted_text)[1:-1]


        # print(extracted_text[1:-1])  # Output: ['Some nested text']





        books_data1.append(book_details)
        file_path='books_data.csv'
        file_exists = os.path.isfile(file_path)

        df = pd.DataFrame(books_data1)
        df.to_csv(file_path, mode='a', header=not file_exists, index=False)

        # df.to_csv('books_data.csv', mode='a',header=False,index=False)




            # details_list = soup.find_all('div', {'class': 'MuiBox-root mui-style-h3npb'})
            # for detail in details_list:
            #     text = detail.text
            #     if 'ISBN-10' in text:
            #         book_details['ISBN-10'] = text.split(':')[1].strip()
            #     elif 'Published' in text:
            #         book_details['Published Date'] = text.split(':')[1].strip()
            #     elif 'Publisher' in text:
            #         book_details['Publisher'] = text.split(':')[1].strip()
            #     elif 'Pages' in text:
            #         book_details['No. of Pages'] = text.split(':')[1].strip()

    except Exception as e:
        print(f"Error occurred for ISBN {isbn}: {e}")

    return book_details


for isbn in isbn_list[1:]:
    book_details = scrape_book_details(isbn)
    print(book_details)
    # books_data.append(book_details)

