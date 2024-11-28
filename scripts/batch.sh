
modeldir=$1

# for ckpt in 8000 12000
# for ckpt in 14000 16000
# for ckpt in 17000
# for ckpt in 20000
for ckpt in 2500 2000 3000
do
    bash run.sh $modeldir/checkpoint-${ckpt}
done
