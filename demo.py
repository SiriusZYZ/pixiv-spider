import pixivSpider
import os
def main():
    
    rs = pixivSpider.rankingSession()
    rs.set_proxies(7890)
    rs.get_ranking_page()
    r1 = rs.resolve()
    for idx, item in enumerate(r1):
        print(idx+1, item)

    print("\n\n\n")

    ips = pixivSpider.illustPageSession()
    ips.set_proxies(7890)
    target_illust_id = r1[0]["illust_id"] 
    ips.get_illust_page(target_illust_id)
    for idx, item in enumerate(ips.resolve()):
        print(idx+1, item)



if __name__ == "__main__":
    main()