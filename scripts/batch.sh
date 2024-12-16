
modeldir=$1

# for ckpt in 8000 12000
# for ckpt in 14000 16000
# for ckpt in 17000
# for ckpt in 20000

# for ckpt in 22000 24000 26000 28000 30000

# for ckpt in `seq 32000 2000 44000`
# for ckpt in 22000 24000 26000 28000 30000
# 12000
for ckpt in 10000 8000 6000 4000 2000
do
    echo "ckpt $ckpt ..."
    # rm $modeldir/checkpoint-${ckpt}/evaluation/open_instruct_results_local/evalplus/*/*_results.json
    bash run.sh $modeldir/checkpoint-${ckpt}
done
