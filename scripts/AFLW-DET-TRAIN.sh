CUDA_VISIBLE_DEVICES=0,1 python ./main.py \
	--train_lists ./datasets/AFLW_lists/train.GTB \
	--eval_ilists ./datasets/AFLW_lists/test.GTB \
	--num_pts 5 \
        --data_indicator AFLW-19 \
	--save_path ./snapshots/AFLW-CPM-DET 
	
