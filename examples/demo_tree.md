# Tree Extension Demo

This file demonstrates the `TREE` extension.

## Basic Tree
<!-- docs TREE path="." -->

```
.
├── nested # A nested directory for testing tree descriptions
├── README.md
├── demo_just.md
├── demo_tree.md
└── justfile
```

<!-- /docs -->

## Tree with Depth Limit
<!-- docs TREE path="." depth=3 -->

```
.
├── nested # A nested directory for testing tree descriptions
│   ├── even_more_nested
│   │   ├── most_nested
│   │   ├── README.md
│   │   ├── level_2.md
│   │   └── level_2.py
│   ├── README.md
│   └── level_1.py
├── README.md
├── demo_just.md
├── demo_tree.md
└── justfile
```

<!-- /docs -->

## Tree with Directories Only
<!-- docs TREE path="." dirs_only=true -->

```
.
└── nested # A nested directory for testing tree descriptions
```

<!-- /docs -->
