from src.Latip176.module import *
from src.Latip176.output import FinalOutput


# --> Class Response
class Response(object):
    def __init__(self, session=requests.Session()):
        self.__session = session  # --> self session: untuk menyimpan requests Session

    # --> Request ke web
    def __response(self, category=None, keyword=None) -> str:
        if category != None:
            return self._Response__session.get(
                "https://www.mangayaro.net/",
                headers={"UserAgent": "chrome"},
            )
        if keyword != None:
            return self._Response__session.get(
                f"https://www.mangayaro.net/?s={keyword}",
                headers={"UserAgent": "chrome"},
            )

    # --> Final Output
    def __setup(self, data_list: list, query: str) -> dict:
        priv_list = []
        if data_list != None:
            if query == "populer":
                for data in data_list:
                    url, bg_url, title, chapter, rating = data
                    priv_list.append(
                        {
                            "url": url,
                            "bg_url": bg_url,
                            "title": title,
                            "chapter": chapter,
                            "rating": rating,
                        }
                    )
            elif query == "terbaru" or query == "proyek":
                for data in data_list:
                    url, bg_url, title, update = data
                    priv_list.append(
                        {"url": url, "bg_url": bg_url, "title": title, "update": update}
                    )
            else:
                for data in data_list:
                    url, bg_url, title, chapter, rating, tipe = data
                    priv_list.append(
                        {
                            "url": url,
                            "bg_url": bg_url,
                            "title": title,
                            "chapter": chapter,
                            "rating": rating,
                            "tipe_komik": tipe,
                        }
                    )
            self._Response__data_dict.update(
                {
                    "results": [
                        {
                            "data": priv_list,
                            "msg": "Success",
                            "status_code": 200,
                            "jumlah_data": len(priv_list),
                        }
                    ],
                    "author": "Latip176",
                }
            )
            return self._Response__data_dict, 200
        else:
            return {
                "results": [
                    {
                        "data": None,
                        "msg": "Data Not Found",
                        "status_code": 200,
                        "jumlah_data": 0,
                    }
                ],
                "author": "Latip176",
            }


