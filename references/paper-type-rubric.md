# Paper Type Classification Rubric

Classify the paper into ONE primary type before analysis. The type determines which method analysis template to apply.

## Types & Indicators

### AI/深度学习
Needs 2+ indicators:
- Neural network, deep learning, transformer, CNN, RNN, GAN, diffusion model
- Reports accuracy/F1/mAP/BLEU/perplexity on benchmark datasets
- Model architecture diagram present
- GPU training, batch size, learning rate as hyperparameters
- Standard datasets: ImageNet, COCO, SQuAD, GLUE, etc.

### 传统算法/理论
Needs 2+ indicators:
- Algorithm with pseudocode or formal proof
- Complexity analysis (O-notation)
- No neural network components
- Theorem/lemma/proof structure
- Optimization, graph theory, combinatorics, formal methods

### 系统/工程
Needs 2+ indicators:
- System architecture (components, interfaces, protocols)
- Metrics: throughput, latency, scalability, availability
- Implementation details (language, framework, deployment)
- Compares with existing systems

### 实验/实证
Needs 2+ indicators:
- Human subjects, user studies, surveys
- Statistical analysis (p-value, confidence interval, effect size)
- IRB/ethics approval mentioned
- Qualitative or mixed-methods research

### 综述/Survey
Needs 1 indicator:
- Title contains "survey", "review", "overview", "综述"
- Systematically reviews 20+ papers
- No original experiments or novel method proposed

### 其他/跨学科
Use when paper spans multiple types or fits none above.

## Conflict Resolution

1. Check paper's own claim in abstract ("we propose", "we conduct a user study")
2. Use type with more indicators
3. If tied → `其他/跨学科`, note both types

## Output Format

```
论文类型：[类型标签]
判断依据：[2-3个具体指标，引用论文内容]
```
