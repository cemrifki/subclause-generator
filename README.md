# Subclause Generation
This repo contains the source code for generating subclauses from a given sentence in English. This functionality is also used in the work stated below. However, the following performs a comprehensive study on sentiment analysis; the creation of subclauses in a novel way is only a part of the whole work:

[Combination of Recursive and Recurrent Neural Networks for Aspect-Based Sentiment Analysis Using Inter-Aspect Relations](https://ieeexplore.ieee.org/document/9078752).
Cem Rifki Aydin, Tunga Gungor. IEEE Access

This approach generates subclauses from texts on a sentence-basis in English. However, this functionality can be enhanced by taking into account several other dependency relationships. This can be adapted to other languages as well with minor changes. This also performs a basic preprocessing operation prior to extracting subclauses, which can be skipped. In addition, at the end of each subclause, we add the punctuation mark that appears at the end of the whole sentence. Lastly, redundantly appearing tokens at the beginning and end of subclauses (e.g. "and") are removed.

## Requirements

- Python 3.7 or a newer version of Python
- spacy 2.1.0

## Execution

A simple usage of the code is given below. You can also import this module in your projects by performing minor changes:
```
from subclauses import Subclauses
SC = Subclauses()
subcls = SC.convert_to_subclauses("The vibe is relaxed and cozy, the service was great, and the ambiance was good!")
print(subcls)
# The result is: [['the', 'vibe', 'is', 'relaxed', 'and', 'cozy', '!'], ['the', 'service', 'was', 'great', '!'], ['the', 'ambiance', 'was', 'good', '!']]
```

## Citation
If you find this code useful, please cite the following in your work:
```
@ARTICLE{9078752,  
    author={C. R. {Aydin} and T. {Güngör}},  
    journal={IEEE Access},   
    title={Combination of Recursive and Recurrent Neural Networks for Aspect-Based Sentiment Analysis Using Inter-Aspect Relations},   
    year={2020},  
    volume={8},  
    pages={77820-77832},  
    doi={10.1109/ACCESS.2020.2990306}}
```
## Credits
Codes were written by Cem Rifki Aydin
