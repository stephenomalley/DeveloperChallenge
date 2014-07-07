__author__ = 'Stephen'

from bs4 import BeautifulSoup
from urllib2 import urlopen
from categories import TypeCategory, TagCategory, Category
from itertools import count
from maths import StatisticMaths as StatPack

import re


class Scraper(object):

    def __init__(self, max_pages):
        self.max_pages = max_pages
        self.tag_categories = []
        self.type_categories = []
        self.stat_categories = []

        for tag in TagCategory.tags:
            category = TagCategory(tag)
            self.tag_categories.append(category)

        for m_type in TypeCategory.most_type:
            category = TypeCategory(m_type)
            self.type_categories.append(category)

        self.scrape()

    def make_soup(self, url):
        html = urlopen(url).read()
        soup = BeautifulSoup(html)
        return soup

    def get_tag_summary_count(self):
        results = []
        for category in self.tag_categories:
            soup = self.make_soup(category.url)
            summary_counts = [div.string.strip() for div in soup.findAll("div", "summarycount al")]
            for row in summary_counts:
                category.numberOf = row

            results.append(category)
        return results

    def get_most_type_data(self):
        results = []
        for category in self.type_categories:
            soup = self.make_soup(category.url)

            category.views = self.get_type_views(soup)
            category.title = self.get_type_title(soup)
            category.associated_tags = self.get_type_tags(soup)

            results.append(category)
        return results

    def get_type_views(self, soup):
        views = [div.text for div in soup.findAll("div", {'class': 'views supernova'}, limit=1)]
        if not views:
            views = [div.text for div in soup.findAll("div", {'class': 'views'}, limit=1)]
        return views[0]

    def get_type_title(self, soup):
        titles = [a.string for a in soup.findAll("a", {'class': 'question-hyperlink'}, limit=1)]
        if titles:
            return titles[0]

    def get_type_tags(self, soup):
        main_div = soup.findAll("div", {'class': 'tags'}, limit=1)
        if main_div:
            soup = BeautifulSoup(str(main_div))
            main_div = [a.string for a in soup.findAll("a", {'class': 'post-tag'})]
            tag = ""

            for tags in main_div:
                tag += tags+", "

            return tag[:-2]

    def get_averages_per_question(self):
        category = Category(Category.BASE_URL)
        views = []
        votes = []
        for page_num in count(1):
            soup = self.make_soup(category.url+'?page='+str(page_num)+'&sort=votes')

            string_results = self.parse_for_title(soup.findAll('div', {'class': 'views supernova'}))
            view_results = self.parse_results_for_digits(string_results)

            vote_results = self.parse_results_for_digits(
                [span.text for span in soup.findAll("span", {'class': 'vote-count-post'})])

            views += view_results
            votes += vote_results

            if page_num == self.max_pages:
                break

        category.views = views
        category.votes = votes
        category.samples = len(views)
        return category

    def parse_for_title(self, values):
        counts = []
        for items in values:
            counts.append(items['title'])
        return counts

    def parse_results_for_digits(self, view_array):
        view_as_digit = []
        for views in view_array:
            digit_only = re.sub("[^0-9]", "", views)
            view_as_digit.append(int(digit_only))
        return view_as_digit

    def scrape(self):

        self.tag_categories = self.get_tag_summary_count()
        self.type_categories = self.get_most_type_data()
        self.stat_categories = self.get_statistics()

    def get_statistics(self):
        maths_pack = StatPack()

        statistic_cat = self.get_averages_per_question()
        mean_votes = maths_pack.calculate_mean(statistic_cat.votes)
        med_view = maths_pack.calculate_median(statistic_cat.views)

        return {'samples': statistic_cat.samples,
                'mean_of_votes': maths_pack.bankers_round(mean_votes),
                'median_of_views': maths_pack.bankers_round(med_view),
                'python_comp_2': Scraper.do_compare(self.tag_categories, 'Python', 'Python-2.7'),
                'python_comp_3': Scraper.do_compare(self.tag_categories, 'Python', 'Python-3.x')}

    @staticmethod
    def find_category(category_list, search_field):
        for category in category_list:
            if category.tag == search_field:
                return category

    @staticmethod
    def do_compare(category_list, tag_a, tag_b):
        maths_pack = StatPack()

        cat_a = Scraper.find_category(category_list, tag_a)
        cat_b = Scraper.find_category(category_list, tag_b)

        perc = 100*(float(re.sub(",", "", cat_b.numberOf))/float(re.sub(",", "", cat_a.numberOf)))

        return maths_pack.bankers_round(perc)