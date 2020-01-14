{! README.md !}

## Visualization

The git repo for hourly has a custom configuration that allows us to embed
the work hours as a graph in the mkdocs site.
 
If we run `hourly-report` from its own git repo, the graph div gets stored in
`docs/hourly-work.html`. 

The graph is embedded using the [markdown-include](https://github.com/cmacmackin/markdown-include) extension in `mkdocs.yml`.

Then we add the following in our site page:

\{! docs/hourly-work.html !\}

Which embeds the graph below:

{! docs/hourly-work.html !}