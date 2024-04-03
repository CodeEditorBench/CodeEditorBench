# CodeEditorBench: A Framework for Evaluating Code Editing Capability of Large Language Models

<p align="center">
    <a href="https://codeeditorbench.github.io"><img src="https://img.shields.io/badge/🏠-Home Page-8A2BE2"></a>
    <a href="https://openreview.net/forum?id=OUWD60zfcZ"><img src="https://img.shields.io/badge/Paper-Arxiv-red"></a>
    <a href="https://huggingface.co/datasets/m-a-p/CodeEditorBench"><img src="https://img.shields.io/badge/🤗%20Hugging%20Face-CodeEditorBench-yellow"></a>
    <a href="https://github.com/CodeEditorBench/CodeEditorBench/blob/main/LICENSE"><img src="https://img.shields.io/badge/LICENSE-Apache--2.0-green"></a>
</p>



## Introduction

Large Language Models (LLMs) for code are rapidly evolving, with code editing emerging as a critical capability. We introduce CodeEditorBench, a pioneering evaluation framework designed to rigorously assess the performance of LLMs in code editing tasks, including debugging, translating, polishing, and requirement switching. Unlike existing benchmarks focusing solely on code generation, CodeEditorBench emphasizes real-world scenarios and practical aspects of software development.

We curated diverse coding challenges and scenarios from five sources, covering various programming languages, complexity levels, and editing tasks. Evaluating 17 LLMs revealed that closed-source models, particularly Gemini-Ultra and GPT-4, outperform open-source models in CodeEditorBench, highlighting differences in model performance based on problem type and prompt sensitivity. CodeEditorBench aims to catalyze advancements in LLMs by providing a robust platform for assessing code editing capabilities. We will release all prompts and datasets to enable the community to expand the dataset and benchmark emerging LLMs. By introducing CodeEditorBench, we contribute to the advancement of LLMs in code editing and provide a valuable resource for researchers and practitioners in the field. 

<p align="center">
<img width="1000px" alt="CodeEditorBench" src="https://codeeditorbench.github.io/static/images/tech_route.jpg">
</p>



## Quick Start

### Set Environment

- Entering the workspace: `git clone https://github.com/CodeEditorBench/CodeEditorBench.git`

- Create a new conda environment with coder.yml: `conda env create -f coder.yml`
- Activate the coder environment: `conda activate coder`

### Download Data

We upload our datasets on Huggingface.

[CodeEditorBench](https://huggingface.co/datasets/m-a-p/CodeEditorBench)

### Download Models

Before inferencing with open models, make sure you have download all of them from HuggingFace.

We suggest you using `huggingface-cli` to acclerate your downloading process.

```bash
huggingface-cli download --resume-download deepseek-ai/deepseek-coder-33b-instruct --local-dir ./model/deepseek-coder-33b-instruct
```

### Inference

We use `vllm` for inferencing with open models. You can simply run `bash vllm_inference.sh` to inference with all open models we supported. Make sure you have created the output folder.

```bash
mkdir -p greedy_result/{code_debug,code_translate,code_polish,code_switch}
```

Here is a demo code snippet used to explain the hyperparameters.

```bash
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
```

- `base_model`: The open model used to generate output. You can view all supported models in `vllm_inference.sh`.
- `--dataset`: The dataset used for the inference process.
- `--input_data_dir`: The directory where the input data is located.
- `--output_data_dir`: The destination path where the output data will be saved.
- `--batch_size`: Number of samples that will be processed in parallel.
- `--num_of_sequences`: Number of sequences that will be generated for the same question.
- `--num_gpus`: Number of GPUs will be used for computation.
- `--prompt_type`: Type of prompts that model use to generate output.
- `--start_idx`: The starting index for processing the dataset.
- `--end_idx`: The ending index for processing the dataset.

Remember that to fully understand these hyperparameters, you should consult the source code of `vllm_inference.py`.



## Results

<div style="text-align: center;">
    <img src="./mdPICs/Models-Zero Shot.png" class="result"
    width="45%" />
    <img src="./mdPICs/win_rate_zero.png" class="result"
    width="45%" />
</div>

We propose evaluating LLMs across four scenarios capturing various code editing capabilities, namely code debug, code translate, code polish, and code requirement switch.The figure depicts various model performances across the four scenarios available in CodeEditorBench\_Plus in a radial plot – highlighting how relative differences across models change across the scenarios. We also give the Performance of open-source and closed-source models on CodeEditorBench\_Plus in zero-shot evaluated through win\_rate.



## Citation





## Acknowledgement