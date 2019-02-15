import requests
from bs4 import BeautifulSoup

def main():
    main_page()
    outage_events = event_link_extractor(outage_soup)
    disrupt_events = event_link_extractor(disruption_soup)
    print " "
    print("-"*72 )
    print("{} Recent OUTAGE EVENTS detected. Details as below : ".format(len(outage_events)))
    print("-"*72 )
    event_info_extractor(outage_events)
    print " "
    print("-"*77 )
    print("{} Recent DISRUPTION EVENTS detected. Details as below : ".format(len(disrupt_events)))
    print("-"*77 )
    event_info_extractor(disrupt_events)


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def get_html(url):
    r = requests.get(url)
    html = r.text
    return html


def event_link_extractor(event):
    i = 0
    url_list = []
    for inc in event:
        inc = event[i]
        inc_par = inc.findParent('a')
        par_lin = baseurl + inc_par.get('href')
        i += 1
        url_list.append(par_lin)
    inc_nums = []
    for inc_num in url_list:
        inc_num = int(inc_num[-5:])
        inc_nums.append(inc_num)
    gen_dict = dict(zip(inc_nums, url_list))
    s_url_list = []
    for url in (sorted(gen_dict)):
        url = gen_dict[url]
        s_url_list.append(url)
    s_url_list.reverse()
    return(s_url_list)

def event_info_extractor(s_url_list):
        for url in s_url_list:
            inc_html = get_html(url)
            inc_soup = BeautifulSoup(inc_html, 'lxml')
            service_name_soup = inc_soup.select(".service-name")
            print(service_name_soup[0].text + "- " + url + " :")
            service_summary_soup = inc_soup.select(".card.admin")
            service_summary = service_summary_soup[0].text.split()
            service_summary = " ".join(service_summary)
            print(service_summary)
            print " "

def main_page():
    global baseurl
    global outage_soup
    global disruption_soup
    global normal_soup
    baseurl = "https://status.firebase.google.com/"
    home_html = get_html(baseurl)
    main_soup = BeautifulSoup(home_html, 'lxml')
    outage_soup_sameday = main_soup.select(".high.only-today")
    outage_soup_extended = main_soup.select('.high.begins')
    outage_soup = outage_soup_extended + outage_soup_sameday
    disruption_soup_sameday = main_soup.select('.medium.only-today')
    disruption_soup_extended = main_soup.select('.medium.begins')
    disruption_soup = disruption_soup_extended + disruption_soup_sameday
    normal_soup = main_soup.select('.ok')
    del normal_soup[-1]

if __name__ == "__main__":
    main()
