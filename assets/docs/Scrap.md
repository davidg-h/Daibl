# Srap README


first of all look at this chart:
<div align="center">
  <img src="assets/docs/docs_images/Screenshot-RAG-trends.png">
</div>

As we started the Project back in March 2023 the term Retrieval Augmented Generation (RAG) wasn't even invented!!!
And yet it is the term that exactly describes our Project.
The Term RAG is the number one solution for building custom knowlege agnostic Chatbots for obvious Reasons:

1. It is easier and cheaper to implement than fine-tuning a model
2. The verification of facts is much easier - the sources are given
3. The System can easily adapt to new Information - (example: lectures for new semester)

The field is evolving rapidly and unfortunatly our solutions are a bit outdated.
As we started the Project we didn't know anything about Vector-databases, Embedding algorithms and Prompt Engineering, nor about Large Language Models, Venvs, Slurm, or alot about python in general.
All that is to say the Code works but could/should be improved drastically.

## The Present

To understand how the code is working at the Moment, it is useful to go through the Notebook data_processing.ipynb.
Keep in mind that much of the things described there are already outdated for the production code (like all that has to do with simple BERT) or are unnessesary if one would switch to a vector db (like Chroma DB).

To understand how the Scraping works (this is actually still relevant), one should read the Notebooks data_scraping_new and data_scraping_intranet.
The data collection could be improved too, if one could collect all the data that is stored in pdf files (like all the exam schedules or timetables)

The data is stored in an sqlite db, which is not stored in the git repository.
The data needed could be broduced my initialisind the database and going through the scraping notebooks and the processing notebooks.

The db_init module has the logic to save and load pandas dataframes to the db.
Pandas Dataframes are the main source of handling and manipulating data.

The calculate_embeddings is used to calculate embeddings with the hardware of the HPC Server from the TH Nuremberg.


The Notebooks in the data visualization directory help to grep hold of the Data and understand their true meaning.
The T-SNE Notebook trys to visualize different Embeddings, but this isn't much of a value to understand or compare them.


## The Future

There are many ways to improve the project.
For example: all the Embeddings should be stored in a vector database.
Vectordatabases are getting popular in the same time as RAG, and the chart for google search is roughly the same as the one at the top.
Chroma DB is a good choice for a vector db. (Its one of the simpler ones)
It simplifies the storing of the embedding (as vector storage is its main target),
the embedding creation (as it has support to autoencode most embedding algorithms) and the retrieval (as it has the Ranking functions build in)

The prompting can be leveraged by libraries like llama-index, which has great support for accessing different LLMs, has well constructed Querie Templates and much more.
The possibility of chaining multiple Queries is good, too.


TODO:
- For future it would be advised to store vectors in a vector db (Milvus, Chroma DB).
- Srcaping and reading pdf files would be very useful.
- Continous scraping would be useful, too. (example th-mensa API)
- splitting data into good chunks and embed them




