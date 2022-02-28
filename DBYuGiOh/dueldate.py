import requests
import bs4

from Cardreq import cardSelect
from Cardreq import cardSelect2
from Cardreq import cardSearch

selectClass=[
    ".box_card_name",
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
    '.box_card_text',
    '.link_value'
]

def reqtest(Name,No,Cno):
    # url =   "https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&keyword=XXNAMEXX&stype=1&ctype=&starfr=&starto=&pscalefr=&pscaleto=&linkmarkerfr=&linkmarkerto=&link_m=2&atkfr=&atkto=&deffr=&defto=&othercon=2"
    # 通常魔法、通常罠
    # url =    https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&page=XXPAGEXX&keyword=XXNAMEXX&stype=1&ctype=XXCTYPEXX&effe=20&starfr=&starto=&pscalefr=&pscaleto=&linkmarkerfr=&linkmarkerto=&link_m=2&atkfr=&atkto=&deffr=&defto=&othercon=2
    # 永続魔法、速攻魔法、儀式魔法、永続魔法、フィールド魔法
    # url =    https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&page=XXPAGEXX&keyword=XXNAMEXX&stype=1&ctype=XXCTYPEXX&effe=23&effe=22&effe=25&effe=26&effe=24&starfr=&starto=&pscalefr=&pscaleto=&linkmarkerfr=&linkmarkerto=&link_m=2&atkfr=&atkto=&deffr=&defto=&othercon=2
    # 永続罠、カウンター罠
    # url =    https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&page=XXPAGEXX&keyword=XXNAMEXX&stype=1&ctype=XXCTYPEXX&effe=24&effe=21&starfr=&starto=&pscalefr=&pscaleto=&linkmarkerfr=&linkmarkerto=&link_m=2&atkfr=&atkto=&deffr=&defto=&othercon=2
    pageUrl = "https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&page=XXPAGEXX&keyword=XXNAMEXX&stype=1&ctype=XXCTYPEXX&starfr=&starto=&pscalefr=&pscaleto=&linkmarkerfr=&linkmarkerto=&link_m=2&atkfr=&atkto=&deffr=&defto=&othercon=2"
    
    if Cno==2 or Cno==3:
        pageUrl = "https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&page=XXPAGEXX&keyword=XXNAMEXX&stype=1&ctype=XXCTYPEXX&effe=20&starfr=&starto=&pscalefr=&pscaleto=&linkmarkerfr=&linkmarkerto=&link_m=2&atkfr=&atkto=&deffr=&defto=&othercon=2"
    elif Cno==4:
        pageUrl = "https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&page=XXPAGEXX&keyword=XXNAMEXX&stype=1&ctype=2&effe=23&effe=22&effe=25&effe=26&effe=24&starfr=&starto=&pscalefr=&pscaleto=&linkmarkerfr=&linkmarkerto=&link_m=2&atkfr=&atkto=&deffr=&defto=&othercon=2"
    elif Cno==5:
        pageUrl = "https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&page=XXPAGEXX&keyword=XXNAMEXX&stype=1&ctype=3&effe=24&effe=21&starfr=&starto=&pscalefr=&pscaleto=&linkmarkerfr=&linkmarkerto=&link_m=2&atkfr=&atkto=&deffr=&defto=&othercon=2"

    # requesturl = url.replace('XXNAMEXX',Name)
    # Name=Name.replace(' ','+')
    requesturl = pageUrl.replace('XXNAMEXX',Name)
    requesturl = requesturl.replace('XXPAGEXX',str(No))
    requesturl = requesturl.replace('XXCTYPEXX',str(Cno))

    # print(requesturl)

    #日本語指定
    headers = {'Accept-Language': 'ja'}

    if Name=="":
        return "名前が入力されていません"
    
    #リクエスト送信
    response = requests.get(requesturl,headers=headers)
    
    #通信エラーの場合は何もしない
    if response.status_code != 200:
        msg = 'カード検索失敗：通信エラー(' +str(response.status_code) + ')'
        return [msg]
    
    #レスポンス解析
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    #該当データ無しの場合は終了
    elems = soup.select('.no_data')
    for elem in elems:
        msg = '該当カードが見つかりません。'
        # print(msg)
        return msg

    #カード名取得
    elems = soup.select('.box_card_name span')

    textList=[]

    # print(len(elems))
    # print(elems)

    cs=cardSearch(elems,Name)

    if cs==21:
        # cs=cardSearch(elems,Name)
        return reqtest(Name,No+1,Cno)

    print("ページ番号")
    print(cs)
    #ヒットしたカード件数が5件以上の場合は終了
    if len(elems) > 20:
        textList.append('該当カードが5件超過のため表示できません')
        print(textList)
        return textList

    for s in selectClass:
        c=cardSelect2(soup,s,cs)
        # textList.append(c)
        if len(c)!=0:
            textList.append(c)

    # print(textList)
    # print("リスト数"+str(len(textList)))
    
    return textList

def reqmain():
    Name=input("reqtest Name ")
    # Cno=input("Card Type (1.monster, 2.magic, 3.trap)")
    # reqtest(Name,1,Cno)
    testans=""
    ans=""
    l=0
    for f in range(1,6):
        testans=reqtest(Name,1,f)
        if testans=="該当カードが見つかりません。":
            l+=1
        else:
            ans=testans
    if l==5:
        print("該当カードが見つかりません。")
    else:
        print(ans)
        return ans

if __name__ == "__main__":
    a=reqmain()
    print(a[-2])
