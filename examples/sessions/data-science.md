# Example Session: Data Science & ML

This example demonstrates a provisioning session for a data scientist/ML engineer. It follows the question flow defined in `tasks/profiles/data-science.yaml` and shows handling of Python environment setup.

---

## Session Start

**Agent:**
```
Welcome to Agentic Provision! I'll help you set up this Mac for development.

What type of development will you be doing?

A) Full-Stack Web - JavaScript/TypeScript, React, Node.js, PostgreSQL
B) Backend & APIs - Python with FastAPI or Django, databases
C) Mobile Development - React Native, Flutter, or native iOS/Android
D) Data Science & ML - Python, Jupyter, pandas, scikit-learn
E) Other (describe your needs)
```

**User:** D

---

## Phase 2: Gather Requirements

### Question 1: Python Environment

**Agent:**
```
Let's set up your Python data science environment.

How would you like to manage Python versions?

A) pyenv - Multiple Python versions, lightweight, Unix-style
B) Anaconda - Full distribution with conda, many pre-installed packages
C) Miniconda - Minimal conda, install only what you need
D) Not sure - What's the difference?
E) Other
```

**User:** D

**Agent:**
```
Here's how they compare:

**pyenv** manages Python versions only. You use pip for packages. Lightweight,
gives you control, preferred by many developers. Works well with virtual
environments (venv) or tools like Poetry.

**Anaconda** is a full distribution that includes Python plus 250+ data science
packages pre-installed (numpy, pandas, scikit-learn, jupyter, etc.). Uses conda
for package management. Large download (~3GB) but convenient.

**Miniconda** is Anaconda's minimal version. Just Python + conda package manager.
You install only what you need. Best of both worlds for many users.

**Recommendation:**
  • If you want full control: pyenv + pip
  • If you want convenience: Anaconda
  • If you want balance: Miniconda

Which would you prefer?

A) pyenv - Multiple Python versions, lightweight, Unix-style
B) Anaconda - Full distribution with conda, many pre-installed packages
C) Miniconda - Minimal conda, install only what you need
D) Skip - I'll decide later
E) Other
```

**User:** C

---

### Question 2: IDE/Editor

**Agent:**
```
Which IDE or editor do you prefer for data science work?

A) VS Code + Python/Jupyter extensions - Lightweight, flexible
B) PyCharm Professional - Full IDE, excellent debugger, notebook support
C) JupyterLab - Browser-based, great for exploration
D) Cursor - AI-powered, built on VS Code
E) Other
```

**User:** A

---

### Question 3: Notebooks

**Agent:**
```
How would you like to run Jupyter notebooks?

A) JupyterLab - Full-featured, browser-based environment
B) VS Code notebooks - Integrated in your editor
C) Both - JupyterLab for exploration, VS Code for development
D) Skip - I don't need notebooks right now
E) Other
```

**User:** C

---

### Question 4: Database

**Agent:**
```
Do you need a database for your data work?

A) PostgreSQL - Great for structured data, SQL analytics
B) DuckDB - Fast analytics, works with pandas, no server needed
C) Both PostgreSQL and DuckDB
D) None - I'll work with files and cloud storage
E) Other
```

**User:** B

---

### Question 5: Additional Tools

**Agent:**
```
Would you like any additional data tools?

A) Docker - For containerized environments and deployments
B) AWS CLI - For S3, SageMaker, and other AWS services
C) Both Docker and AWS CLI
D) None - I have what I need
E) Other
```

**User:** A

---

### Question 6: Shell

**Agent:**
```
Would you like shell customization?

A) Starship - Fast prompt showing conda env, git status
B) Oh My Zsh - Popular framework with many plugins
C) None - Keep the default shell
D) Skip for now
E) Other
```

**User:** A

---

### Question 7: Git Setup

**Agent:**
```
Do you need help setting up Git?

A) Yes - Configure git and generate SSH keys
B) Just git config - Set my name and email
C) No - Already configured
D) Skip for now
E) Other
```

**User:** C

---

## Phase 3: Present Plan

**Agent:**
```
Here's what I'll set up:

**Package Manager**
  • Homebrew

**Python Environment**
  • Miniconda (conda package manager + Python)

**Editor & Notebooks**
  • VS Code with Python/Jupyter extensions
  • JupyterLab

**Data Tools**
  • DuckDB (fast analytics database)

**Containers**
  • Colima (Docker runtime)
  • Docker CLI

**Shell**
  • Starship prompt (shows conda env)

**CLI Tools** (included by default)
  • ripgrep, fd, jq, httpie, wget

Ready to proceed?

A) Yes, install everything
B) Yes, but let me review each step
C) Modify the plan
D) Start over
```

