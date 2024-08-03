python3.11 -m venv environment
environment\Scripts\Activate.ps1
pip install streamlit Pillow tensorflow-cpu~=2.17.0 torch==2.4.0+cu121 torchvision==0.19.0+cu121 jax[cpu] --extra-index-url https://download.pytorch.org/whl/cu121
pip install --upgrade keras
