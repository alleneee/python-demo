from transformers import AutoTokenizer, AutoModelForCausalLM

# 指定 LLaMA 3 的模型名称
model_name = "meta-llama/Llama-3b"  # 这里假设使用的是 3B 参数的 LLaMA 模型

# 加载 Tokenizer 和 预训练模型
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

from datasets import load_dataset

# 加载 wikitext 数据集作为示例
dataset = load_dataset("wikitext", "wikitext-103-raw-v1")

# 定义数据预处理函数
def preprocess_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

# 应用数据预处理
tokenized_dataset = dataset.map(preprocess_function, batched=True, num_proc=4, remove_columns=["text"])


from torch.utils.data import DataLoader
from transformers import DataCollatorForLanguageModeling

# 创建数据填充器
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# 定义训练和验证数据加载器
train_dataloader = DataLoader(tokenized_dataset["train"], batch_size=4, shuffle=True, collate_fn=data_collator)
eval_dataloader = DataLoader(tokenized_dataset["validation"], batch_size=4, collate_fn=data_collator)


from transformers import TrainingArguments, Trainer

# 定义训练参数
training_args = TrainingArguments(
    output_dir="./llama3-results",  # 输出文件夹
    evaluation_strategy="epoch",    # 每个 epoch 进行一次评估
    learning_rate=2e-5,             # 学习率
    per_device_train_batch_size=4,  # 每个设备上的训练批次大小
    per_device_eval_batch_size=4,   # 每个设备上的评估批次大小
    num_train_epochs=3,             # 训练轮数
    weight_decay=0.01,              # 权重衰减
    logging_dir='./logs',           # 日志保存路径
    logging_steps=10,               # 日志记录的步数
    save_steps=500,                 # 模型保存的步数
    save_total_limit=2,             # 保存的总模型数量限制
    fp16=True,                      # 如果使用 GPU，加速训练的混合精度
)


# 创建 Trainer 实例
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator
)

# 开始训练
trainer.train()

# 评估模型
results = trainer.evaluate()
print(results)

# 保存模型
trainer.save_model("./llama3-finetuned-model")
tokenizer.save_pretrained("./llama3-finetuned-model")

from transformers import pipeline

# 加载训练好的模型和 tokenizer
llama_pipeline = pipeline("text-generation", model="./llama3-finetuned-model", tokenizer=tokenizer)

# 使用模型进行文本生成
generated_text = llama_pipeline("Once upon a time", max_length=50, num_return_sequences=1)
print(generated_text)
