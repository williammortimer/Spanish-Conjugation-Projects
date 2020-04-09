import requests
import json
from bs4 import BeautifulSoup
from bs4 import Tag


base_url = 'https://www.spanishdict.com/conjugate/'
verb = 'correr'


def generateURL(infinitive: str) -> str :
    return base_url+infinitive

def createSoup(url: str) -> BeautifulSoup :
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def define(site: BeautifulSoup, infinitive: str) -> str :
    definition_container = site.find('div', id='quickdef1-es')
    return definition_container.get_text()




def main():
    page_url = generateURL(infinitive=verb)
    verb_soup = createSoup(url=page_url)

    verb_definition = define(site=verb_soup, infinitive=verb)

    conjugations = verb_soup.find('div', id='conjugation-content-wrapper').next_element.find_all('div', recursive=False)

    for conjugation in conjugations:
        verb_json = {
            'infinitive': verb,
            'definition': verb_definition
        }

        has_class = False
        class_name = []
        if(conjugation.get('class')):
            has_class = True
            class_name = conjugation.get('class')

        if(has_class and class_name==['_1XBD5ylq', '_3E987rfM']):
            form = conjugation.find('a').get_text()
            conjugated_form = conjugation.find('a', ['_1btShz4h _388srgc_']).get_text()
            print(form + conjugated_form)
        elif(not has_class):
            form = conjugation.find('span').get_text()

            table = conjugation.find('table', 'veSogiba')
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if(cells[0].get_text()==''):
                    print("empty cell for tense row")
                else:
                    print('perspective = ' + cells[0].get_text())
                for cell in cells:
                    print(cell.get_text())
        else:
            pass





if __name__ == "__main__":
    main()
