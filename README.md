# chat_analyzer
Statistics for whatsapp chats, emojis, etc

Inspired by [Chat Recapai AI](https://chatrecapai.org/)

Used AI to help create this script

## Make a poetry2nix project

1. Start with `nix-shell -p poetry`
2. `poetry init`
3. Add packages with for example `poetry add matplotlib pandas python-dateutil`
4. structure:
    ```
    ├── chatanalyzer # same as project name `[tool.poetry]` `name = "chatanalyzer"`
    │   ├── __init__.py
    │   └── main.py 
    ```
5. script defined in poetry's toml
   ```toml
    [tool.poetry.scripts]
    start = "chatanalyzer.main:main" # file main, runs function main
   ```
6. As mencioned in the script above `main.py` needs to have a `def main()` function, that is what will be ran.
7. the `start` here: ` start = "chatanalyzer.main:main" # file main, runs function main` is the same in the flake.nix here: `program = "${self.packages.${system}.default}/bin/start";`

**Update:**
1. `nix develop`
2. `poetry update`
3. `nix flake update`
