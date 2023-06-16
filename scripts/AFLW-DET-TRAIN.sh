CUDA_VISIBLE_DEVICES=0,1 python /content/cpm/main.py \
	--train_lists /content/cpm/datasets/AFLW_lists/train.GTB \
	--eval_ilists /content/cpm/datasets/AFLW_lists/test.GTB \
	--num_pts 19 \
        --data_indicator AFLW-19 \
	--save_path ./snapshots/AFLW-CPM-DET 
	
