{! README.md !}

# Visualization

The git repo for hourly has a custom configuration that allows us to embed
the work hours as a graph in the mkdocs site:
 
```yaml
{! hourly-config.yaml !}
```

If we run hourly from its own git repo, the graph div gets stored in
`outputs/<date>/<time>/hourly-work.html`. 

We embed using the `markdown-include` extension in `mkdocs.yml`:

```yaml
{! mkdocs.yml !}
```

And then add the following in our site page:

\{! outputs/2019-12-30/13-57-17/hourly-work.html !\}

Which embeds the graph below:

{! outputs/2019-12-30/13-57-17/hourly-work.html !}