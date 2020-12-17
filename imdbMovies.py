from selenium import webdriver
from bs4 import BeautifulSoup as Soup
import re
import csv

driver = webdriver.Chrome(
    'D:/Google Drive/University/7 Sem/DW/Assignments/web scrapping/chromedriver_win32/chromedriver')
file = open('yearly movies.txt', 'r')
Lines = file.readlines()

with open('MovieDetails.csv', mode='w', newline='') as csvFile:
    fieldNames = ['Title', 'Rating', 'StoryLine', 'Genre', 'Stars', 'Directors', 'Budget', 'Gross', 'TagLine']
    csvWriter = csv.DictWriter(csvFile, fieldnames=fieldNames)
    csvWriter.writeheader()
    for line in Lines:
        # myUrl = "https://www.imdb.com/search/title/?title_type=feature&release_date=2015-01-01,2015-12-31&adult=include&sort=boxoffice_gross_us,desc"
        myUrl = line
        pageHTML = driver.get(myUrl)
        content = driver.page_source
        pageSoup = Soup(content, "html.parser")

        # getting movie titles
        movieItem = pageSoup.findAll("div", {"class": "lister-item-content"})
        for i in range(0, 50):
            movieUrl = 'https://www.imdb.com/' + movieItem[i].h3.a['href']
            subPageHTML = driver.get(movieUrl)

            # navigating to the movie pgae
            content = driver.page_source
            subPageSoup = Soup(content, "html.parser")

            # getting title
            if subPageSoup.find('div', attrs={'class': 'title_wrapper'}) is not None:
                movie = subPageSoup.find('div', attrs={'class': 'title_wrapper'})
                title = movie.h1.text.strip()
                print(title)

            # get rating
            if subPageSoup.find('div', attrs={'class': 'ratingValue'}) is not None:
                ratingHTML = subPageSoup.find('div', attrs={'class': 'ratingValue'})
                rating = ratingHTML.span.text
                print(rating)

            # get storyline
            if subPageSoup.find('div', attrs={'class': 'summary_text'}) is not None:
                storyHTML = subPageSoup.find('div', attrs={'class': 'summary_text'})
                storyLine = storyHTML.text.strip()
                print(storyLine)

            # get genre
            for item in subPageSoup.findAll('div', attrs={'class': 'see-more inline canwrap'}):
                if item.h4 == None:
                    break
                if item.h4.text == 'Genres:' or item.h4.text == 'Genre:':
                    genre = ''
                    for val in item.findAll('a'):
                        genre = genre + val.text + ','
                    print(genre)

            # get stars
            for item in subPageSoup.findAll('div', attrs={'class': 'credit_summary_item'}):
                if item.h4 == None:
                    break
                if item.h4.text == 'Stars:' or item.h4.text == 'Star:':
                    stars = ''
                    for val in item.findAll('a'):
                        if val.text == 'See full cast & crew':
                            break
                        stars = stars + ", " + val.text
                    stars = stars.strip()
                    print(stars)

            # get direction
            for item in subPageSoup.findAll('div', attrs={'class': 'credit_summary_item'}):
                if item.h4 == None:
                    break
                if item.h4.text == 'Directors:' or item.h4.text == 'Director:':
                    directors = ''
                    for val in item.findAll('a'):
                        directors = directors + ", " + val.text
                    directors = directors.strip()
                    print(directors)

            # get budget
            for item in subPageSoup.findAll('div', attrs={'class': 'txt-block'}):
                if item.h4 == None:
                    break
                if item.h4.text == 'Budget:':
                    text = item.text.strip()
                    result = re.search('Budget:(.*)', text)
                    amount = result.group(1)
                    budgetAmount = re.sub('[!@#$.,]', '', amount)
                    print(budgetAmount)

            # get gross
            for item in subPageSoup.findAll('div', attrs={'class': 'txt-block'}):
                if item.h4 == None:
                    break
                if item.h4.text == 'Cumulative Worldwide Gross:':
                    text = item.text.strip()
                    result = re.search('Cumulative Worldwide Gross:(.*)', text)
                    amount = result.group(1)
                    grossAmount = re.sub('[!@#$.,]', '', amount)
                    print(grossAmount)

            # get tagline
            for item in subPageSoup.findAll('div', attrs={'class': 'txt-block'}):
                if item.h4 == None:
                    break;
                if item.h4.text == 'Tagline:' or item.h4.text == 'Taglines:':
                    text = item.text.strip()
                    result = re.search('Taglines:\n(.*)', text)
                    tagline = result.group(1)
                    print(tagline)
            csvWriter.writerow(
                {'Title': title, 'Rating': rating, 'StoryLine': storyLine, 'Genre': genre, 'Stars': stars,
                 'Directors': directors, 'Budget': budgetAmount, 'Gross': grossAmount, 'TagLine': tagline})
    csvFile.close()
