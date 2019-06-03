DATA_DIR=data/remap/
REMAP_FILE=remap2018_public_nr_macs2_hg38_v1_2.bed.gz
REMAP_URL=http://tagc.univ-mrs.fr/remap/download/remap2018/hg38/MACS/
MIN_NPEAK=1000

mkdir -p $DATA_DIR

# Download from remap
if [ ! -e $DATA_DIR/$REMAP_FILE ]; then
    wget -P $DATA_DIR $REMAP_URL/$REMAP_FILE
fi

# Split the big download from remap
zcat $DATA_DIR/$REMAP_FILE | awk -vd=$DATA_DIR '{print $1 "\t" $7 - 50 "\t"  $8 + 50 >> d"/"$4; close($4)}'; for i in `ls $DATA_DIR/[A-Z]* | grep -v bed`; do mv $i $i.bed; done

# gzip it!
gzip $DATA_DIR/*.bed

# Remove all files with less than 1000 peaks
for i in $DATA_DIR/[A-Z]*bed.gz; do echo $i `zcat $i | wc -l`; done | tr \  \\t | sort -k2g | awk -vnpeak=$MIN_NPEAK '$2 < npeak' | cut -f1 | xargs rm
