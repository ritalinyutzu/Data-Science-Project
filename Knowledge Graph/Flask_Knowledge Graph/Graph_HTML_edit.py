
import os
import codecs
def HTML_edit_func():
    f = codecs.open(os.getcwd()+"/templates/Knowledge Graph.html","r").read()
    add = '''
    <!-- Paste this code into the BODY section of your HTML document  -->
    <select size="1" name="jumpit" onchange="document.location.href=this.value"> 
        <option selected value="">Make a Selection</option>
        <option value="http://127.0.0.1:5000/">All Brand</option>
        <option value="http://127.0.0.1:5000/?Brand=Brand_A">Brand_A</option>
        <option value="http://127.0.0.1:5000/?Brand=Brand_B">Brand_B</option>
        </select> 
    '''
    f_new = f[:f.find('<div id = "mynetwork">')]+add+f[f.find('<div id = "mynetwork">'):]
    HTML_file = open(os.getcwd()+"/templates/Knowledge Graph.html","w")
    HTML_file.write(f_new)
    HTML_file.close()
