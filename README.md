# CSDS-WIL-Group-17-RAG
Group 17's RAG assignment

downloading steps: - marc
1. download ollama itself.

paste this in powershell: irm https://ollama.com/install.ps1 | iex

OR can download from website (https://ollama.com/download)

2. download nomic (the embedding model)

after downloaded ollama, paste this in powershell: ollama pull nomic-embed-text

3. download python packages

navigate into the project folder in powershell, ensuring that requirements.txt is there in the directory
then paste this into powershell: pip install -r requirements.txt