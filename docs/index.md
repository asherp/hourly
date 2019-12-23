{! README.md !}


# Visualization

We can generate a graph of work committed to the hourly project:

```console
	hourly -s 2018-10-21  --ignore "pro bono" -e "Dec 1, 2019" --plot docs/hourly-graph.html --include_plotlyjs cdn
```
<iframe src="hourly-graph.html" height="400" width="700"></iframe>