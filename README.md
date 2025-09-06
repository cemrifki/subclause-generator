# Subclause Generation
This repo contains the source code for generating subclauses from a given sentence in English and Turkish. This functionality is also used in the work stated below. However, the following performs a comprehensive study on sentiment analysis; the creation of subclauses in a novel way is only a part of the whole work:

[Combination of Recursive and Recurrent Neural Networks for Aspect-Based Sentiment Analysis Using Inter-Aspect Relations](https://ieeexplore.ieee.org/document/9078752).
Cem Rifki Aydin, Tunga Gungor. IEEE Access

This approach was originally developed for English only, generating subclauses from texts on a sentence-by-sentence basis. The functionality can be further enhanced by incorporating additional dependency relationships. In version 0.2.0, support for Turkish has also been introduced, increasing portability. With minor adjustments, the approach can be adapted to other languages as well. This also performs a basic preprocessing operation prior to extracting subclauses, which can be skipped. In addition, at the end of each subclause, we add the punctuation mark that appears at the end of the whole sentence. Lastly, redundantly appearing tokens at the beginning and end of subclauses (e.g. "and") are removed.

## Requirements

- Python 3.9 or a newer version of Python
- spacy
- numpy
- thinc

## Execution

I ran this code by relying on `Python 3.9`. A simple usage of the code is given below. First, go into the subclause_generator folder. Then you can run the below lines of code or similar ones. You can also import this module in your projects by performing minor changes:

```
from subclauses import SubclauseGenerator
SC = SubclauseGenerator("en")
subcls = SC.convert_to_subclauses("The vibe is relaxed and cozy, the service was great, and the ambiance was good!")
print(subcls)
# The result is: [['the', 'vibe', 'is', 'relaxed', 'and', 'cozy', '!'], ['the', 'service', 'was', 'great', '!'], ['the', 'ambiance', 'was', 'good', '!']]
```

If you want to create subclauses based on Turkish texts, you can run the below exemplary commands:

```
from subclauses import SubclauseGenerator
SC = SubclauseGenerator("tr")
subcls = SC.convert_to_subclauses("Yemek çok iyiydi ve servis de süperdi.")
print(subcls)
# The result is: [['yemek', 'çok', 'iyiydi', '.'], ['servis', 'de', 'süperdi', '.']]
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
All the code was written by Cem Rifki Aydin
