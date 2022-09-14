import markdown
import os
import pickle as pkl
from bs4 import BeautifulSoup
from mdutils.mdutils import MdUtils
from mdutils.tools.Table import Table
# from mdutils import Html

DATABASE_FILE_NAME = "database.pkl"
NOTES_FILE_NAME = "README.md"

f = open(NOTES_FILE_NAME,"r")
papernotes = markdown.markdown(f.read(),extensions=['tables'])
papernotes = BeautifulSoup(papernotes,"html.parser")

# get database of old papers
if(os.path.exists(DATABASE_FILE_NAME)):
    with open(DATABASE_FILE_NAME,"rb") as f:
        donepapers = pkl.load(f)
else:
    donepapers = {}

paperarray = []

# read all papers, filter for new ones

## fetch all papers in the list
alltables = papernotes.find_all("tbody")
for table in alltables:
    for row in table.find_all("tr"):
        paperarray.append(row)

## convert html to list of objects (dict)
paperdict = {}
updatedKeys = []
for paper in paperarray:
    name,paperlink,tags = paper.find_all("td")
    tags = tags.find_all("a")
    
    # convert html to strings
    notes = name.find("a").get('href')
    name = name.find("a").get_text()
    paper = paperlink.find("a").get("href")
    taglinks = [tag.get("href") for tag in tags]
    tags = [tag.get_text() for tag in tags]
    
    ### new paper
    if(name not in donepapers.keys()):
        paperdict[name] = {"notes":notes,"paper":paper,"tags": tags,"taglinks": taglinks}    
    ### changed paper (new/changed tags)
    elif(tags != donepapers[name]["tags"]):
            updatedKeys.append(name)
            #### change the tags in the donepapers
            donepapers[name]["tags"] = tags
            donepapers[name]["taglinks"] = taglinks
        
    
        
# create notes section for new papers 
for name,content in paperdict.items():
    mdFile = MdUtils(file_name=content["notes"])
    mdFile.new_header(1, "["+name+"]("+content["paper"]+")")
    tagstrings = ["["+tag+"]" for tag in content["tags"]]
    taglinks = ["("+tag+")" for tag in content["taglinks"]]
    mdFile.new_paragraph("Tags: "+", ".join([tagstrings[i]+taglinks[i] for i in range(len(tagstrings))]))
    mdFile.new_header(2, "Summary")
    mdFile.new_header(2, "Technical Details")
    mdFile.new_header(2, "Notes")
    mdFile.create_md_file()
    
# create combined dataset of papers
allpapers = donepapers | paperdict 
    
# create tag page for all new tags
pertag = {}
for name, content in allpapers.items():
    for taglink in content["taglinks"]:
        tag = taglink.replace('tags/','').replace(".md","")
        if tag not in pertag:
            pertag[tag] = []     
        pertag[tag].append(name)

# now go over every tag
#  TODO: Richtige links einfügen -> sind noch lokale links
for tag,papernames in pertag.items():
    mdFile = MdUtils(file_name="tags/"+tag)
    mdFile.new_header(1, "Tag: "+tag)
    text_list = ['Name', 'Link', 'Tags']
    for paper in papernames:
        text_list.append("["+paper+"](../"+ allpapers[paper]["notes"] + ")")
        text_list.append("[paper]("+ allpapers[paper]["paper"] + ")")
        tagstring = []
        for i in range(len(allpapers[paper]["tags"])):
            tagstring.append("["+allpapers[paper]["tags"][i]+"](../"+allpapers[paper]["taglinks"][i] + ")")
        text_list.append(", ".join(tagstring))
        
    
    mdFile.new_table(3, int(len(text_list)/3), text=text_list, text_align='center')
    mdFile.create_md_file()
    
# update all tag pages for new papers 

# update all tag pages for edited papers

# save new database with updated papers
with open(DATABASE_FILE_NAME,"wb") as f:
    pkl.dump(allpapers, f)