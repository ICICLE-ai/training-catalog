---
tags:
  - AI4CI
  - Release 2026-03
---
# AutoSDT

Scaling Data-Driven Discovery Tasks Toward Open Co-Scientists.
AutoSDT is an automatic pipeline for collecting high-quality coding tasks from real-world, data-driven scientific discovery workflows. It uses large language models (LLMs) to search repositories, identify ecologically valid scientific tasks, and synthesize executable task instructions and solutions.

Our AutoSDT collects data-driven discovery tasks in three steps: (1) AutoSDT-Search generates a list of keywords for each discipline and searches for relevant repositories. (2) AutoSDT-Select identifies programs that represent data-driven discovery tasks and extracts their execution dependency folders. (3) AutoSDT-Adapt modifies the selected programs to be independently executable and generates their corresponding task instructions.

We construct AutoSDT-5K, a dataset of 5,404 scientific coding tasks spanning four scientific disciplines (bioinformatics, computational chemistry, geographical information science, and psychology and cognitive neuroscience) and using 756 unique Python packages.

After fine-tuning Qwen2.5-Coder-32B-Instruct on AutoSDT-5K, the model reaches GPT-4o-level performance on ScienceAgentBench with a success rate of 7.8%, doubling the base model performance. It also improves the hypothesis matching score by 17.4% relatively on DiscoveryBench.

Despite long-standing efforts in accelerating scientific discovery with AI, building reliable AI co-scientists remains challenging due to the lack of high-quality data for training and evaluation. AutoSDT addresses this data scarcity problem through an automatic data collection and adaptation pipeline.

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/AutoSDT)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ICICLE-ai/AutoSDT/tree/main?tab=MIT-1-ov-file)

<p align="center">
[<a href="https://osu-nlp-group.github.io/AutoSDT/">Website</a>] •
[<a href="https://arxiv.org/abs/2506.08140">Paper</a>] •
[<a href="https://huggingface.co/datasets/osunlp/AutoSDT-5K">Dataset</a>] •
[<a href="https://x.com/YifeiLiPKU/status/1932962920134046022">Twitter</a>]
</p>


## References
- AutoSDT Project Website: https://osu-nlp-group.github.io/AutoSDT/
- AutoSDT Paper (arXiv): https://arxiv.org/abs/2506.08140
- AutoSDT-5K Dataset (Hugging Face): https://huggingface.co/datasets/osunlp/AutoSDT-5K
- LLaMA-Factory: https://github.com/hiyouga/LLaMA-Factory
- vLLM Documentation: https://docs.vllm.ai/en/latest/

## Issue Reporting
If you encounter any issues, please report through one of the following channels:
- GitHub Issues: https://github.com/OSU-NLP-Group/AutoSDT/issues
- Email: li.14042@osu.edu

When reporting, include your environment, executed command, error logs, and reproduction steps.

## Acknowledgements
Please include other funding sources as needed.

National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606).

## Contact
Yifei Li (li.14042@osu.edu), Hanane Nour Moussa (moussa.45@osu.edu), Huan Sun (sun.397@osu.edu), The Ohio State University

## Disclaimer
AutoSDT creates tasks based on open-source code and data, and we respect creators' ownership and intellectual property. We made best efforts to ensure included repositories have permissive licenses allowing academic use.

We ensure all 1325 repositories composing final tasks in AutoSDT-5K allow academic use, including MIT, GNU, Apache, BSD, CC, Boost, Public Domain, ISC, Eclipse, PolyForm, Mulan, and custom licenses. We manually reviewed repositories with custom licenses to confirm academic and non-commercial use permissions.

## License
Code under this repo is licensed under MIT License.

Note: If your GitHub repository metadata currently shows GPL-3.0 while this README states MIT, please reconcile the mismatch by updating the repository license settings and the root `LICENSE` file to the intended single license.

## Citation
Please cite our paper (and star our repo) if you use our data, models, or code.
```bibtex
@misc{li2025autosdtscalingdatadrivendiscovery,
      title={AutoSDT: Scaling Data-Driven Discovery Tasks Toward Open Co-Scientists}, 
      author={Yifei Li and Hanane Nour Moussa and Ziru Chen and Shijie Chen and Botao Yu and Mingyi Xue and Benjamin Burns and Tzu-Yao Chiu and Vishal Dey and Zitong Lu and Chen Wei and Qianheng Zhang and Tianyu Zhang and Song Gao and Xuhui Huang and Xia Ning and Nesreen K. Ahmed and Ali Payani and Huan Sun},
      year={2025},
      eprint={2506.08140},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2506.08140}, 
}
```
