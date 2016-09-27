"""
HTML <-> text conversions.
"""
import re

from html.parser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc

import os
import string

import codecs

inputfile=r"D:\EigeneDateienMarkus\SkyDrive\Dokumente\Handball\ASR\ArbeitsgruppeSchiedsrichter_SHV\Qualitaetssicherung\Saison16-17\importtool-py\sro_spiele_today.asp.html"
targetfile=r"D:\EigeneDateienMarkus\SkyDrive\Dokumente\Handball\ASR\ArbeitsgruppeSchiedsrichter_SHV\Qualitaetssicherung\Saison16-17\importtool-py\spielplan.csv"



class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)

            if text =='Sejdaj Samir':
                pass

            self.__text.append(text)
            #self.__text.append(text + ';')




    def handle_starttag(self, tag, attrs):

        if tag=='tr':
            self.__text.append('\n')

##        if tag == 'p':
##            self.__text.append('\n\n')
##        elif tag == 'br':
##            self.__text.append('\n')

    def handle_endtag(self, tag):
        #print("End tag  :", tag)
        pass

        if tag=='td':
            self.__text.append(';')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        #return ''.join(self.__text).strip()
        return ''.join(self.__text)


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text


def main():

    #write result
    #f2 = open(targetfile,'w')

    f2 = codecs.open(targetfile, "w", "utf-8")
    f2.write(u'\ufeff')


    if os.path.splitext(inputfile)[1]==".html":
        print("*******************************")
        f = open(inputfile, 'r')
        text=f.read()
        f.close()

        #HTML to text
        parsedtext=dehtml(text)


        #remove blank lines
        parsedtext="".join([s for s in parsedtext.strip().splitlines(True) if s.strip()])

        print(parsedtext)
        print("****************")

        print("Parse Lines")
        lines=parsedtext.splitlines()

        for line in lines:
            print(line)

            if (line== 'Datum;Start;Liga;Spl. Nr.;Team Heim;Team Gast;Halle;SR 1;SR 2;Del 1;Del 2;Insp;'):
                line='Tag;' + line

            if (line == '<!-- //-->' or line.strip(';') == 'Anz. Tage;10 Tage20 Tage30 Tage60 Tage90 Tage120 Tage') or line==';':
                print("falsch:  " + line.strip())
                pass
            else:
                f2.write(line.strip(';'))
                f2.write("\n")

        f2.close

if __name__ == '__main__':
    main()