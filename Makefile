install:
	python3 -m venv venv
	source venv/bin/activate
	
	cd TILDE/;\
	pip install -r requirements.txt

	wget https://msmarco.z22.web.core.windows.net/msmarcoranking/collection.tar.gz;\ 
	tar -xvf collection.tar.gz;\ 
	mv collection.tsv data/collection

	cd ../trec_eval/; make

test:
	./search information retrieval