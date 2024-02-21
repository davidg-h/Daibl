#!/bin/bash
#SBATCH --job-name=evaluation # Kurzname des Jobs
#SBATCH --nodes=1 # Anzahl benötigter Knoten
#SBATCH --ntasks=1 # Gesamtzahl der Tasks über alle Knoten hinweg
#SBATCH --partition=p2 # Verwendete Partition (z.B. p0, p1, p2 oder all)
#SBATCH --time=12:00:00 # Gesamtlimit für Laufzeit des Jobs (Format: HH:MM:SS)
#SBATCH --cpus-per-task=16 # Rechenkerne pro Task
#SBATCH --mem=24G # Gesamter Hauptspeicher pro Knoten
#SBATCH --gres=gpu:1 # Gesamtzahl GPUs pro Knoten
#SBATCH --qos=basic # Quality-of-Service
#SBATCH --mail-type=ALL # Art des Mailversands (gültige Werte z.B. ALL, BEGIN, ↪ END, FAIL oder REQUEUE)
#SBATCH --mail-user=nguyenda81452@th-nuernberg.de # Emailadresse für Statusmails
#SBATCH --output=/nfs/scratch/students/nguyenda81452/logs/slurm-%j.out # Output Pfad der slurm Dateien
echo "=================================================================="
echo "Starting Batch Job at $(date)"
echo "Job submitted to partition ${SLURM_JOB_PARTITION} on ${SLURM_CLUSTER_NAME}"
echo "Job name: ${SLURM_JOB_NAME}, Job ID: ${SLURM_JOB_ID}"
echo "Requested ${SLURM_CPUS_ON_NODE} CPUs on compute node $(hostname)"
echo "=================================================================="
###################### Optional for Pythonnutzer:innen #######################
# Die folgenden Umgebungsvariablen stellen sicher, dass
# Modelle von Huggingface und PIP Packages nicht unter
# /home/$USER/.cache landen.
CACHE_DIR=/nfs/scratch/students/nguyenda81452/CACHE_DIR/huggingface/hub
export PIP_CACHE_DIR=$CACHE_DIR
export TRANSFORMERS_CACHE=$CACHE_DIR
export HF_HOME=$CACHE_DIR
mkdir -p CACHE_DIR
########################################################
############### Starte eigenen Job hier ################

# info
echo -n "Server: "; hostname
echo "Startet by $USER"; 
echo -n "Working Dir: "; pwd


source /nfs/scratch/students/nguyenda81452/.venv/bin/activate # activate .venv for slurm

cd /nfs/scratch/students/nguyenda81452/project/daibl/discord_bot/main/evaluation
python evaluation.py

########################################################