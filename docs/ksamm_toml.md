# KSAMM_TOML

The `ksamm.toml` file is a file used to give information to KSA Mod Manager about your mod. As of current you can define required and optional dependencies for your mod as well as a link to download them. Only dependencies that the user does not have will show up in the list that they are given. To ensure proper functionality of this file please ensure that you use the actual mod name in dependencies (The same name as would be used in manifest.toml)

the `ksamm.toml` should be put in the main folder for your mod. Here is an example for the folder format:

```
PolarEarth/
├──Textures/
├──mod.toml
├──ksamm.toml
└── ...
```

Here is a sample `ksamm.toml`:

```
[[dependencies]]
name = "<name1>"
link = "<link1>"

[[dependencies]]
name = "<name2>"
link = "<link2>"

[[optional_dependencies]]
name = "<name3>"
link = "<link3>"

[[optional_dependencies]]
name = "<name4>"
link = "<link4>"
```

New features will be created in the future.
