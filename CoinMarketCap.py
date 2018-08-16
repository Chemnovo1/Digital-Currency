from cryptocmd import CmcScraper

scraper = CmcScraper('bch','01-01-2012','14-08-2018')
scraper.export_csv('bchusd.csv')