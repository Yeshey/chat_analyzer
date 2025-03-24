# chat_analyzer
Statistics for whatsapp chats, emojis, etc

Inspired by [Chat Recapai AI](https://chatrecapai.org/)

Used AI to help create this script

## Usage

1. Open WhatsApp and go to the chat you want to save.
2. Tap the three dots in the top-right corner > More > Export chat.
3. Select Without media.
4. In a nix flakes enabled system: `nix run github.com:Yeshey/chat_analyzer -- test_chat.txt`

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

## Example output

```txt
CHAT STATISTICS
========================================
| METRIC               | JONNAS   | VICTOR   | TOTAL    |
|----------------------|----------|----------|----------|
| Total Messages       |     5245 |     5309 |    10554 |
| Total Words          |    31282 |    24855 |    56137 |
| Words/Message        |     5.96 |     4.68 |     5.32 |

TOP EMOJIS (BOTH)
------------------------------------------------------------
 1. 😘 -    574 times (in 296 separate messages)
 2. ❤ -    294 times (in 165 separate messages)
 3. 🥰 -    184 times (in 88 separate messages)
 4. 😚 -    181 times (in 87 separate messages)
 5. 😋 -     93 times (in 66 separate messages)
 6. 😊 -     76 times (in 52 separate messages)
 7. 👀 -     62 times (in 56 separate messages)
 8. 🤷 -     61 times (in 60 separate messages)
 9. 🙃 -     47 times (in 42 separate messages)
10. 🥴 -     37 times (in 27 separate messages)
11. 🫠 -     36 times (in 35 separate messages)
12. 💪 -     32 times (in 24 separate messages)
13. 😂 -     29 times (in 25 separate messages)
14. 😔 -     27 times (in 16 separate messages)
15. 👍 -     24 times (in 24 separate messages)
16. 😕 -     24 times (in 21 separate messages)
17. 🤔 -     23 times (in 19 separate messages)
18. 🍆 -     22 times (in 18 separate messages)
19. 😅 -     21 times (in 20 separate messages)
20. 🥺 -     21 times (in 16 separate messages)
21. 😭 -     20 times (in 11 separate messages)
22. 👏 -     20 times (in 8 separate messages)
23. 😵 -     20 times (in 15 separate messages)
24. 😍 -     20 times (in 10 separate messages)
25. 😳 -     19 times (in 14 separate messages)
26. 😢 -     19 times (in 15 separate messages)
27. 🥵 -     15 times (in 11 separate messages)
28. ☺ -     14 times (in 14 separate messages)
29. 🥳 -     13 times (in 5 separate messages)
30. 🥲 -     13 times (in 10 separate messages)
31. 🎉 -     11 times (in 7 separate messages)
32. 🙏 -     10 times (in 7 separate messages)
33. 🫶 -     10 times (in 5 separate messages)
34. 💀 -      9 times (in 7 separate messages)
35. 🤦 -      9 times (in 9 separate messages)
36. 😉 -      9 times (in 6 separate messages)
37. 😬 -      8 times (in 8 separate messages)
38. 🤡 -      8 times (in 8 separate messages)
39. 😩 -      8 times (in 4 separate messages)
40. 😖 -      8 times (in 5 separate messages)

TOP EMOJIS (JONNAS)
------------------------------------------------------------
 1. 😘 -    401 times (in 226 separate messages)
 2. 😚 -    169 times (in 82 separate messages)
 3. ❤ -    133 times (in 87 separate messages)
 4. 🥰 -    128 times (in 61 separate messages)
 5. 👀 -     44 times (in 40 separate messages)
 6. 😋 -     38 times (in 29 separate messages)
 7. 😂 -     29 times (in 25 separate messages)
 8. 🤷 -     28 times (in 28 separate messages)
 9. 💪 -     26 times (in 18 separate messages)
10. 🙃 -     21 times (in 17 separate messages)
11. 🍆 -     20 times (in 16 separate messages)
12. 😅 -     18 times (in 18 separate messages)
13. 🥺 -     17 times (in 14 separate messages)
14. 👏 -     17 times (in 7 separate messages)
15. ☺ -     12 times (in 12 separate messages)
16. 🥲 -     12 times (in 9 separate messages)
17. 🥵 -     12 times (in 9 separate messages)
18. 🎉 -     11 times (in 7 separate messages)
19. 👍 -     11 times (in 11 separate messages)
20. 😳 -     10 times (in 8 separate messages)
21. 🤔 -      8 times (in 5 separate messages)
22. 🤦 -      8 times (in 8 separate messages)
23. 🥴 -      7 times (in 7 separate messages)
24. 👌 -      7 times (in 7 separate messages)
25. ツ -      6 times (in 6 separate messages)
26. 😬 -      5 times (in 5 separate messages)
27. 🫠 -      5 times (in 5 separate messages)
28. 😵 -      5 times (in 5 separate messages)
29. 😢 -      5 times (in 2 separate messages)
30. 😙 -      5 times (in 4 separate messages)
31. 😍 -      5 times (in 4 separate messages)
32. ⬆ -      5 times (in 1 separate messages)
33. 🤣 -      5 times (in 2 separate messages)
34. 😭 -      4 times (in 4 separate messages)
35. 😒 -      4 times (in 3 separate messages)
36. 🤗 -      4 times (in 4 separate messages)
37. 😣 -      4 times (in 3 separate messages)
38. 😏 -      4 times (in 4 separate messages)
39. 💯 -      4 times (in 2 separate messages)
40. 🙏 -      3 times (in 3 separate messages)

TOP EMOJIS (VICTOR)
------------------------------------------------------------
 1. 😘 -    173 times (in 70 separate messages)
 2. ❤ -    161 times (in 78 separate messages)
 3. 😊 -     74 times (in 50 separate messages)
 4. 🥰 -     56 times (in 27 separate messages)
 5. 😋 -     55 times (in 37 separate messages)
 6. 🤷 -     33 times (in 32 separate messages)
 7. 🫠 -     31 times (in 30 separate messages)
 8. 🥴 -     30 times (in 20 separate messages)
 9. 🙃 -     26 times (in 25 separate messages)
10. 😔 -     25 times (in 14 separate messages)
11. 😕 -     24 times (in 21 separate messages)
12. 👀 -     18 times (in 16 separate messages)
13. 😭 -     16 times (in 7 separate messages)
14. 🤔 -     15 times (in 14 separate messages)
15. 😵 -     15 times (in 10 separate messages)
16. 😍 -     15 times (in 6 separate messages)
17. 😢 -     14 times (in 13 separate messages)
18. 👍 -     13 times (in 13 separate messages)
19. 😚 -     12 times (in 5 separate messages)
20. 🥳 -     11 times (in 3 separate messages)
21. 😳 -      9 times (in 6 separate messages)
22. 😉 -      9 times (in 6 separate messages)
23. 🫶 -      9 times (in 4 separate messages)
24. 🤡 -      8 times (in 8 separate messages)
25. 🙏 -      7 times (in 4 separate messages)
26. 😩 -      7 times (in 3 separate messages)
27. 💀 -      7 times (in 5 separate messages)
28. 💪 -      6 times (in 6 separate messages)
29. 🤭 -      6 times (in 5 separate messages)
30. 🤟 -      5 times (in 5 separate messages)
31. 😫 -      5 times (in 2 separate messages)
32. 😖 -      5 times (in 4 separate messages)
33. 🥺 -      4 times (in 2 separate messages)
34. 😴 -      4 times (in 1 separate messages)
35. 🥹 -      4 times (in 3 separate messages)
36. 😬 -      3 times (in 3 separate messages)
37. 👉 -      3 times (in 3 separate messages)
38. 👈 -      3 times (in 3 separate messages)
39. 👏 -      3 times (in 1 separate messages)
40. 🥵 -      3 times (in 2 separate messages)
```

![message_timeline](https://github.com/user-attachments/assets/3b204960-ffcd-4722-8b66-dbfc9ed975aa)


