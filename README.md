## Revert Risk models benchmarking:
Repository that implements the logic for revert risk models performance testing and comparing
It is mainly based on the model inference logic is implemented in 
[![Knowledge Integrity repo](https://img.shields.io/badge/GitLab-repo-orange)](https://gitlab.wikimedia.org/repos/research/knowledge_integrity)

### Data used: 
As for analysis I have used the sample of 10K random samples from the testing dataset  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8174336.svg)](https://doi.org/10.5281/zenodo.8174336)

Numbers obtained are super close to what we reported in the paper [![DOI:10.1145/3580305.3599823](https://zenodo.org/badge/DOI/10.1145/3580305.3599823.svg)](
https://doi.org/10.1145/3580305.3599823), but you can use bigger sample to get more reliable results. 

**ORES scores**: We use Wikimedia Analytics Cluster and [this script](https://github.com/trokhymovych/KI_multilingual_training/blob/main/modules/ores_scores_collection.py) for ORES scores collection, that are later used in the analysis.


### Models used: 

- Pretrained language-agnostic [model binary link](https://gitlab.wikimedia.org/repos/research/knowledge_integrity/-/tree/main/pretrained_models)
- Pretrained multilingual [model binary link](https://drive.google.com/file/d/1_nIWa9g8HLn88RmMlS-8n-qqiW9DZa6u/view?usp=drive_link).

### Approach:

**Note**: I am running presented scripts and notebooks from *knowledge_integrity* repo parent directory.

Getting scores for RRLA: 
```bash
poetry shell
poetry install --extras "revertrisk"
python test_performance_rrla.py
```

Getting scores for RRML: 
```bash
poetry shell
poetry install --extras "revertrisk-multilingual""
python test_performance_rrla.py
```

Later obtained files + ORES scores file + ground truth data is used in the notebook **"01_RR_performance_benchmark"**
for models metrics calculation and comparison. 
