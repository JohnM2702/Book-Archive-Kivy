import sqlite3
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window 
import os, sys
from kivy.resources import resource_add_path, resource_find

from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.theming import ThemableBehavior
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList
from kivymd.effects.stiffscroll import StiffScrollEffect
from kivy.properties import StringProperty, ListProperty



class ContentNavigationDrawer(MDBoxLayout):
    pass

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

class AddingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Discard draft?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                    MDFlatButton(
                        text="DISCARD",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                ],
            )
        self.dialog.open()


Window.size = (1200, 700) 
class BookArchiveApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file("design.kv")


        self.date_dialog = MDDatePicker(mode = "range", accent_color=get_color_from_hex("#5d1a4a"))
        self.date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)

    def build(self):
        self.theme_cls.theme_style = "Dark" 

        connection = sqlite3.connect('bookDatabase.db')
        connection.execute('''CREATE TABLE if not exists BookDetails
                    (Series TEXT, 
                    Title TEXT NOT NULL, 
                    Author TEXT NOT NULL,
                    Page INT,
                    BookID TEXT NOT NULL);''')
        connection.execute('''CREATE TABLE if not exists CompletionDate
                    (Month INTEGER, 
                    Day INTEGER, 
                    Year INTEGER,
                    BookID TEXT NOT NULL);''')

        connection.close()


        return self.screen
    
    def backend_affairs(self, mode, value):
        connection = sqlite3.connect('bookDatabase.db')
        myCursor = connection.cursor()
        
        if mode == 0:
            data = []
            text_fields = value
            for i in text_fields:
                data.append(self.root.ids[i].text)
            
            duration = data[1].split("  -  ")
            endDate = duration[1]
            book_id = endDate[:4] +"-"+ self.dataFetcher(4, endDate[:4])

            myCursor.execute("INSERT INTO BookDetails VALUES (?, ?, ?, ?, ?, ?, ?, ?)\
                                ", (book_id, data[3], data[4], data[5], data[6], data[0], data[2], data[1]))
        

        connection.commit()
        myCursor.close()
        connection.close()

    def dataFetcher(self, mode, valOne):
        connection = sqlite3.connect('bookDatabase.db')
        myCursor = connection.cursor()
        value = 0

        if mode == 0:
            myCursor.execute("SELECT * FROM BookDetails")
            rc=myCursor.fetchall()
            value = str(len(rc))
        elif mode == 1:
            myCursor.execute("SELECT	count(*) as Quantity, Author\
                                FROM	BookDetails\
                                GROUP BY Author\
                                ORDER BY Quantity DESC")
            rc = myCursor.fetchall()
            value = rc
        elif mode == 2:
            myCursor.execute("SELECT count(*)\
                                FROM(SELECT count(*)\
                                    FROM CompletionDate\
                                    GROUP BY Year)")
            rc = myCursor.fetchone()
            value = rc[0]
        elif mode == 3:
            if valOne != "":
                valOne = '%'+valOne+'%'
                myCursor.execute("SELECT	*\
                                    FROM	BookDetails\
                                    WHERE Series LIKE ?", (valOne, ))
                rc = myCursor.fetchone()

                if rc != None: 
                    value = 1
                    self.root.ids.seriesTF.text = rc[1]
                    self.root.ids.authorTF.text = rc[3]
        elif mode == 4:
            valOne = valOne+'%'
            myCursor.execute("SELECT COUNT(*)\
                                FROM BookDetails\
                                WHERE BookID LIKE ?", (valOne, ))
            rc = myCursor.fetchone()
            value = str(rc[0]+1)
        elif mode == 5:
            if valOne != "":
                valOne = '%'+valOne+'%'
                myCursor.execute("SELECT	*\
                                    FROM	BookDetails\
                                    WHERE Title LIKE ?", (valOne, ))
                rc = myCursor.fetchone()

                if rc != None: 
                    value = 1
                    self.root.ids.seriesTF.text = str(rc[1])
                    self.root.ids.titleTF.text = str(rc[2])
                    self.root.ids.authorTF.text = str(rc[3])
                    self.root.ids.pageTF.text = str(rc[4])
                    self.root.ids.typeTF.text = str(rc[5])
                    self.root.ids.hours_spentTF.text = str(rc[6])
                    self.root.ids.datePickerTF.text = str(rc[7])

        connection.commit()
        myCursor.close()
        connection.close()
        return value
    
    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;

        :param value: selected date;
        :type value: <class 'datetime.date'>;

        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''

        if date_range != []: self.root.ids.datePickerTF.text = str(date_range[0]) + "  -  " + str(date_range[len(date_range)-1])

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''



if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    BookArchiveApp().run()
















#home mode 
'''
about and function of the app


'''
#add mode 
'''
can add by choosing a series
    - lets user choose among the existing series
    - lets user add a pre-recorded series
can add standalone books

'''
#dislay mode 
'''
display all books
display by month&year
display by year
display by author
    all submodes can be displayed alphabetically, most recent
'''
#statistics mode 
'''
most read book (list of rereaads)
fastest completion of a book
average time spent on books
# total number of books read
number of books read in each year
# number of different authors
number of different series
total number of pages turned

'''
#search mode 
'''
smart search algorithm: letter casing is not strict, familiarity/accuracy percentage, 
search by author
search by series
search by year
can edit infos of books

'''
#to read list mode 
'''
can add books to be read
can update status of books (ongoing, completed, not yet started)

'''