# Mandelbrot-generator

Generate custom mandelbrot images.

Includes two versions (now 3)

Install the dependencies with conda

```bash
conda install --file environment.yaml
```

Try running the command below (be sure to be in the projectfolder)

```bash
python3 main.py images/test.png -l -2 -1.25 -r 1 1.25 --hres 1080
```

Skip the confirmation with `-y` flag

```bash
python3 main.py images/test.png -l -2 -1.25 -r 1 1.25 --hres 1080 -y
```

Read the command help

```bash
python3 main.py test.png -h
```
