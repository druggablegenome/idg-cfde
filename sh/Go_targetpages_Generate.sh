#!/bin/bash
# Create TCRD target page files.
###

date

T0=$(date +%s)

TCRD_VERSION="684"

cwd=$(pwd)

DATADIR="${cwd}/data/targetpages${TCRD_VERSION}"
if [ ! -f ${DATADIR} ]; then
	mkdir -p ${DATADIR}
fi
#
python3 -m BioClients.idg.tcrd.Client listTargets \
	--o $DATADIR/tcrd_targets.tsv
#
cat $DATADIR/tcrd_targets.tsv |sed '1d' \
	|awk -F '\t' '{print $1}' |sort -nu \
	>$DATADIR/tcrd_targets.tid
#
N=$(cat $DATADIR/tcrd_targets.tid |wc -l)
#
printf "N_targets = %d\n" "$N"
#
I=0
while [ $I -lt $N ]; do
	I=$[$I + 1]
	tid=$(cat $DATADIR/tcrd_targets.tid |sed "${I}q;d")
	TID=$(printf "%05d" ${tid})
	FILENAME="tcrd_target_${TID}.json"
	printf "${I}. TID=${tid}; FILE=${FILENAME}\n"
	ofile=${DATADIR}/${FILENAME}
	python3 -m BioClients.idg.tcrd.Client getTargetPage --ids "${tid}" --o $ofile
done
#
printf "Elapsed: %ds\n" "$[$(date +%s) - $T0]"
date
#
