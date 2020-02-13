import json
import os
from itertools import count

def chop(s): # assume len(s) > 240
    i = s.rfind(" ",0,240)
    if(i < 0): i = 239
    s, t = s[:i+1], s[i+1:]
    t = t.split(" ")
    t = "".join(t[i]+("\\\\n" if i % 4 == 3 else " ") for i in range(len(t)))
    return (s, t)

books = [] #bible file taken from https://github.com/aruljohn/Bible-kjv
with open(os.path.join("bible","Books.json"),"r",encoding="utf-8") as f: books = json.loads(f.read())

for book_name in books:
    func_name = book_name.lower().replace(" ","_")
    with open(os.path.join("bible",book_name+".json"),"r",encoding="utf-8") as f: book = json.loads(f.read())
    output = 'give @s written_book{generation:2,author:"multiple authors",title:"'+book_name+'",pages:['
    for i in range(0,len(book["chapters"]),10):
        output += '\'[""'
        for j in range(i,min(i+10,len(book["chapters"]))):
            output += ',{"text":"'+book_name+" "+str(j+1)+'\\\\n","color":"dark_purple","clickEvent":{"action":"run_command","value":"/function bible:'+func_name+"_"+str(j+1)+'"}}'
        output += "]',"
    output = output[:-1] + "]}"
    with open(os.path.join("..","data","bible","functions",func_name+".mcfunction"),"w",encoding="utf-8") as f: f.write(output)
    for chapter in book["chapters"]:
        output = 'give @s written_book{generation:2,author:"multiple authors",title:"'+book_name+" "+chapter["chapter"]+'",pages:['
        for verse in chapter["verses"]:
            if(len(verse["text"]) > 240):
                chopped = chop(verse["text"])
                output += '\'["",{"text":"'+chopped[0]+'"},'
                output += '{"text":"\u2026","hoverEvent":{"action":"show_text","value":"'+chopped[1]+'"}}]\','
            else: output += '\'{"text":"'+verse["text"]+'"}\','
        output = output[:-1] + "]}"
        with open(os.path.join("..","data","bible","functions",func_name+"_"+chapter["chapter"]+".mcfunction"),"w",encoding="utf-8") as f: f.write(output)
