# 🐙 GitHub Activity CLI

A command-line interface (CLI) tool built with Python to fetch, filter, and display the recent activity of any GitHub user directly in your terminal.


## 🚀 Features

* **Zero External Dependencies:** Built using strictly Python standard library modules.
* **Visual Summary:** Quickly view an activity breakdown with visual bars directly in the console.
* **Filter by Event Type:** Filter specific actions like `PushEvent`, `PullRequestEvent`, `IssuesEvent`, etc.
* **Activity Statistics:** Highlights interacted repositories and calculates the day(s) with the highest contribution count.
* **Colorized Terminal Output:** Formatted with ANSI colors for enhanced readability.


## 📋 Requirements

* **Python 3.8** or higher.


## 📦 Quick Installation

Choose your operating system and follow the instructions below.

## 🐧 Linux

### Automatic Installation

Run the installation script:

```bash
cd Github-Activity
chmod +x install.sh
./install.sh
```

The installer will:

- Copy `ghe.py` to `~/.local/bin`
- Give execution permissions
- Configure the `ghe` command


## ⚠️ Manual Installation

If the installation script does not work, follow these steps.


### 1. Create the local binary directory

Create the `.local/bin` folder inside your home directory:

```bash
mkdir -p ~/.local/bin
```

Copy the program file:

```bash
cp ghe.py ~/.local/bin/
```

Give execution permissions:

```bash
chmod +x ~/.local/bin/ghe.py
```


### 2. Find your shell configuration file

Open the configuration file for your shell:

**Bash**

```
~/.bashrc
```

**Zsh**

```
~/.zshrc
```

**Fish**

```
~/.config/fish/config.fish
```

**Ksh**

```
~/.kshrc
```

**Tcsh / Csh**

```
~/.tcshrc
```


### 3. Create the `ghe` command

Add the following code depending on your shell.


### Bash

Add to `~/.bashrc`:

```bash
ghe() {
    python3 ~/.local/bin/ghe.py "$@"
}
```

Reload:

```bash
source ~/.bashrc
```


### Zsh

Add to `~/.zshrc`:

```zsh
ghe() {
    python3 ~/.local/bin/ghe.py "$@"
}
```

Reload:

```zsh
source ~/.zshrc
```


### Fish

Add to `~/.config/fish/config.fish`:

```fish
function ghe
    python3 ~/.local/bin/ghe.py $argv
end
```

Reload:

```fish
source ~/.config/fish/config.fish
```


### Ksh

Add to `~/.kshrc`:

```ksh
function ghe {
    python3 ~/.local/bin/ghe.py "$@"
}
```

Reload:

```bash
source ~/.kshrc
```


### Tcsh / Csh

`tcsh` and `csh` do not support functions. Use an alias instead.

Add to `~/.tcshrc`:

```tcsh
alias ghe 'python3 ~/.local/bin/ghe.py \!*'
```

Reload:

```tcsh
source ~/.tcshrc
```


## ✅ Verify Installation

Run:

```bash
ghe --help
```

If everything is correct, the GitHub Activity CLI help menu will appear.


## 🍎 macOS

```bash
git clone https://github.com/Gnn2009/Github-Activity.git && cd Github-Activity
```


## 🪟 Windows (CMD / PowerShell)

```bash
git clone https://github.com/Gnn2009/Github-Activity.git ; cd Github-Activity
```


#### Project Idea From:

* https://roadmap.sh/projects/github-user-activity
