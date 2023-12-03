# XML to OMPL Converter for the Ableton Live Object Model Documentation

## IDEA 
Ableton LIVE is one of the most popular Music Production Softwares. 
And it has an API, which you can use via a Control Surface Script or with the bundled Software MAX DSP.

You can pretty much control every aspect of a live set (a song/document) through this API, which is also called Live Object Model

However, the documentation is confusing and hard to work with. There are two sources, one is on the website of the MAX for Live Documentation and an unofficial one, made by Julien Bayle with the help of a script called LiveAPI_MakeDoc, which puts out all accessible API points in a XML file.

Here is a link:

the script: 
[https://github.com/NSUSpray/LiveAPI_MakeDoc](https://github.com/NSUSpray/LiveAPI_MakeDoc)
and the resulting xml file:
[https://structure-void.com/PythonLiveAPI_documentation/Live11.0.xml](https://github.com/NSUSpray/LiveAPI_MakeDoc)

Those Control Surface Scripts are programmed in Python, which was the main reason for me to take this course in CS50. (And I liked it a lot)

My idea was to bring this document into a format which is much more easy to overview. I really like the way MindMaps have foldable branches. I use the software XMind. It can't import xml files, but OPML was an importable format.

I thought writing a code to transform this xml data structure into the OPML Format is a good idea. In the future features probably will be added in the API and all you have to do then is to run the programm and have a beautiful documentation.

## Methodology and steps
It was obvious me that it would be best to use OOP for this to store everything into a class and have methods to come with it.

### 1) import the data from the xml file
I used the library xml.etree.ElementTree to import the data into one list. 

**Data Structure**
Objects (or Modules) have Children, Methods, Properties, Sub-Classes, Listener. Those will be used to group elements together.
I used keywords, tags to break the elements into the different pieces, regarding type of object, path and description and stored them into a dictionary with a unique id as a reference.

The hierachy of the xml files is flat though.
e.g. 
Live.ChainModule
Live.Chain.ChainClass
Live.Chain.Chain.name
Live.Chain.Chain.solo

What I wanted is to build a tree structure with correct relationships:

![](tree_struct.png)

### 2) Referencing and building a tree structure
I then searched each element and referenced in both directions parent and children, so it is possible to climb between branches up and down.

The build_tree_recursive_with_groups_as_children function constructs the hierarchical tree structure, where elements are organized based on their parent-child relationships. Groups are treated as special nodes that group related elements together.

The TreeNode class is a fundamental part of the tree structure. Each node in the tree is represented by an instance of this class. It has the following attributes:

data: Stores information about the LOM element associated with this node.
children: A list of child nodes, representing the elements nested beneath the current element.
The TreeNode class is used to build a hierarchical representation of the LOM, where each node corresponds to an element in the LOM XML.


### 3) write the opml file for XMind
I build the desired structure in XMind with a very few elements manually, using XMind specific features like:
- note for the description 
- label to indicate the type of element

Then I exported it as a OPML file and re-engineered the outline formatting to match those features:

`‌outline = f'{indent}<outline text="{name}" _note="{description}" type="label" _label="{tag}">\n'`

## Testing (test_AbletonLOM.py)
I did the testing procedures after everything worked. Given that the xml file input is static, because it is actually always the same file, there was no need to test to code for unexpected input.

However, as the search feature in XMind is very slow, because of the amount of text, 

## Outcome, plans and summary

It works perfectly for my use cases. Now it is a real joy to look for certain aspects. 
I have two plans for the future:

1) I want to make it accessible for the ableton community. I think the best way is to use my output side of the program to build a folder structure for a static site generator like hugo to make it fast and accessible for the web.

2) porting the LiveAPI_MakeDOC script to Python3:
Unfortunately the underlying source is not working in the latest updates of Ableton, because they switched to Python 3. The script latest commit is dated to 2011 and has been archived by its owner.
I'll try to make it work with the latest Ableton version to make sure the latest added features are availble.

Thank you David Malan and everybody else at CS50 at Harvard, it has been a great journey to dive into Python programming. The results will be very beneficial for my workflow!





