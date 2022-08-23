# Installation

```bash
conda create -n yubaba python=3.8 -y
conda activate yubaba
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch

git clone https://github.com/TeamCHK/yubaba.git
cd model_dev
pip install -r requirements.txt
```

Add COMET API KEY to your ~/.bashrc
```bash
export COMET_API_KEY="YOUR_COMET_API_KEY"
```
# Run Inference


# Run Training
