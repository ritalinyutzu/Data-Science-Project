!pip install -U synonyms
!python -c "import synonyms" # download word vectors file

!pip install opencc
from opencc import OpenCC
import synonyms
cc = OpenCC('tw2s')

str_ = '鈦'
synonyms.display(cc.convert(str_))