# --> Class Turunan dari Class Response
class WebScrapper(Response):
    def __init__(self, list=[], dict={}):
        super().__init__()
        self.__data_list = list  # --> self data list: untuk menampung data list

    def route(self, category: str = None, keyword: str = None) -> dict:
        self._WebScrapper__data_list.clear()
        if keyword == "debug":
            return jsonify(
                {
                    "debug_log": BeautifulSoup(
                        self._Response__response(category=category).text, "html.parser"
                    )
                }
            )
        if keyword != None or category != None:
            if category == "populer" or category == "terbaru" or category == "proyek":
                soup = BeautifulSoup(
                    self._Response__response(category=category).text, "html.parser"
                )  # --> BeautifulSoup
                if category == "populer":  # --> Jika Query memasukan "populer"
                    populer = self.populer_hari_ini(
                        soup
                    )  # --> Menuju ke Function populer_hari_ini
                    return FinalOutput().results(populer, "Success", 200)
                elif category == "proyek":  # --> Jika Query memasukan "proyek"
                    proyek = self.pembaruan_projek(
                        soup
                    )  # --> Menuju ke Function pembaruan_projek
                    return FinalOutput().results(proyek, "Success", 200)
                elif category == "terbaru":
                    terbaru = self.pembaruan_terbaru(
                        soup
                    )  # --> Menuju ke Function pembaruan_terbaru
                    return FinalOutput().results(terbaru, "Success", 200)
            else:
                soup = BeautifulSoup(
                    self._Response__response(keyword=keyword).text, "html.parser"
                )  # --> BeautifulSoup
                search = self.searchComic(soup)
                return FinalOutput().results(search, "Success", 200)
        else:
            return FinalOutput().results(None, "query is required!", 400)

    def populer_hari_ini(
        self, soup
    ) -> list:  # --> Function untuk Scraping data komik Populer Hari Ini
        content = (
            soup.find("div", attrs={"id": "content"})
            .find("div", attrs={"class": "listupd"})
            .findAll("div", attrs={"class": "bs"})
        )  # --> Find div yang berisikan data populer sesuai yang ada di websitenya
        for i in content:
            link = i.find("a", href=True)
            bigor, limit = link.find("div", attrs={"class": "bigor"}), link.find(
                "div", attrs={"class": "limit"}
            )
            url, bg_url, title, chapter, rating = [
                link.get("href"),
                limit.find("img").get("src"),
                " ".join(
                    re.findall(
                        "([a-zA-Z0-9]+)",
                        str(bigor.find("div", attrs={"class": "tt"}).string),
                    )
                ),
                re.findall(
                    "\d+", str(bigor.find("div", attrs={"class": "epxs"}).string)
                )[0],
                bigor.find("div", attrs={"class": "numscore"}).string,
            ]  # --> Scraping mengambil data: url, judul, jumlah chapter, rating. komik
            self._WebScrapper__data_list.append(
                {
                    "url": url,
                    "bg_url": bg_url,
                    "title": title,
                    "chapter": chapter,
                    "rating": rating,
                }
            )  # --> Menambahkan data hasil Scraping ke Self data list
        return self._WebScrapper__data_list  # --> mengembalikan nilai Self data list

    def pembaruan_projek(
        self, soup
    ) -> list:  # --> Function untuk Scraping data komik Pembaruan Projek
        content = (
            soup.find("div", attrs={"id": "content"})
            .find("div", attrs={"class": "postbody"})
            .findAll("div", attrs={"class": "bixbox"})[0]
            .findAll("div", attrs={"class": "utao"})
        )  # --> Find div yang berisikan data populer sesuai yang ada di websitenya
        for i in content:
            imgu, luf = i.find("div", attrs={"class": "imgu"}).find(
                "a", href=True
            ), i.find("div", attrs={"class": "luf"})

            url, bg_url, title, update = [
                imgu.get("href"),
                imgu.find("img").get("src"),
                " ".join(
                    re.findall(
                        "([a-zA-Z0-9]+)",
                        str(imgu.get("title")),
                    )
                ),
                [
                    {
                        str(i + 1): {
                            "chapter": x.find("a").string,
                            "time": x.find("span").string,
                        }
                        for i, x in enumerate(luf.find("ul").findAll("li"))
                    }
                ],
            ]
            self._WebScrapper__data_list.append(
                {"url": url, "bg_url": bg_url, "title": title, "update": update}
            )  # --> Menambahkan data hasil Scraping ke Self data list
        return self._WebScrapper__data_list  # --> mengembalikan nilai Self data list

    def pembaruan_terbaru(
        self, soup
    ) -> list:  # --> Function untuk Scraping data komik Pembaruan Projek
        content = (
            soup.find("div", attrs={"id": "content"})
            .find("div", attrs={"class": "postbody"})
            .findAll("div", attrs={"class": "bixbox"})[1]
            .findAll("div", attrs={"class": "utao"})
        )  # --> Find div yang berisikan data populer sesuai yang ada di websitenya
        for i in content:
            imgu, luf = i.find("div", attrs={"class": "imgu"}).find(
                "a", href=True
            ), i.find("div", attrs={"class": "luf"})

            url, bg_url, title, update = [
                imgu.get("href"),
                imgu.find("img").get("src"),
                " ".join(
                    re.findall(
                        "([a-zA-Z0-9]+)",
                        str(imgu.get("title")),
                    )
                ),
                [
                    {
                        str(i + 1): {
                            "chapter": x.find("a").string,
                            "time": x.find("span").string,
                        }
                        for i, x in enumerate(luf.find("ul").findAll("li"))
                    }
                ],
            ]
            self._WebScrapper__data_list.append(
                {"url": url, "bg_url": bg_url, "title": title, "update": update}
            )  # --> Menambahkan data hasil Scraping ke Self data list
        return self._WebScrapper__data_list  # --> mengembalikan nilai Self data list

    def searchComic(
        self, soup=None
    ):  # --> Function untuk Scraping data komik searching
        content = (
            soup.find("div", attrs={"id": "content"})
            .find("div", attrs={"class": "listupd"})
            .findAll("div", attrs={"class": "bs"})
        )
        try:
            pagination = soup.find("div", attrs={"class": "pagination"})
            page = pagination.find("a", attrs={"class": "next page-numbers"})
        except:
            pass
        for x in content:
            bigor, limit = x.find("div", attrs={"class": "bigor"}), x.find(
                "div", attrs={"class": "limit"}
            )
            href = x.find("a", href=True)
            data_list = (url, bg_url, title, chapter, rating, tipe) = [
                href.get("href"),
                limit.find("img", attrs={"src": True}).get("src"),
                " ".join(
                    re.findall(
                        "([a-zA-Z0-9]+)",
                        str(href.get("title")),
                    )
                ),
                bigor.find("div", attrs={"class": "epxs"}).string,
                bigor.find("div", attrs={"class": "numscore"}).string,
                "Warna"
                if limit.find("span", attrs={"class": "colored"})
                else "Tidak Berwarna",
            ]
            self._WebScrapper__data_list.append(
                {
                    "url": url,
                    "bg_url": bg_url,
                    "title": title,
                    "chapter": chapter,
                    "rating": rating,
                    "tipe_komik": tipe,
                }
            )  # --> Menambahkan data hasil Scraping ke Self data list
        # if page:
        #    self.searchComic(
        #        BeautifulSoup(requests.get(page.get("href")).text, "html.parser")
        #    )  # --> Menambahkan data hasil Scraping ke Self data list
        return self._WebScrapper__data_list  # --> mengembalikan nilai Self data list
