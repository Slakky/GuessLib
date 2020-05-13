# guesslib

An open-access tool for NGS library recognition brought to you by the GuessLib team:

- [Claudio Novella Rausell<sup>1</sup>](https://github.com/nrclaudio)
- [Erik Zhivkoplias<sup>1</sup>](https://github.com/zhivkoplias)
- [Karl Nyrén<sup>1</sup>](https://github.com/karlnyr)
- Leonard Sparring<sup>1</sup>
- [Karthik Nair<sup>1</sup>](https://github.com/KarNair)
- Shrija Srinivasan<sup>1</sup>

> <sup>1</sup>: contributed equally


The analysis of publicly accessible RNA-seq data is becoming more and more popular in the field of bioinformatics. However, as the biological datasets are usually not curated, the metadata is not annotated properly.
One time-saving piece of information regarding RNA-seq is the library type, which is used to analyze the data
published by other researchers. We present in this paper GuessLib, an open access solution for library type determination created to fill in this missing metadata type. GuessLib was mainly developed in Django using an
in house algorithm for library type determination.

RNA-Seq relies on mapping multiple fragmented short sequences (raw reads) onto the known sequence. In order to assemble them correctly, it’s crucial to know the features of the sequenced reads. These features strictly depend on the library preparation kits. The kit provides all of the enzymes required for the extraction of RNA from the cell and prepares it for sequencing (RNA library construction). Different kits follow different protocols, which result in specific RNA library types.

Publicly available RNA-Seq datasets dont always contain information on RNA library type was used to produce RNA-Seq data, whereas the papers linked to those datasets provide only with information about the names of library preparation kits. Unfortunately, the supplier’s websites may not store information about that particular kit if its not on sale anymore, so if a person is interested in analyzing such RNA-Seq dataset have to align raw reads with different parameters to see which option would give the best alignment score. Therefore, a lot of human effort and computational resources are spent before a user starts doing the actual bioinformatics analysis (analysis of the presence and quantity of the expressed genes).

The aim of our project is to build up a web app that quickly analyzes a subset of the submitted raw reads (FASTQ file format), evaluates the reads composition based on the reference sequence, and informs the user on the RNA library type that was used to produce the total RNA-Seq data
