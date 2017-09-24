# Python-for-Earth-Science-Students

```python
# Pay no attention to this cell
# All will be revealed in due time.
import pandas as pd
from IPython.display import Image
syllabus=pd.read_csv('syllabus.csv',header=0)
syllabus=syllabus.fillna("")
syllabus.index = range(1,len(syllabus)+1)
```

## Introduction to Computational  Earth Science

Authors: Lisa Tauxe,  ltauxe@ucsd.edu & Hanna Asefaw, hasefaw@ucsd.edu


### Computers in Earth Science

Computers are essential to all modern Earth Science research.  We use them for compiling and analyzing data, preparing illustrations like maps or data plots, writing of manuscripts and so on.  In this class you will learn computer programming with special applications useful to Earth Sciences.  We will learn Python, an object-oriented programming language.

### Python

So why Python?  

- Flexible, freely available, cross platform
- Easier to learn than many other languages
- It has many numerical, statistical and visualization packages
- It is well supported and has lots of online documentation
- The name 'Python' refers to 'Monty Python' - not the snake and many examples in Python documentation use jokes from the old Monty Python skits.  If you have never heard of Monty Python, look it up on youtube; you are in for a treat. 

Which Python?  
- Python is undergoing a transition from 2.7 to 3.  The notebooks in this class, apart from a few exceptions, are compatible with both.  
- If you are not using the university computers for this class, we recommend that you install the most recent version of Anaconda  python for your operating system : 
https://www.anaconda.com/download/



### Class Structure: 

- There will usually be three lectures a week and one discussion session. 
- Each lecture begins with a quick review (~5 min) and procedes into the topic of the day.  Interspersed in the lecture will be  time to practice the skills covered in the lecture.    
- There will be a programming assignment every week, due BEFORE CLASS one week from the assignment.  These are not optional because you can only learn how to program by programming.  This is not a spectator sport. 
- We'll discuss the assignments during discussion section, both before they are due and after they have been graded.  
- In lieu of a final exam, there will be a final project - a program of your own design. There is a great deal of flexibility in the choice of what the program will do but there are some compulsory elements to it, which we will discuss in more detail later.  


## Class Expectations

- Attendence is strongly suggested and weekly homework assignements are mandatory as is  the final project.    
- Homework will not be accepted late.  
- You may  consult any online resources to help you solve your problem. This is  encouraged. But do NOT copy verbatim what you find there. You must re-work anything through your own brain and in your own words or you will not learn how to program. Copying programs does not help you learn and in fact it is "cheating".  Cheating will be reported to the authorities and will result in unpleasantness all around. 
- The best way to figure out the problem is to attend the lecture, do the practice problems and attend the discussion section where your TA can help.  



## Lectures


```python
syllabus[['Topic','Application']]

```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Topic</th>
      <th>Application</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>Intro to the class</td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>Variables and Operations</td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>Data structures</td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>Dictionaries, program loops (if, while and for)</td>
      <td></td>
    </tr>
    <tr>
      <th>5</th>
      <td>functions and modules</td>
      <td></td>
    </tr>
    <tr>
      <th>6</th>
      <td>NumPy and matplotlib</td>
      <td>seismic record</td>
    </tr>
    <tr>
      <th>7</th>
      <td>NumPy arrays</td>
      <td></td>
    </tr>
    <tr>
      <th>8</th>
      <td>file systems and paths</td>
      <td></td>
    </tr>
    <tr>
      <th>9</th>
      <td>Pandas, file I/O</td>
      <td>P-S wave arrival times</td>
    </tr>
    <tr>
      <th>10</th>
      <td>object oriented programming</td>
      <td>objects and classes</td>
    </tr>
    <tr>
      <th>11</th>
      <td>recursions and exceptions</td>
      <td>fibonacci spiral</td>
    </tr>
    <tr>
      <th>12</th>
      <td>lambda, map, filter reduce, list comprehension</td>
      <td></td>
    </tr>
    <tr>
      <th>13</th>
      <td>data wrangling with Pandas</td>
      <td>seismic travel time plots</td>
    </tr>
    <tr>
      <th>14</th>
      <td>subplots, bar charts pie charts</td>
      <td>elemental abundances</td>
    </tr>
    <tr>
      <th>15</th>
      <td>histograms and cumulative distribution functions</td>
      <td>hypsometric curve</td>
    </tr>
    <tr>
      <th>16</th>
      <td>statistics 101</td>
      <td>Univariate data</td>
    </tr>
    <tr>
      <th>17</th>
      <td>hypothesis testing t, F</td>
      <td></td>
    </tr>
    <tr>
      <th>18</th>
      <td>application to grain sizes</td>
      <td>grain sizes</td>
    </tr>
    <tr>
      <th>19</th>
      <td>line and curve fitting</td>
      <td>Bivariate data &amp; Hubble plot</td>
    </tr>
    <tr>
      <th>20</th>
      <td>maps</td>
      <td>spatial data; earthquake locations/ depths</td>
    </tr>
    <tr>
      <th>21</th>
      <td>gridding and contouring</td>
      <td>IGRF</td>
    </tr>
    <tr>
      <th>22</th>
      <td>rose diagrams and equal area projections</td>
      <td>glacial striations</td>
    </tr>
    <tr>
      <th>23</th>
      <td>matrix math - dot and cross products</td>
      <td>poles to planes and more</td>
    </tr>
    <tr>
      <th>24</th>
      <td>plotting great and small circles</td>
      <td></td>
    </tr>
    <tr>
      <th>25</th>
      <td>3D plots of points and surfaces</td>
      <td>benioff zone</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Time series  - periodograms</td>
      <td>temporal data</td>
    </tr>
    <tr>
      <th>27</th>
      <td>Animations</td>
      <td>Indian plate motion</td>
    </tr>
  </tbody>
