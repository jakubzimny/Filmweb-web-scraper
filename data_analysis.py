#import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

class DatasetAnalyzer():

    def __init__(self, dataset):
        self.dataset = dataset

    def calculate_average_rating(self):
        ratings_sum = 0
        movies_number = 0
        for rating in self.dataset['ratings']:
            if rating != 'brak oceny':
                ratings_sum = ratings_sum + int(rating)
                movies_number += 1
        return ratings_sum/movies_number

    def get_category_names(self, category):
        category_names = [] #labels possible in dataset 
        for category in self.dataset[category]:
            if isinstance(category, str):
                category_list = category.split(",")
                category_list = [component.strip() for component in category_list]
                category_names.extend(category_list)
            else:
                category_names.extend(category)
        return category_names

    def get_category_occurences_counter(self, category):
        category_names = self.get_category_names(category)
        category_occurences = Counter(category_names)
        return category_occurences

    def get_category_occurences(self, category_names, category):
        category_occurences_counter = self.get_category_occurences_counter(category)
        category_occurences = [category_occurences_counter[name] for name in category_names]
        return category_occurences

    def plot_category(self,category, plot_type, title, color='blue'):
        category_names = sorted(set(self.get_category_names(category)))
        category_occurences = self.get_category_occurences(category_names, category)
        if plot_type == 'bar':
            self.bar_plot_category(category_names, category_occurences, color, title)
        elif plot_type == 'line':
            self.line_plot_category(category_names, category_occurences, color, title)
        elif plot_type == "pie":
            self.pie_chart_of_category(category_names, category_occurences, title)
        else: 
            print("Wrong plot type.")
        plt.savefig('plots/'+category+'_'+plot_type+'.png',bbox_inches = "tight")
        plt.gcf().clear()

    def bar_plot_category(self, names, occurences, color, title):
        plt.figure(figsize=(14,7))
        _, ax = plt.subplots(figsize=(14,7))    
        x = [i for i in range(1,len(names)+1)]
        ax.bar(x, occurences,  color=color, tick_label=names, edgecolor= 'k', linewidth=1)
        for i, v in enumerate(occurences):
            if v>=100:
                offset= 0.4
            elif v<100 and v >=10:
                offset = 0.6
            else:
                offset = 0.8
            ax.text(i+offset, v+3, str(v))
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.grid()
        plt.ylabel("Liczba filmów")
        plt.title(title)
    
    def line_plot_category(self, names, occurences, color, title):
        plt.figure(figsize=(14,7))
        plt.plot(names, occurences, color=color, marker ='x')
        plt.grid()
        plt.ylabel("Liczba filmów")
        plt.title(title)

    def pie_chart_of_category(self, names, occurences, title):
        plt.figure(figsize=(7,7))
        colors = ['yellowgreen','pink','gold','cyan','blue','darkgreen','lightskyblue','red','violet','magenta','yellow']
        percent = [100 * occurence/sum(occurences) for occurence in occurences]
        patches, _ = plt.pie(occurences, colors=colors, shadow=True, wedgeprops={"edgecolor":"k",'linewidth': 1})
        labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(names, percent)]
        plt.legend(patches, labels, loc='best')
        plt.title(title)

    def plot_date(self):
        #TODO
        return

#if __name__ == "__main__":
    #categories: countries, genres, ratings, year
    #dataset = pd.read_csv("./data/dataset.csv", sep=';')
    #analyzer = DatasetAnalyzer(dataset)
    # analyzer.plot_category('rating', 'pie', 'Oceny')
    # analyzer.plot_category('countries', 'bar', 'Kraje pochodzenia','#1a53af')
    # analyzer.plot_category('genres', 'bar', 'Gatunki', '#48bc0f',)
    # analyzer.plot_category('years', 'line', 'Lata produkcji', '#e85e14')
    
    #Wykres historii ocen