
# base model mbpp stop tokens
# stop tokens ['<|endoftext|>', '<|endofmask|>', '</s>', '\nif __name__', '\ndef main(', '\nprint(', '\n"""', '\nassert']
# base model human stop tokens
# stop tokens ['<|endoftext|>', '<|endofmask|>', '</s>', '\nif __name__', '\ndef main(', '\nprint(', '\ndef ', '\nclass ', '\nimport ', '\nfrom ', '\nassert ']

# mbpp chat with assert: 
# stop tokens ['<|endoftext|>', '<|endofmask|>', '</s>', '\nif __name__', '\ndef main(', '\nprint(', '\n"""', '\nassert']
# humaneval 
# stop tokens ['<|endoftext|>', '<|endofmask|>', '</s>', '\nif __name__', '\ndef main(', '\nprint(', '\n```\n']

# MODEL_PATH=$1
MODEL_PATH=/home/xizhang/blobs/msranlpintern_xx/projects/instruct_tuning/experiments/xingxing/gv15/code/code_5m_1028_4m_xl_1m_hany_all_git/llama3.1_8b_mi300_pre/model_lr1e-5_batch512_epochs3_gpus8_nodes4_linearSchedule

SAVE_PATH=${MODEL_PATH}/evaluation/open_instruct_results_local

PLUS_DIR=$SAVE_PATH/evalplus_test_w_assert

# rm -rf ${PLUS_DIR}

mkdir -p ${PLUS_DIR}
identifier=evalplus


PYTHONPATH=.. evalplus.evaluate --model ${MODEL_PATH} --dataset mbpp --backend vllm --greedy \
    --root ${PLUS_DIR} --model_identifier "evalplus"


PYTHONPATH=.. evalplus.evaluate --model ${MODEL_PATH} --dataset humaneval --backend vllm --greedy \
    --root ${PLUS_DIR} --model_identifier "evalplus"

