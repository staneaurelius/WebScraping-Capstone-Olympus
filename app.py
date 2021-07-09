from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
def extract_page (output_list, row):
    row_length = len(row)

    for i in range(row_length):
        title = row[i].find('h3').find('a').text
        rating_div = row[i].find('div', attrs = {'class':'ratings-bar'})

        if rating_div == None:
            rating = 0
            metascore = 0

        else:
            rating = rating_div.find('strong')
            if rating == None:
                rating = 0
            else:
                rating = rating.text

            metascore = rating_div.find('span', attrs = {'class':'metascore'})
            if metascore == None:
                metascore = 0
            else:
                metascore = metascore.text.strip()

        votes = row[i].find('span', attrs = {'name' : 'nv'})
        if votes == None:
            votes = 0
        else:
            votes = votes.text

        output_list.append((title, rating, metascore, votes))

#insert the scrapping process here
temp = []
for i in range(1, 1000, 50):
    url_get = requests.get('https://www.imdb.com/search/title/?release_date=2021-01-01,2021-12-31&start=' + 
                           str(i) + '&ref_=adv_prv')

    soup = BeautifulSoup(url_get.content, "html.parser")
    row = soup.find_all('div', attrs = {'class':'lister-item mode-advanced'}) 
    extract_page (temp, row)

#change into dataframe
data = pd.DataFrame(temp, columns = ('title', 'imdb_rating', 'metascore', 'votes'))

#insert data wrangling here
data['imdb_rating'] = data['imdb_rating'].astype(float)
data['metascore'] = data['metascore'].astype(int)

data['votes'] = data['votes'].str.replace(',', '')
data.fillna(0, inplace = True)

data['votes'] = data['votes'].astype(int)
data = data.set_index('title')

data_top = data[['votes']].sort_values(by = 'votes', ascending = False)

#data wrangling for metascore tab
data_meta = data[['metascore', 'imdb_rating']].sort_values(by = 'metascore', ascending = False).copy()
data_meta['metascore'] = data_meta['metascore'] / 10

data_meta.rename(index = {'Summer of Soul (...Or, When the Revolution Could Not Be Televised)' : 
                          'Summer of Soul'}, inplace = True)

#end of data wranggling 

@app.route("/")
def index(): 
	
    card_data = f'{data["votes"].max()}' #be careful with the " and ' 
    card_data_2 = f'{data["metascore"].max()}'

	# generate plot
    ax = data_top.head(7).plot(kind = 'barh', color = '#b03610', figsize = (15,9))
    ax.invert_yaxis()
    ax.yaxis.label.set_visible(False)

	# Rendering plot for Votes
	# Do not change this
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True, bbox_inches='tight')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    plot_result = str(figdata_png)[2:-1]

    # plot (metascore)
    ax = data_meta.head(7).plot(kind = 'barh', color = ['#b03610', '#333333'], figsize = (15,9))
    ax.set_xticks(range(0, 14, 2), minor=False)
    ax.legend(loc = 'lower right')
    ax.yaxis.label.set_visible(False)
    ax.invert_yaxis()

    # Rendering plot for Metascore
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True, bbox_inches='tight')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    plot_result_meta = str(figdata_png)[2:-1]

	# render to html
    return render_template('index.html',
		card_data = card_data,
        card_data_2 = card_data_2, 
		plot_result=plot_result,
        plot_result_meta = plot_result_meta
		)


if __name__ == "__main__": 
    app.run(debug=True)