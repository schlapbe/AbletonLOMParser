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
Objects (or Modules) have Children, Methods, Properties, Sub-Classes, Listeners.
I used keywords, tags to break the elements into the different pieces, regarding reference, type of object, path and description and stored them into a dictionary.

The hierachy of the xml files is flat though.
e.g. 
Live.ChainModule
Live.Chain.ChainClass
Live.Chain.Chain.name
Live.Chain.Chain.solo

What I wanted is to build a tree structure with correct references:

LIVE
├── ChainModule
│   ├── ChainClass
│   │   ├─Chain
│   │   │   ├── name
│   │   │   ├── solo
├── ChainMixerDevice
│   ├── etc....
│   │   ├── etc...│   

### 2) Referencing and building a tree structure
I then searched each element and referenced in both directions parent and children, so it is possible to climb between branchen up and down.

I then wrote methods to get the children of each

3) write the opml file


