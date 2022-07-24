from crawl import LinkCrawl

from banner import banner


class Handler:

    @staticmethod
    def run():
        link = input(banner)
        aparat = LinkCrawl(link)
        qualities = aparat.get_all_qualities()
        for quality in qualities:
            print(f"\t - {quality}")
        quality = input("Enter The Quality of Video :")

        print(aparat.get_link(quality))


if __name__ == '__main__':
    Handler.run()
