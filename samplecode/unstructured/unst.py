from unstructured.partition.auto import partition
from unstructured.documents.elements import PageBreak
from itertools import groupby

elements = partition(filename="Saraswathi - Application Summary.pdf", 
                     strategy='hi_res')

content=[]
for el in elements:
    content.append([el.metadata.page_number,el.text])

content={ key:' '.join([ subgroup[1] for subgroup in group]) 
         for key, group in groupby(content, key=lambda x: x[0])}


for key in content.keys():
    print(key,content[key],'\n')
    print('-----------')

