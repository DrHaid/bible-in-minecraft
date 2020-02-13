#import sys
import re
#import json
import glob
#import os

# this script converts bible chapters into mcfunctions
# the chapters have to be in separate text files and the script executed in the same directory.
# the bible I used was a text file from http://www.gutenberg.org/cache/epub/10/pg10.txt

# read file
def read_source_file(source_file_path):
    source_file = open(source_file_path, "r")
    return source_file.read()


# split raw chapter text into a list of verses
def parse_text_by_verses(raw_text):
    verses = list()
    no_whitespaces_text = raw_text.replace('\n', ' ').replace('\r', ' ')
    iter = re.finditer(r"\d+:\d+", no_whitespaces_text)
    indices = [m.start(0) for m in iter]
    for index in range(len(indices)):
        if index < len(indices)-1:
            verses.append(no_whitespaces_text[indices[index]:indices[index+1]])
        else:
            verses.append(no_whitespaces_text[indices[index]:])

    return verses


# create the book tag for the command
def build_book_tag(volume, book_title):
    book_pages = "" # text component (content of the book)
    for page in volume:
        book_pages += ("\"{\\\"text\\\":\\\"%s\\\"}\"," % (page))

    book_pages = book_pages[:-1]  # delete last comma
    book_tag = "{pages: [%s],title: \"%s\",author:%s}" % (book_pages, book_title, book_author)
    return book_tag


# writes to file
def write_output_file(output_file_path, finished_command):
    output_file = open(output_file_path, "w")
    output_file.write(finished_command)


# splits array l into chunks of length n
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


def build_chest_command(book_tags, book_title):
    slot_construct = "" # sorts the different books into slots of the chest
    slot_counter = 0
    for tag in book_tags:
        slot_construct += ("{Slot:%d, id:\"written_book\", tag:%s, Count:1}" %
                           (slot_counter, tag)) + ","
        slot_counter += 1
    slot_construct = slot_construct[:-1] # detete last comma
    item_component = "{Items:[%s]}" % (slot_construct)

    chest_command = "give @p chest{display:{Name:\"\\\"%s\\\"\"},BlockEntityTag:%s} 1" % (
        book_title, item_component)
    return chest_command


def generate_mcfunction_from_file(file_name, book_title):
    verses = parse_text_by_verses(read_source_file(file_name))
    volumes = list(chunks(verses, 100))
    book_tags = list()
    volume_counter = 1
    for volume in volumes:
        final_book_title = book_title + " Vol." + str(volume_counter)
        book_tags.append(build_book_tag(volume, final_book_title))
        volume_counter += 1

    chest_command = build_chest_command(book_tags, book_title)
    write_output_file(file_name.replace(".txt", ".mcfunction"), chest_command)
        

# Main part
book_author = "God"

for file in glob.glob("*.txt"):
    print("-----------------------------------------")
    print(file)
    book_title = input("Book/Chest Title: ")
    generate_mcfunction_from_file(file, book_title)
