install:
	python3 -m venv venv;\
	. venv/bin/activate;\
	pip install -r requirements.txt

	git submodule init
	git submodule update

	cd trec_eval/; make

get_collection:
	wget https://msmarco.z22.web.core.windows.net/msmarcoranking/collection.tar.gz
	tar -xvf collection.tar.gz
	mv collection.tsv TILDE/data/collection.tsv

test:
	./search information retrieval