</table>
</div>



## Jupyter notebooks

This class is entirely structured around a special programming environment called jupyter notebooks. A Jupyter notebook is a development environment where you can write, debug, and execute your programs.  Put all the lectures and other directories associated with this package into a directory on your computer.  To launch a notebook, follow the instructions on this website:  

jupyter-notebook-beginner-guide.readthedocs.io/en/latest/execute.html

Launch Lecture_01_syllabus.ipynb

You should now be looking at this notebook that I am reading from.  

### Jupyter notebook anatomy

Jupyter notebooks have two basic _cells_:

- Markdown: for typesetting notes. That is what this one is.  

- Code: for writing python code

You can insert a new cell by finding the drop down menu:  





```python
Image(filename='Figures/insertCell.png')
```




![png](output_4_0.png)



You change the cell "flavor" with the menu that defaults to 'Code' and can be changed to "Markdown".  

And you "execute" a cell (either _typeset_ or _run_ the code)  by  clicking  on the run key (sideways triangle with vertical line) or run the cell under _Cell_.  


```python
Image(filename='Figures/menuBar.png')
```




![png](output_6_0.png)




### Practice with inserting cells

Insert a cell below this one.   Change it  to ‘Markdown’ and type some notes.  You can just type most things, but special features like Section headers, bullets, numbered lists and other fun things require special formatting.  For a pretty good explanation see this link: 
https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet



**Run** the cell to typeset your notes.  If you want to change them, just double click on the cell, type away, then 'run' it again.  

### Practice with markdown cells

If you see plain text in one of the cells in the lecture notebooks, just double click on it and all will be revealed.  Try double clicking on THIS cell to see how to make section headers - then run it.   
 
### Practice with code cells
Insert another cell, keeping it the default of _Code_.  

type: **print "Hello World"** in the cell and then run that.  

It should look like this:   


```python
print ("Hello World")
```

    Hello World


Congratulations! That was your first Python program. 

In a code block, you can only type valid python statements EXCEPT
after a pound sign - everything after that will be ignored.  
That is how you write "comments" in your code to remind yourself or tell others what you were thinking:  


```python
# I can type anything here
but not here
```


      File "<ipython-input-18-ae00b29ef7b9>", line 2
        but not here
                   ^
    SyntaxError: invalid syntax



That was an example of a _bug_ which oculd be fixed by commenting out the second line, or making it a valid statement:


```python
# I can type anything here
# but not here
print ("but not here")
```

    but not here


### ### How to take notes in class

Now you know how to insert a markdown cell and write in it, you should take advantage of these notebooks to add your own commentary to the lecture notebook as you go.   You could even have a separate notebook open in another  window in which you can type notes.  For that, you need to know how to create your own notebook and save it. And it would be handy to know how to split your screen to have two side by side notebooks. 

#### Creating new notebooks, naming and saving.  

To open a new notebook, pull down the 'File' menu and select the 'New Notebook => Python 3' option.  You can 'tear' the notebook off so it is in a separate window if you like seeing both together.  

To rename the notebook, choose 'Rename' under the File menu.  

To save it, click on the disk icon on the menu bar. Wait until the 'checkpoint created...' message disappears before you try to exit the notebook.  

#### Splitting your screen

Click on the green button in the top left corner of your browser and drag it to the side you want your lecture in.  Put your "notes" notebook on the other side.  


### Practice with notebooks

Open a new notebook, rename it to, for example, 'Lecture_01_notes', split your screen if you like, make a Markdown cell, write some notes, and save the file.  Now look in your folder and see your brand new notebook!  


### Final project

We will learn much more about markdown and code blocks in the coming weeks and you will begin to understand how to write programs.  As you learn new conepts, start thinking about what you'd want to do for a final project.  


There is a great deal of flexibility on the exact nature of the final project but it must be related to Earth and Space Science and include these characterisics:  
- at least one module that includes at least three functions
- it must read in at least one data file
- it must make  at least one plot.
- There must be at least three markdown blocks:  
    -a description of what the  program does, 
    - how to use the program, and 
	- what the scientific conclusion was


Turn the project in as a zipped directory with all parts necessary to run it (the data files, figures, modules and whatever else is required).    
           
Here are a few possible ideas: 


		
1) Make a movie:		
		
- of lightning strikes across the continental US		
- of volcanic eruptions across the western US		
- of plate motion over the last 200 Ma		

2)  Make a 3D image of the solar system with orbiting planets 
				
3) Recreate your favorite plot from a number of examples you will be given. 		
				
4) Design your own project: 

In Week 6, you will be asked to turn in a proposal for the final project. In the proposal, you'll describe the final project and how it relates to Earth and Space Science.  At that stage, you still may not have all the skills required to complete your project, but we can let you know if it is possible and substantial enough for the final project.  The final project is worth five times as much as a weekly assignment. We've designated the last two class periods as work days, but by then you should have spent some time working on it.

Each student will have a chance to present their final project.  
