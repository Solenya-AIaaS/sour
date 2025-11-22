# Just Extension Demo

This file demonstrates the `JUST` extension.

## Hello Recipe
<!-- docs JUST recipe="hello" -->

Say hello

```bash
just hello
```

<!-- /docs -->

## Build Recipe (Code only)
<!-- docs JUST recipe="build" format="code" -->

```just
build:
    echo "Building..."
```

<!-- /docs -->

## Hello Recipe (Doc only)
<!-- docs JUST recipe="hello" format="doc" -->

Say hello

<!-- /docs -->

## Hello Recipe (Quarto Safe)
<!-- docs JUST recipe="hello" quarto_safe="true" -->

Say hello

```{{bash}}
just hello
```

<!-- /docs -->
