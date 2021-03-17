Figures with .eps extension are automatically converted to .pdf and then inserted. However, there's some weird problem (at least on my setup: Ubuntu 20.04 + TeXstudio) and you need to
```
sudo apt install texlive-font-utils
```
which fixes the .pdf generation.
