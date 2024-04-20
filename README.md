# Examples using the Fine Tuning Framework.

This repo uses the [llm-research-fine-tuning](https://github.com/ai-hero/llm-research-fine-tuning) and [llm-research-orchestration](https://github.com/ai-hero/llm-research-orchestration) repos to run fine tuning jobs, locally or in the cloud.

## Setup

### Requirements

```sh
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Llama 2

Make sure you've signed the T&Cs to be able to access the llama-2 weights on Huggingface.

### Environment

You'll also need a `.env` file in the folder from where you'll run the jobs.

```
# For reporting experiments to W&B
WANDB_API_KEY=
WANDB_USERNAME=

# For loading/saving data/models to Huggingface
HF_TOKEN=

# For downloading data to from S3
S3_ENDPOINT=s3.amazonaws.com
S3_ACCESS_KEY_ID=
S3_SECRET_ACCESS_KEY=
S3_REGION=us-east-2
S3_SECURE=true
```

### Data

Set up data for training or inference using the instructions in the [llm-research-data](https://github.com/ai-hero/llm-research-data) project.

## Running in colab.

Please checkout `notebooks/Launch_SFT_jobs_in_the_Notebook.ipynb`.

## Running on Coreweave: Launching a Fine-Tuning Job

### Kubernetes

Currently we are only supporting Coreweave.

- `Coreweave` - We assume that you have downloaded the `kubeconfig` file and can see your pods using `kubectl get pods`.

### Update the Config for the Job

Update [k8s/configs/<YOUR CONFIG>.yaml](k8s/yamls/) as needed for your job.

### Launch the Job

```sh
python k8s/train.py launch rparundekar/fine_tune_research:a327fd0 ./k8s/configs/simple_text.yaml
```

You'll see the name of the job. And instructions to see the logs and delete the job.
NOTE: The container is created in the fine-tuning project.

The hash above should be the 7-hex hash in the [llm-research-fine-tuning](https://github.com/ai-hero/llm-research-fine-tuning) project's main branch.

#### If launching with a distributed config

```sh
python k8s/train.py launch rparundekar/fine_tune_research:fbea00f distributed_default.yaml -d fsdp_single_worker.yaml
```

#### Deleting a Job

Use the same program to delete the job so that all resources are deleted.

```sh
python k8s/train.py delete <job-name>
```

## Batch Inference with Pretrained LLM

```sh
python k8s/infer.py launch rparundekar/fine_tune_research:fbea00f open_instruct_batch_inference.yaml
```

## Serving a Trained Model

We'll use the Huggingface TGI library to serve a model. The program will read details of the output model from the training config and serve in Kubernetes.
Then, you can port forward locally and run the PoC

```sh
python k8s/serve.py launch mmlu_peft.yaml
```

### Running the PoC

The PoC assumes that the model server is running at `http://127.0.0.1:8080/`.

```sh
streamlit run poc/poc.py
```
