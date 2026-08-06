#!/bin/sh

set -eu

APP_NAME="Github-Activity"
SCRIPT_NAME="ghe.py"

SOURCE_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

BIN_DIR="$HOME/.local/bin"
APP_DIR="$BIN_DIR/$APP_NAME"

SOURCE_FILE="$SOURCE_DIR/$SCRIPT_NAME"
TARGET_FILE="$APP_DIR/$SCRIPT_NAME"
COMMAND_FILE="$BIN_DIR/ghe"

echo "Installing $APP_NAME..."

# Check Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: Python 3 is required."
    exit 1
fi

# Check file
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: $SCRIPT_NAME not found."
    exit 1
fi


mkdir -p "$APP_DIR"
mkdir -p "$BIN_DIR"


cp "$SOURCE_FILE" "$TARGET_FILE"

chmod 755 "$TARGET_FILE"


cat > "$COMMAND_FILE" <<EOF
#!/bin/sh
exec python3 "$TARGET_FILE" "\$@"
EOF

chmod 755 "$COMMAND_FILE"


add_path() {
    CONFIG="$1"

    touch "$CONFIG"

    if ! grep -q ".local/bin" "$CONFIG"; then
        {
            echo ""
            echo "# Github-Activity"
            echo 'export PATH="$HOME/.local/bin:$PATH"'
        } >> "$CONFIG"
    fi
}


add_fish_path() {
    CONFIG="$HOME/.config/fish/config.fish"

    mkdir -p "$HOME/.config/fish"
    touch "$CONFIG"

    if ! grep -q "fish_add_path ~/.local/bin" "$CONFIG"; then
        {
            echo ""
            echo "# Github-Activity"
            echo "fish_add_path ~/.local/bin"
        } >> "$CONFIG"
    fi
}


CURRENT_SHELL="$(ps -p $$ -o comm= | tr -d ' ')"

case "$CURRENT_SHELL" in

    fish)
        add_fish_path
        ;;

    bash)
        add_path "$HOME/.bashrc"
        ;;

    zsh)
        add_path "$HOME/.zshrc"
        ;;

    ksh|mksh)
        add_path "$HOME/.kshrc"
        ;;

    *)
        echo "Shell not supported: $CURRENT_SHELL"
        echo "Command installed, but PATH was not modified."
        ;;

esac


echo
echo "================================"
echo "Installation completed!"
echo
echo "Run:"
echo "    ghe"
echo
echo "Installed:"
echo "    $COMMAND_FILE"
echo "================================"