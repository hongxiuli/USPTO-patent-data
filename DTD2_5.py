from bs4 import BeautifulSoup
import os

def party_us(party):
    """process TAG <PARTY-US> to return name, city, state, postal code, and country
    
    @param party: the BeautifulSoup object representing the <PARTY-US> element 
    @return: a dictionary contains name, city, state, pcode, country
    """
    info = {
        'name':None,
        'city':None,
        'state':None,
        'pcode':None,
        'country':None
    }
    info['name'] = party.find('NAM').get_text(' ', strip=True)
    adr = party.find('ADR')
    if(adr is not None):
        #city
        city = adr.find('CITY')
        if(city is not None):
            info['city'] = city.get_text(' ', strip=True)
        #state
        state = adr.find('STATE')
        if(state is not None):
            info['state'] = state.get_text(' ', strip=True)
        #postal code
        pcode = adr.find('PCODE')
        if(pcode is not None):
            info['pcode'] = pcode.get_text('', strip=True)
        #country
        country = adr.find('CTRY')
        if(country is not None):
            info['country'] = country.get_text(' ', strip=True)
    return info

def processXMLDoc(content):
    """ process one XML document to extract patent number, title, abstract, inventor(s) and assignee(s) 
    NOTE: only non-design patterns are processed here
    
    @param content: the string representing one XML document 
    """
    bs = BeautifulSoup(content, 'xml')
    patnum = bs.B110.string
    
    #skip design patterns
    if(patnum.startswith('D')):
        print(patnum, 'design pattern')
        return
    
    title = bs.B540.string
    abst = bs.SDOAB.get_text(' ', strip=True)
    #inventor
    B721 = bs.find_all("B721")
    inventors = []
    for b721 in B721:
        info = party_us(b721.find('PARTY-US'))
        inventors.append(info)
    
    assignees = []
    B730 = bs.find_all('B730')
    for b730 in B730:
        #assignee 
        B731 = b730.find('B731')
        info = party_us(B731.find('PARTY-US'))
        #assignee type
        B732US = b730.find('B732US')
        info['assignee_type'] = B732US.get_text(' ', strip=True)
        assignees.append(info)
    
    #for now, just print the scraped information
    print(patnum, title, abst, inventors, assignees)
    
    #TODO: write patnum, title, abstract, inventor(s) and assignee(s) to persistent storage such as a csv file or a relational database 
    
def DTD2_5(filePath):
    """process each XML snippet in the file filePath
    
    @param filePath: the path of file to be processed 
    """
    content = ''
    with open(filePath) as f:
        for line in f:
            if(line.startswith('<?xml')):
                if(len(content)>0):
                    processXMLDoc(content)
                    content = ''
            content += line
                    
def processDTD2_5(folder):
    """process XML files inside folder
    NOTE: each XML file in the folder contains lots of XML snippets. Each XML snippet represent one patent.
    
    @param folder: the path to the folder to be processed 
    """
    for fileName in os.listdir(folder):
        if(fileName.endswith('.xml')):
            DTD2_5(folder+fileName)
            #break

processDTD2_5("D:\\patent\\pgb\\")