**User:** A

---

## Phase 4: Execute

**Agent:**
```
Starting installation...

▶ Checking Homebrew...
✓ Homebrew already installed (4.2.0)

▶ Installing Miniconda...
```

```
$ brew install --cask miniconda
```

```
✓ Miniconda installed

Initializing conda for zsh...
```

```
$ /opt/homebrew/Caskroom/miniconda/base/bin/conda init zsh
```

```
✓ Conda initialized

Note: Open a new terminal or run `source ~/.zshrc` to activate conda.
```

---

**Agent:**
```
▶ Creating data science environment...
```

```
$ conda create -n ds python=3.11 numpy pandas scikit-learn matplotlib seaborn jupyter jupyterlab -y
```

```
✓ Environment 'ds' created with core data science packages

To activate: conda activate ds
```

---

**Agent:**
```
▶ Installing VS Code...
```

```
$ brew install --cask visual-studio-code
```

```
✓ VS Code installed

Installing Python extension...
```

```
$ code --install-extension ms-python.python
$ code --install-extension ms-toolsai.jupyter
```

```
✓ Python and Jupyter extensions installed
```

---

**Agent:**
```
▶ Installing DuckDB...
```

```
$ brew install duckdb
```

```
✓ DuckDB installed

Also adding to conda environment...
```

```
$ conda activate ds && pip install duckdb
```

```
✓ DuckDB available in Python
```

---

**Agent:**
```
▶ Installing Colima and Docker...
```

```
$ brew install colima docker
```

```
✓ Docker installed

Note: Run `colima start` when you need Docker.
```

---

**Agent:**
```
▶ Installing Starship...
```

```
$ brew install starship
$ echo 'eval "$(starship init zsh)"' >> ~/.zshrc
```

```
✓ Starship configured
```

---

**Agent:**
```
▶ Installing CLI tools...
```

```
$ brew install ripgrep fd jq httpie wget
```

```
✓ CLI tools installed
```

---

## Phase 5: Completion

**Agent:**
```
✓ Setup complete!

**Installed:**
  • Homebrew (package manager)
  • Miniconda with 'ds' environment
    - Python 3.11, numpy, pandas, scikit-learn
    - matplotlib, seaborn, jupyter, jupyterlab
  • VS Code with Python/Jupyter extensions
  • DuckDB (CLI and Python package)
  • Colima + Docker
  • Starship prompt
  • CLI tools (ripgrep, fd, jq, httpie, wget)

**Quick start:**

1. Activate your environment:
   conda activate ds

2. Start JupyterLab:
   jupyter lab

3. Or open VS Code:
   code .

What would you like to do next?

A) Test the setup (run a quick Python check)
B) Install additional packages (PyTorch, TensorFlow, etc.)
C) Learn about the conda workflow
D) I'm all set!
```

**User:** A

**Agent:**
```
Let me verify everything is working...
```

```
$ source ~/.zshrc && conda activate ds && python -c "
import numpy as np
import pandas as pd
import sklearn
import matplotlib
import duckdb

print('NumPy:', np.__version__)
print('Pandas:', pd.__version__)
print('Scikit-learn:', sklearn.__version__)
print('Matplotlib:', matplotlib.__version__)
print('DuckDB:', duckdb.__version__)
print()
print('✓ All packages imported successfully!')
"
```

```
NumPy: 1.26.3
Pandas: 2.1.4
Scikit-learn: 1.4.0
Matplotlib: 3.8.2
DuckDB: 0.9.2

✓ All packages imported successfully!
```

```
Your data science environment is ready!

Some commands to remember:
  • `conda activate ds` - Activate your environment
  • `conda install <package>` - Install new packages
  • `jupyter lab` - Start JupyterLab
  • `duckdb` - Start DuckDB CLI

Happy analyzing! 📊
```

---

## Key Behaviors Demonstrated

1. **Environment explanation** - Clearly explains pyenv vs Anaconda vs Miniconda tradeoffs
2. **Pre-created environment** - Sets up a 'ds' environment with common packages
3. **Tool integration** - Installs DuckDB both as CLI and in Python environment
4. **Verification step** - Offers to test the setup with actual imports
5. **Conda-aware prompt** - Starship shows active conda environment
6. **Practical next steps** - Quick start commands specific to data science workflow
