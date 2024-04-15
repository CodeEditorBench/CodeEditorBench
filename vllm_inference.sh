#!/bin/bash

base_models=(
    "WizardLM/WizardCoder-33B-V1.1" "deepseek-ai/deepseek-coder-33b-instruct" \
    "codefuse-ai/CodeFuse-CodeLlama-34B" "Phind/Phind-CodeLlama-34B-v2" \
    "codellama/CodeLlama-7b-Instruct-hf" "codellama/CodeLlama-34b-Instruct-hf" \
    "ise-uiuc/Magicoder-S-DS-6.7B" "bigcode/octocoder" \
    "WizardLM/WizardCoder-15B-V1.0" "codellama/CodeLlama-13b-Instruct-hf" \
    "codellama/CodeLlama-34b-hf" "ise-uiuc/Magicoder-S-CL-7B" \
    "m-a-p/OpenCodeInterpreter-DS-6.7B" "m-a-p/OpenCodeInterpreter-DS-33B" \
)
datasets=("debug" "translate" "polishment" "switch")

for base_model in "${base_models[@]}"; do
    for dataset in "${datasets[@]}"; do
        echo "Running inference with base_model: $base_model and dataset: $dataset"
        python vllm_inference.py \
            --base_model "$base_model" \
            --dataset "$dataset" \
            --input_data_dir "./data/" \
            --output_data_dir "./greedy_result/" \
            --batch_size 64 \
            --num_of_sequences 1 \
            --num_gpus 8 \
            --prompt_type "zero" \
            --start_idx 0 \
            --end_idx -1
    done
done