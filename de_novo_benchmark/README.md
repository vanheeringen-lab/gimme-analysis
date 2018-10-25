Configuration
=============

The file `config.yaml` contains the configuration:

``` 
```

Please update this where necessary. 
For the ENCODE peaks you will need to have hg19 installed (shameless plug: use [genomepy](https://github.com/simonvh/genomepy)).

Install the workflow dependencies using conda:

```
conda env create -n de_novo_benchmark --file environment.yaml
```

Activate the enviroment.

``` 
source activate de_novo_benchmark
```

And (dry)run! Remove the `-n` to really run.

```
snakemake --use-conda -n
```
