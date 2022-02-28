from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
i=0
def cardSelect(soup,cardClass):
    textList=[]
    elems = soup.select(cardClass)
    for elem in elems:
        # if cardClass==".box_card_name span":
            # print(elem.get_text('\n').strip())
        if cardClass=='.card_info_species_and_other_item':
            elem=str(elem.get_text('\n').strip()).replace('\t',"")
            elem=str(elem).replace('\r',"")
            elem=str(elem).replace('\n',"")
            textList.append(elem)
        else:
            textList.append(elem.get_text('\n').strip())
    
    return textList

def cardSelect2(soup,cardClass,cs):
    global i
    textList=[]
    selectClass=[
        ".box_card_name span",
        ".box_card_name strong",
        '.box_card_attribute',
        '.box_card_level_rank',
        '.box_card_linkmarker',
        ".box_card_effect",
        '.card_info_species_and_other_item',
        '.atk_power',
        '.def_power',
        '.box_card_pen_scale',
        '.box_card_pen_effect',
        '.box_card_text'
    ]
    elems = soup.select(cardClass)
    j=0
    cs=(cs)/2
    cs=Decimal(str(cs)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    v=soup.find_all('input', {'class':'link_value'})
    # print("https://www.db.yugioh-card.com"+v['value'])
    # print(v[0]["value"])
    
    for elem in elems:
        j+=1
        if cardClass==selectClass[6] and cs==j:
            elem=str(elem.get_text('\n').strip()).replace('\t',"")
            elem=str(elem).replace('\r',"")
            elem=str(elem).replace('\n',"")
            textList.append(elem)
        else:
            # if cs-2==j and (cardClass!=selectClass[0] and cardClass!=selectClass[6]) or (cardClass==selectClass[0] and cs*2==j) or (cardClass==selectClass[6] and cs==j):
            tmp = elem.get_text('\n').strip()
            if tmp.find('\n') and cardClass!=selectClass[11]:
                tmp=tmp.split('\n')[0]
            if tmp.find('\u3000'):
                tmp=tmp.replace("\u3000"," ")
            if cardClass==".link_value" and cs==j:
                textList.append("https://www.db.yugioh-card.com"+v[j-1]["value"])
                d="\nQ&A\n"+"https://www.db.yugioh-card.com"+(v[j-1]["value"]).replace('card','faq')
                textList.append(d.replace('ope=2','ope=4'))
            elif cs==j and (cardClass!=selectClass[0] and cardClass!=selectClass[11] and cardClass!=selectClass[10]) or (cardClass==selectClass[0] and cs*2==j) or (cardClass==selectClass[11] and cs==j) or (cardClass==selectClass[10] and cs==j):
                if cardClass==selectClass[9] and len(tmp)!=0:
                    tmp="ペンデュラムスケール "+tmp
                textList.append(tmp)
                
    # print(selectClass)
    # print(elems)
    # print(len(elems))

    return textList

def cardSearch(elems,Name):
    j=0
    
    for elem in elems:
        el=elem.get_text('\n').strip()
        j+=1
        
        if str(el)==Name:
            print("完全一致")
            print(len(elems))
            return j
    return 21
    