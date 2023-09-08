############################################################
# File: createData.py
# Purpose: This script will import and clean the raw data
#          provided by JSTOR. This only needs to be run
#          when JSTOR provides an update to the dataset
#          and the customer wishes a larger dataset.
#          While cleaning, this script outputs a file
#          that effectively serves as the database for
#          all processes of the main program.
############################################################

import xml.etree.ElementTree as ET
import os
import csv
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from collections import Counter


class BookDatabase():

    #### Global variables
    bookMetaData = {} #main storage dictionary for book information (includes top 10 common words as well)
    stop_words = stopwords.words('english')
    stop_words.extend(['would', 'could', 'also', 'said', 'came'])
    bookTitles = []


    def acquireMetadata(self, file):

        bookInformation = []
        subjectList = []
        tree = ET.parse('./data/metadata/' + file)
        root = tree.getroot()

        for child in root:
            for secondchild in child:

                # Check to see if book is English--if not, do not add to database
                if secondchild.tag == 'custom-meta-group':
                    for customMetaChild in secondchild:
                        if customMetaChild.tag == 'custom-meta':
                            for customMetaGrandchild in customMetaChild:
                                if customMetaGrandchild.tag == 'meta-value':
                                    if customMetaGrandchild.text != 'eng':
                                        return

                if secondchild.tag == 'book-id':
                    bookInformation.append(secondchild.text) # add bookID
                elif secondchild.tag == 'subj-group':
                    for subjectchild in secondchild:
                        if subjectchild.tag == 'subject':
                            if subjectchild.text not in subjectList: #don't add duplicates
                                subjectList.append(subjectchild.text)
                elif secondchild.tag == 'book-title-group':
                    for booktitle in secondchild:
                        if booktitle.tag == 'book-title':
                            bookInformation.append(booktitle.text)
                        if booktitle.tag == 'subtitle':
                            bookInformation.append(booktitle.text)
                    if len(bookInformation) < 3:
                        bookInformation.append('No subtitle')
                elif secondchild.tag == 'pub-date':
                    for pubdate in secondchild:
                        if pubdate.tag == 'year':
                            bookInformation.append(int(pubdate.text))


        bookInformation.append(subjectList) # add the completed subject list (all duplicates already moved during the search process above)

        return bookInformation


    def mergenGramFiles(self, fileID, files_list):

        # Each book has separate files for each chapter; this function combines all chapters into one book

        with open ('data/ngram1/' + fileID + '.txt', 'w') as merged_file:
            for file in files_list:
                with open('data/ngram1/' + file) as opened_file:
                    data = opened_file.read()
                merged_file.write(data)

    def acquireWordFrequencies(self, fileID):
        #This function will return the top 10 most frequent words from the ngram collection for each book
        wordFrequencyDictionary = {}

        with open('data/ngram1/' + fileID + '.txt', newline = '') as words:
            word_reader = csv.reader(words, delimiter ='\t')
            for line in word_reader:
                if line[0] in self.stop_words: #skip stop words
                    continue
                if len(line[0]) < 4: #skip short words or especially single letters
                    continue
                if line[0] in wordFrequencyDictionary:
                    wordFrequencyDictionary[line[0]] = wordFrequencyDictionary[line[0]] + int(line[1])
                if line[0] not in wordFrequencyDictionary:
                    wordFrequencyDictionary[line[0]] = int(line[1])

        c = Counter(wordFrequencyDictionary) #take the top 10 most frequent words from the compiled dictionary
        wordFrequencyDictionary = c.most_common(10)

        return wordFrequencyDictionary

    def exportCleanData(self):
        with open('data/bookdata.csv', 'w') as csv_file:
            # Will write in following order: 'bookID', 'title', 'subtitle', 'year', 'most_frequent_words']
            writer = csv.writer(csv_file)

            list_form = list(self.bookMetaData.values()) #convert dictionary to a list

            for x in list_form:
                writer.writerow(x) #write list to CSV file


    def findUniqueDisciplines(self):
        #Function finds all of the unique disciplines/subjects present in the dataset
        list_form = list(self.bookMetaData.values())
        list_of_disciplines = []
        for x in list_form:
            for y in x[4]:
                list_of_disciplines.append(y)

        list_of_disciplines=list(set(list_of_disciplines)) #remove duplicates from list

        return list_of_disciplines

    def findUniqueYears(self):
        #Function generates all of the years present in the dataset
        list_form = list(self.bookMetaData.values())
        list_of_years = []

        for x in list_form:
            list_of_years.append(x[3])

        list_of_years = list(set(list_of_years)) #remove duplicates
        list_of_years.sort() #sort the years

        return list_of_years

    def calculateBooksByDiscipline(self):
        list_of_disciplines = self.findUniqueDisciplines()
        discipline_book_count = {} #dictionary to hold counts

        for key in self.bookMetaData: #run through every "key"
            for discipline in self.bookMetaData[key][4]: #the disciplines for each book are stored as a list, now iterate through entire list
                if discipline in discipline_book_count:
                    discipline_book_count[discipline] = discipline_book_count[discipline] + 1
                if discipline not in discipline_book_count:
                    discipline_book_count[discipline] = 1

        return discipline_book_count

    def calculateBooksByYear(self):
        year_book_count = {} #dictionary to hold counts

        for key in self.bookMetaData:
            if self.bookMetaData[key][3] in year_book_count:
                year_book_count[self.bookMetaData[key][3]] = year_book_count[self.bookMetaData[key][3]] + 1
            if self.bookMetaData[key][3] not in year_book_count:
                year_book_count[self.bookMetaData[key][3]] = 1

        return year_book_count

    def main_func(self):
        file_list = os.listdir("data/metadata") #get directory list of files for metadata

        for element in file_list: #make sure that you are only grabbing xml files, sometimes operating systems add .ds_store files
            if 'xml' not in element:
                file_list.remove(element)

        for file in file_list:
            newBook = self.acquireMetadata(file)
            if newBook is not None:
                self.bookMetaData[newBook[0]] = newBook # This will simply overwrite pre-existing data if the same key exists

        file_list = os.listdir("data/ngram1") #get new directory list for ngram1

        for element in file_list: #make sure that you are only grabbing txt files, sometimes operating systems add .ds_store files
            if 'txt' not in element:
                file_list.remove(element)


        # Now we find most frequent words from the OCR'd text of each file
        # We need to combine all files first, because each book has a separate file for each chapter
        # After we combine the files into a single file, we call the function to acquire word frequencies
        # We append the top 10 words to the book data
        for fileID in self.bookMetaData:
            temp_file_list = []
            for file in file_list:
                if fileID in file:
                    temp_file_list.append(file)
            if len(temp_file_list)>0: #in case there is a mismatch between metadata and ngram files
                self.mergenGramFiles(fileID, temp_file_list)
                self.bookMetaData[fileID].append(self.acquireWordFrequencies(fileID))


        # Now we want to find the most frequent words from all of the titles combined

        for key in self.bookMetaData:
            self.bookTitles.append(self.bookMetaData[key][1])
            if self.bookMetaData[key][2] != 'No subtitle': #skip adding "No subtitle" for those books with no subtitle
                self.bookTitles.append(self.bookMetaData[key][2])

        #print(bookTitles)


        #print(self.bookMetaData)

        self.exportCleanData()

        self.findUniqueDisciplines()
        self.findUniqueYears()
        self.calculateBooksByDiscipline()







