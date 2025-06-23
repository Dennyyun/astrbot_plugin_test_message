import requests
from lxml import etree
from fake_useragent import UserAgent
import random
from requests.adapters import HTTPAdapter
import time


""" https://s.taobao.com/search?_input_charset=utf-8&commend=all&ie=utf8&initiative_id=tbindexz_20170306&page=1&preLoadOrigin=https%3A%2F%2Fwww.taobao.com&q=%E6%B0%B4%E6%9E%9C&search_type=item&source=suggest&sourceId=tb.index&spm=a21bo.jianhua%2Fa.search_history.d1&ssid=s5-e&suggest_query=&tab=all&wq= """

class TaobaoSearch:
    def __init__(self, data: str):
        self.data = data
               
        
    def create_session():
        """创建带重试机制的会话"""
        session = requests.Session()

        # 重试策略
        retry_strategy = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session
        

    def get_random_headers():
        """生成随机请求头"""
        ua = UserAgent()
        return {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-CA;q=0.7,zh-CA;q=0.6,zh-HK;q=0.5',
            'cache-control': 'no-cache',
            'user-agent': ua.random,
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'Cookie':'thw=ir; arms_uid=6af33550-d33b-45bd-93a7-1bc32c98d873; tracknick=tb464070120549; ariaDefaultTheme=default; ariaFixed=true; ariaReadtype=1; ariaoldFixedStatus=false; ariaMousemode=null; ariaStatus=false; miid=6973189615420292568; t=e89056bc1316d45b88ecb8b96984b90b; lgc=tb464070120549; dnk=dennydetb; wk_cookie2=15cc6ed9714da77e73a3fe00811c36d1; wk_unb=UUpgRS98gQ0tgaj0lA%3D%3D; aui=2213788699324; havana_lgc2_0=eyJoaWQiOjIyMTM3ODg2OTkzMjQsInNnIjoiNjlmOTAwYzhhYmI2YTU5NTUyNWNhMDk1NzJkZTU4ZDEiLCJzaXRlIjowLCJ0b2tlbiI6IjFiRFdWT2F6ajJoYnNpZXVxX1dCdi1RIn0; _hvn_lgc_=0; xlly_s=1; cookie3_bak=284c0549ecb1885485257c6599c8acec; cookie3_bak_exp=1750922977508; env_bak=FM%2BgzJsXjwfMgFZVAJl2UrZRzKW8SOP8zXR3WY5RpuyB; cna=29aAHbmZ5zICAXjkTpjbiigB; cookie2=22554d2d4e44a94490ca072cc65890ec; _tb_token_=ef5ee4d73ebee; mtop_partitioned_detect=1; _m_h5_tk=3a19f8c7e6c1ba1eec69eef88f5b09f0_1750682403362; _m_h5_tk_enc=a1ffcbb641d0e30605a2b4194cd1137e; _samesite_flag_=true; 3PcFlag=1750674484119; unb=2213788699324; cancelledSubSites=empty; cookie17=UUpgRS98gQ0tgaj0lA%3D%3D; _l_g_=Ug%3D%3D; sg=944; _nk_=tb464070120549; cookie1=W80gVhlevQV%2BRdVSuy37ZHVAEJr3P1iEDfAd4y%2BBIPM%3D; sdkSilent=1750760884553; havana_sdkSilent=1750760884553; sgcookie=E100d%2FFFQTDQIQqCLF6qD4q6eoTDN3u9Bw7PLPN5z8yy2cCjhGTdGQ%2B78TvMv%2FRSrC5Dpbd3UVVu60WUFV1gw%2FUj1AJiDBHYvjpdTRZt7Ze4C9U%3D; csg=2616e96c; existShop=MTc1MDY3NDQ4OA%3D%3D; havana_lgc_exp=1781778488208; uc1=existShop=false&cookie15=UtASsssmOIJ0bQ%3D%3D&pas=0&cookie21=V32FPkk%2FgPzW&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie14=UoYby3LsdAXUHQ%3D%3D; uc3=lg2=W5iHLLyFOGW7aA%3D%3D&vt3=F8dD2fzWfY917INHiwA%3D&id2=UUpgRS98gQ0tgaj0lA%3D%3D&nk2=F5RBw5YzzuPFaZ6xfwc%3D; skt=d30b121f08ca3dd1; uc4=nk4=0%40FY4KpmwstFJtQFdxU7H1IS2HHz9vKv3J7g%3D%3D&id4=0%40U2gqykeSPoNpUa%2FB0H6ExrJC909AomiO; _cc_=URm48syIZQ%3D%3D; sca=653821dc; JSESSIONID=DEA0358E1E61F0578D4EE327DB3E7024; tfstk=gMkiQ2XZCfP_-WLL9vw6aB8_XMdpKRwb1qBYk-U2TyzCBSzv1qVmk2NqBRnt-ru-ooHtHxcCn0ijBhwvfRi_h-8JyLHmfcwjx5E6RA2EYoEWHZWw9J8OY-vpyLp-fCr_HD8-H1wUNyrR3-Pag6rURobN7Su4T9rb8OrVQo7exyaF3orNQwzUquzVgqy2xDzQ0-rZuS-nYb8M_PMqLv8pEcwGgfpjylVgzczZXcMFgS1sXycs6vqixzoNGtWqKlVZh_umS2Ptg0NSBmvcdRnoTJrmh350o7cqBJkw8LPQgvuUYVKAGkcm0Yw_1i6jrR00aAPh0twa3fw3YY-ANyH3WqkgT3BuMJk8aRlpOFFYIu0qCVjc34oK2ANInUbUlfE7LoDX4s40ggWFT_o_gtZeDv5fG5rQxzeevfH35oyNGHxhanNaAlaJxHffG5rQxzKHx_-b_kZ_y; isg=BIqKQO2o1pwBrVepydTDLFCh23Asew7VsU37ExTGX11oxyiB_Qin5Ydx1zMbN4Zt'
        }
    
    def search(self):
        """搜索淘宝商品"""
        data = self.data
        
        session = self.create_session()
        url = f"https://s.taobao.com/search?_input_charset=utf-8&commend=all&ie=utf8&initiative_id=tbindexz_20170306&page=1&preLoadOrigin=https%3A%2F%2Fwww.taobao.com&q={data}&search_type=item&source=suggest&sourceId=tb.index&spm=a21bo.jianhua/a.search_history.d1&ssid=s5-e&suggest_query=&tab=all&wq="
        response = session.get(url, headers=self.get_random_headers())
        
        if response.rise_for_status():
            time.sleep(1.5)
            return response.text
        else:
            return None

    def parse(self, html: str):
        """解析淘宝商品信息"""
        tree = etree.HTML(html)
        tree.xpath('//li[@data-spm="_sale"]/div').click() # 点击销量
        items = tree.xpath('//div[@id="content_items_wrapper"]/div') # 获取商品列表
        results = []
        for item in items:
            title = item.xpath('.//div[@class="title--qJ7Xg_90 "]')[0]
            price = item.xpath('.//div[@class="innerPriceWrapper--aAJhHXD4"]').get_text(strip=True).replace(' ','')
            results.append({'title': title, 'price': price})
        return results
    
    
    
def main(data):
    searcher = TaobaoSearch(data)
    html = searcher.search()
    if html:
        results = searcher.parse(html)
        return results
    else:
        return "搜索失败或无结果。"