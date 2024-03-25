install:
	python3 -m venv venv;\
	. venv/bin/activate

	git submodule init
	git submodule update
	
	cd TILDE/ ;\
	pip install -r requirements.txt

	cd trec_eval/; make

get_collection:
	wget https://msmarco.z22.web.core.windows.net/msmarcoranking/collection.tar.gz
	tar -xvf collection.tar.gz
	mv collection.tsv TILDE/data/collection.tsv

test:
	./search information retrieval