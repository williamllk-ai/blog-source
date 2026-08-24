# William Lu Blog Source

Source files for my personal academic blog.

Website:

https://williamllk-ai.github.io/

## Framework

This blog is built with:

-   Hexo
-   Stellar Theme

## Repository Structure

``` text
source/                 # Markdown posts, pages, images and custom assets
themes/                 # Hexo themes
scaffolds/              # Hexo article templates
_config.yml             # Hexo configuration
_config.stellar.yml     # Stellar theme configuration
package.json            # Node.js dependencies
```

## Local Development

Install dependencies:

``` bash
npm install
```

Start local preview:

``` bash
hexo server
```

Generate static files:

``` bash
hexo generate
```

Deploy to GitHub Pages:

``` bash
hexo deploy
```

## Writing New Posts

Create a new post:

``` bash
hexo new post "Post Title"
```

The generated Markdown file will be located in:

``` text
source/_posts/
```

## Deployment Workflow

The source repository stores the Hexo project files.

The generated static website is deployed separately to:

``` text
williamllk-ai.github.io
```

Workflow:

``` text
Hexo Source
    |
    | hexo generate
    v
Generated Static Files
    |
    | hexo deploy
    v
GitHub Pages Website
```

## Notes

This repository contains the source code and content of the blog.

Generated files, deployment cache, and local dependencies are excluded
through `.gitignore`.
