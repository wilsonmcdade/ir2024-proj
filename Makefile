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

train:
	#wget https://git.uwaterloo.ca/jimmylin/doc2query-data/raw/master/T5-passage/doc_query_pairs.train.tsv
	python3 TILDE/train_tilde.py --train_path doc_query_pairs.train.tsv --save_path tilde_ckpts --gradient_checkpoint

index:
	python3 TILDE/indexing.py --ckpt_path_or_name ielab/TILDE --run_path TILDE/data/runs/run.trec2019-bm25.res --collection_path TILDE/data/collection.tsv --output_path TILDE/data/index/TILDE
