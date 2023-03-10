The folder PatchPerPixMatch contains matching results for all of the hemibrain (version 1.2) vs all phase 1 MCFO samples in density categories 2 and 3. 

Hemibrain body IDs are grouped into subfolders via the last two digits of the numerical part of their name. 

For each of ~30,000 hemibrain body IDs, there is a pdf and a spreadsheet (xlsx). 


*** Contents of the pdfs: ***

-- Top left image: Maximum intensity projection (MIP) of the MCFO sample
-- Mid left: Color MIP of best-matching channel
-- Bottom left: Color MIP of best-matching channel, dimmed and overlaid with color MIP of EM body
-- Top right: EM-, line-, sample-, rank- and score info, as well as a MIP of the full expression pattern of the line (to get a sense of the respective density. Note that these are currently missing for a few lines, we're in the process of retrieving them and will update the pdfs accordingly.).
-- Mid right: MCFO masked by best-matching PatchPerPix fragments 
-- Bottom right: MCFO masked by best-matching PatchPerPix fragments (sometimes pruned), overlaid with EM body in purple. 
 
Matches are sorted by PatchPerPixMatch ranks. Samples of the same line are sorted in directly behind the best match of a line.


*** Contents of the spreadsheets: ***

Spreadsheets are provided to facilitate annotation efforts. 
Each row contains line name, slide code, and PatchPerPixMatch rank of a match as contained in the pdf, sorted by rank.


*** Which hemibrain body IDs are included: ***

A list of ~30,000 hemibrain version 1.2 body IDs selected from neuprint by Hideo Otsuna by means of neuprint neuron quality tags, size, etc. For the same list of body IDs, Color MIP search results will be published on NeuronBridge (with the upcoming update to hemibrain version 1.2). If you want more details on the body ID selection process, please contact Hideo. 


*** Which MCFO samples are included: ***

Brains from FlyLight's published MCFO of sparse and medium density Generation 1 GAL4 lines are included (Gen1 MCFO Phase 1 Categories 2 and 3, published at https://www.biorxiv.org/content/10.1101/2020.05.29.080473v1 ). Source imagery can be viewed or downloaded at https://gen1mcfo.janelia.org/. 


*** Convenient batch-download of results for multiple EM body IDs:***

To download results for a list of EM body IDs to your local machine without having to pick every single one manually, 
you can use the following convenience scripts for automated batch-download (depending on your OS):
batch_copy_for_Mac.sh
or
batch_copy_for_Linux.sh
Open the appropriate script in your text editor of choice; The HowTo is in there. 
For Windows users: Sorry, no script yet.. But the good news is: We're in the process of making batch download convenient for everyone via a browser-based interface. We'll announce this via email (and update this ReadMe accordingly) as soon as it exists. 


*** How the PatchPerPixMatch results were generated: ***

-- PatchPerPix segmentations of the MCFO samples: git repo https://github.com/Kainmueller-Lab/PatchPerPix_private.git branch master, commit b315287b97e140b5b5dc606aafffb9f2b4daad79 
-- PatchPerPixMatch search results: git repo https://github.com/Kainmueller-Lab/flymatch.git branch dka_dev, commit 46c44659c93a880f1113e0d4235e6ef6d10e994d
-- PatchPerPixMatch pdfs and spreadsheets: git repo https://github.com/Kainmueller-Lab/flymatch.git branch dka_dev, commit TBA

The git repos will be made public upon publication of the results; if you want access before please contact kainmuellerd@janelia.hhmi.org
