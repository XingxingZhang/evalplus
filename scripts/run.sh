
MODEL_PATH=$1

SAVE_PATH=${MODEL_PATH}/evaluation/open_instruct_results_local

PLUS_DIR=$SAVE_PATH/evalplus

# rm -rf ${PLUS_DIR}

mkdir -p ${PLUS_DIR}
identifier=evalplus


PYTHONPATH=.. evalplus.evaluate --model ${MODEL_PATH} --dataset mbpp --backend vllm --greedy \
    --root ${PLUS_DIR} --model_identifier "evalplus"


PYTHONPATH=.. evalplus.evaluate --model ${MODEL_PATH} --dataset humaneval --backend vllm --greedy \
    --root ${PLUS_DIR} --model_identifier "evalplus"


# PYTHONPATH=../evalplus evalplus.evaluate --model $model --dataset mbpp --backend vllm --greedy \
#     --model_identifier "evalplus" --root $root
